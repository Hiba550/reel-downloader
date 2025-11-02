from flask import Flask, render_template, request, send_file, url_for
import os
import instaloader
import re
import uuid
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

TEMP_DOWNLOADS_DIR = Path('temp_downloads')
TEMP_DOWNLOADS_DIR.mkdir(exist_ok=True)
RETENTION_HOURS = int(os.getenv('DOWNLOAD_RETENTION_HOURS', '6'))

# Initialize Instaloader
L = instaloader.Instaloader(
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern='',
    max_connection_attempts=3
)


def clean_old_downloads(max_age_hours: int = RETENTION_HOURS) -> None:
    """Remove temporary download folders older than the allowed retention period."""
    if not TEMP_DOWNLOADS_DIR.exists():
        return

    cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)

    for folder in TEMP_DOWNLOADS_DIR.iterdir():
        if not folder.is_dir():
            continue
        try:
            modified_at = datetime.utcfromtimestamp(folder.stat().st_mtime)
            if modified_at < cutoff:
                shutil.rmtree(folder, ignore_errors=True)
                logger.info(f"Cleaned expired download directory: {folder}")
        except Exception as exc:
            logger.warning(f"Failed to inspect temp folder {folder}: {exc}")


def format_filesize(num_bytes: int | None) -> str | None:
    if not num_bytes:
        return None
    size = float(num_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024 or unit == 'TB':
            if unit == 'B':
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024


def format_duration(seconds: float | None) -> str | None:
    if seconds is None:
        return None
    total_seconds = int(round(seconds))
    minutes, sec = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}h {minutes:02d}m {sec:02d}s"
    return f"{minutes:02d}:{sec:02d}"


def abbreviate_number(value: int | None) -> str | None:
    if value is None:
        return None
    for threshold, suffix in ((1_000_000_000, 'B'), (1_000_000, 'M'), (1_000, 'K')):
        if value >= threshold:
            return f"{value / threshold:.1f}{suffix}"
    return f"{value:,}"


