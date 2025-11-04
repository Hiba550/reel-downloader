# 📥 Instagram Reel Downloader

A beautiful, modern web app to download Instagram Reels with PWA support and share target functionality.

## ✨ Features

- 📱 **Progressive Web App (PWA)** - Install on mobile devices
- 🔗 **Share Target Support** - Share Reels directly from Instagram or other apps
- 🎨 **Beautiful UI** - Modern gradient design with dark mode
- 📥 **One-Click Downloads** - Quick and easy Reel downloads
- 🌙 **Dark Mode** - Eye-friendly dark theme
- 📲 **Mobile Optimized** - Perfect responsive design
- 🚀 **Fast & Secure** - No tracking, no ads

## 🚀 Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open in browser:
```
http://localhost:5000
```

## 📱 PWA Features

### Install as Mobile App
- **Android**: Tap menu → "Install app"
- **iOS**: Share button → "Add to Home Screen"

### Share Instagram Reels to the App
1. Find a Reel in Instagram
2. Tap the Share button
3. Select "Reel Downloader"
4. The app opens with the link ready to download!

### Share Overlay
When you share a link to the app, a beautiful overlay appears with options to:
- 📥 Download the Reel immediately
- 📋 Copy the link
- ❌ Ignore and browse normally

## 🛠️ Technical Details

### PWA Configuration
- `static/manifest.json` - App manifest with share target
- `static/sw.js` - Service worker for offline support
- Share target endpoint at `/share-target`

### Requirements
- Python 3.7+
- Flask
- instaloader

## 📄 License

See LICENSE file for details.

## 💝 Credits

Made with ❤️ by Hiba  
Powered by Instaloader

---

**Note**: For PWA features to work properly, the app must be served over HTTPS. Use ngrok or deploy to a server with SSL for testing.