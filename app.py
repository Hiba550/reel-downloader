from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import instaloader
import re
import uuid
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Create temp directory
if not os.path.exists('temp_downloads'):
    os.makedirs('temp_downloads')

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

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    
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
                    download_dir = os.path.join('temp_downloads', download_id)
                    os.makedirs(download_dir, exist_ok=True)
                    
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
                            
                            L.dirname_pattern = download_dir
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
                                return render_template('index_simple.html', error=error_message)
                                
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
                            metadata = {
                                'title': title,
                                'username': post.owner_username,
                                'likes': post.likes if post.likes else 0,
                                'file': video_file
                            }
                            
                            with open(os.path.join(download_dir, 'info.json'), 'w') as f:
                                json.dump(metadata, f)
                            
                            logger.info(f"Download complete: {video_file}")
                            
                            # Render the results page
                            return render_template('result_simple.html',
                                                download_id=download_id,
                                                title=title,
                                                username=post.owner_username)
                    except instaloader.exceptions.InstaloaderException as e:
                        error_message = f"Instagram error: {str(e)}"
                    except Exception as e:
                        logger.error(f"Error: {str(e)}")
                        error_message = f"Error processing Instagram Reel: {str(e)}"
            except Exception as e:
                logger.error(f"General error: {str(e)}")
                error_message = f"Error: {str(e)}"
    
    return render_template('index_simple.html', error=error_message)

@app.route('/download/<download_id>')
def download_video(download_id):
    download_dir = os.path.join('temp_downloads', download_id)
    
    if not os.path.exists(download_dir):
        return "Download expired or not found", 404
    
    # Load metadata for title
    metadata = {}
    try:
        with open(os.path.join(download_dir, 'info.json'), 'r') as f:
            metadata = json.load(f)
    except:
        pass
    
    # Find video file
    video_files = [f for f in os.listdir(download_dir) if f.endswith('.mp4')]
    if not video_files:
        return "Video file not found", 404
    
    video_file = video_files[0]
    video_path = os.path.join(download_dir, video_file)
    
    # Create download filename
    title = metadata.get('title', 'instagram_reel')
    safe_title = re.sub(r'[^\w\-_\. ]', '', title)
    safe_title = safe_title.replace(' ', '_')
    
    download_filename = f"{safe_title}.mp4"
    
    return send_file(
        video_path,
        mimetype='video/mp4',
        as_attachment=True,
        download_name=download_filename
    )

if __name__ == '__main__':
    app.run(debug=True)