def sanitize_caption(text: str | None, limit: int = 420) -> str | None:
    if not text:
        return None
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    truncated = cleaned[:limit].rsplit(' ', 1)[0]
    return truncated.rstrip() + '...'

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    clean_old_downloads()
    
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            error_message = "Please enter an Instagram Reel URL"
        elif 'instagram.com' not in url:
            error_message = "Please enter a valid Instagram URL"
        else:
            try:
                logger.info(f"Processing URL: {url}")
                # Extract shortcode from URL
                match = re.search(r'instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)', url)
                if not match:
                    error_message = "Could not extract post ID from URL"
                else:
                    shortcode = match.group(1)
                    logger.info(f"Extracted shortcode: {shortcode}")
                    
                    # Create unique download directory
                    download_id = str(uuid.uuid4())
                    download_dir = TEMP_DOWNLOADS_DIR / download_id
                    download_dir.mkdir(exist_ok=True)
                    
                    try:
                        # Get post by shortcode
                        post = instaloader.Post.from_shortcode(L.context, shortcode)
                        
                        # Check if it's a video
                        if not post.is_video:
                            error_message = "This post does not contain a video"
                        else:
                            # Download the video
                            logger.info(f"Downloading video to {download_dir}")
                            
                            # Set custom filename pattern
                            old_dirname_pattern = L.dirname_pattern
                            old_filename_pattern = L.filename_pattern
                            
                            L.dirname_pattern = str(download_dir)
                            L.filename_pattern = 'video'
                            
                            # Download video
                            L.download_post(post, target=download_dir)
                            
                            # Restore patterns
                            L.dirname_pattern = old_dirname_pattern
                            L.filename_pattern = old_filename_pattern
                            
                            # Find the downloaded video file
                            video_files = [f for f in os.listdir(download_dir) if f.endswith('.mp4')]
                            
                            if not video_files:
                                error_message = "Failed to download video"
                                return render_template('index.html', error=error_message)
                                
                            # Original video file
                            video_file = video_files[0]
                            
                            # Get title for the video
                            title = f"Instagram Reel by {post.owner_username}"
                            if post.caption:
                                # Use first 40 characters of caption as title
                                title = post.caption.split('\n')[0][:40]
                                if len(post.caption) > 40:
                                    title += "..."
                            
                            # Save metadata
                            video_path = download_dir / video_file

                            likes_display = abbreviate_number(post.likes) if hasattr(post, 'likes') else None
                            try:
                                views_raw = getattr(post, 'video_view_count', None)
                            except Exception:
                                views_raw = None
                            views_display = abbreviate_number(views_raw)
                            duration_seconds = getattr(post, 'video_duration', None)
                            duration_display = format_duration(duration_seconds)
                            filesize_bytes = video_path.stat().st_size if video_path.exists() else None
                            filesize_display = format_filesize(filesize_bytes)
                            published_display = None
                            published_iso = None
                            if hasattr(post, 'date_local') and post.date_local:
                                published_display = post.date_local.strftime('%d %b %Y')
                                try:
                                    published_iso = post.date_utc.isoformat()
                                except Exception:
                                    published_iso = None

                            caption_excerpt = sanitize_caption(post.caption)

                            metadata = {
                                'title': title,
                                'username': post.owner_username,
                                'likes_raw': post.likes,
                                'likes_display': likes_display,
                                'views_raw': views_raw,
                                'views_display': views_display,
                                'duration_seconds': duration_seconds,
                                'filesize_bytes': filesize_bytes,
                                'file': video_file,
                                'published_display': published_display,
                                'published_iso': published_iso,
                                'caption_excerpt': caption_excerpt,
                                'shortcode': shortcode
                            }
                            
                            with open(download_dir / 'info.json', 'w') as f:
                                json.dump(metadata, f)
                            
                            logger.info(f"Download complete: {video_file}")
                            
                            reel_info = {
                                'title': title,
                                'username': post.owner_username,
                                'likes': likes_display,
                                'views': views_display,
                                'duration': duration_display,
                                'filesize': filesize_display,
                                'published': published_display,
                                'caption': caption_excerpt,
                                'shortcode': shortcode
                            }

                            download_url = url_for('download_video', download_id=download_id)
                            preview_url = url_for('download_video', download_id=download_id, preview=1)

                            return render_template(
                                'result.html',
                                download_id=download_id,
                                download_url=download_url,
                                preview_url=preview_url,
                                reel_info=reel_info,
                                retention_hours=RETENTION_HOURS
                            )
                    except instaloader.exceptions.InstaloaderException as e:
                        error_message = f"Instagram error: {str(e)}"
                    except Exception as e:
                        logger.error(f"Error: {str(e)}")
                        error_message = f"Error processing Instagram Reel: {str(e)}"
            except Exception as e:
                logger.error(f"General error: {str(e)}")
                error_message = f"Error: {str(e)}"
    
    return render_template('index.html', error=error_message)

@app.route('/download/<download_id>')
def download_video(download_id):
    download_dir = TEMP_DOWNLOADS_DIR / download_id
    
    if not download_dir.exists():
        return "Download expired or not found", 404
    
    # Load metadata for title
    metadata = {}
    try:
        with open(download_dir / 'info.json', 'r') as f:
            metadata = json.load(f)
    except:
        pass
    
    # Find video file
    video_files = [f for f in os.listdir(download_dir) if f.endswith('.mp4')]
    if not video_files:
        return "Video file not found", 404
    
    video_file = video_files[0]
    video_path = download_dir / video_file
    
    # Create download filename
    title = metadata.get('title', 'instagram_reel')
    safe_title = re.sub(r'[^\w\-_\. ]', '', title)
    safe_title = safe_title.replace(' ', '_')
    
    download_filename = f"{safe_title}.mp4"
    preview_mode = request.args.get('preview') == '1'

    response = send_file(
        video_path,
        mimetype='video/mp4',
        as_attachment=not preview_mode,
        download_name=download_filename
    )

    response.headers['Cache-Control'] = 'no-store'
    if preview_mode:
        response.headers['Content-Disposition'] = f'inline; filename="{download_filename}"'

    return response

if __name__ == '__main__':
    app.run(debug=True)