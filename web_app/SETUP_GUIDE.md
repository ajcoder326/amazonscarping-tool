# Amazon ASIN Audit Tool - Web Server Setup Guide

## 🚀 Quick Start

### Step 1: Install Dependencies
```powershell
cd "d:\audit updated v1 backup working\audit updated v1"
pip install flask werkzeug pandas openpyxl playwright aiofiles
playwright install chromium
```

### Step 2: Start the Server
**Option A: Just the local server**
```powershell
cd "d:\audit updated v1 backup working\audit updated v1"
python web_app\app.py
```
Server will run at: `http://localhost:5000`

**Option B: Double-click the batch file**
- Run `web_app\run_server.bat`

---

## 🌐 Expose to Internet with Ngrok

### Step 1: Install Ngrok
1. Download from: https://ngrok.com/download
2. Extract `ngrok.exe` to a folder in your PATH
3. Sign up for free account at ngrok.com
4. Get your auth token from dashboard
5. Run: `ngrok config add-authtoken YOUR_AUTH_TOKEN`

### Step 2: Start Ngrok Tunnel
**Option A: Run both server and ngrok**
```powershell
# Terminal 1 - Start Flask server
cd "d:\audit updated v1 backup working\audit updated v1"
python web_app\app.py

# Terminal 2 - Start ngrok
ngrok http 5000
```

**Option B: Use the batch file**
- Run `web_app\run_with_ngrok.bat`

### Step 3: Share the URL
Ngrok will show something like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:5000
```
Share the `https://abc123.ngrok.io` URL with your users!

---

## 🔧 Using a Custom Ngrok Domain

If you have a paid ngrok account with a reserved domain:

```powershell
ngrok http 5000 --domain=your-domain.ngrok.io
```

Or with a custom subdomain:
```powershell
ngrok http 5000 --subdomain=amazon-audit
```

---

## 📊 Server Configuration

Edit `web_app\app.py` to change these settings:

```python
MAX_ASINS = 1000          # Maximum ASINs per upload
MAX_CONCURRENT_JOBS = 3   # Maximum simultaneous audits
```

---

## 🔒 Security Considerations

1. **Rate Limiting**: Server allows max 3 concurrent jobs
2. **File Size Limit**: 16MB max upload
3. **ASIN Validation**: Only valid 10-character ASINs processed
4. **Auto Cleanup**: Consider adding cleanup for old files

---

## 📁 Folder Structure

```
web_app/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Web interface
├── uploads/            # User uploaded files (auto-created)
├── outputs/            # Audit results (auto-created)
├── run_server.bat      # Start server only
├── run_with_ngrok.bat  # Start server + ngrok
└── SETUP_GUIDE.md      # This file
```

---

## 🔄 How It Works

1. **User uploads** ASIN file (CSV/Excel)
2. **Server validates** file and extracts ASINs (max 1000)
3. **Audit job starts** in background with 10 parallel browsers
4. **Progress updates** sent to browser via polling
5. **User downloads** CSV results when complete

---

## ⚠️ Troubleshooting

### "Playwright not found" error
```powershell
pip install playwright
playwright install chromium
```

### "Port 5000 already in use"
Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=8080, ...)
```
Then: `ngrok http 8080`

### Ngrok connection issues
1. Check your internet connection
2. Verify auth token: `ngrok config check`
3. Try: `ngrok http 5000 --log=stdout`

### Server crashes with many users
Reduce concurrent jobs:
```python
MAX_CONCURRENT_JOBS = 2
```

---

## 📈 Performance Tips

1. **Headless mode**: Already enabled for server efficiency
2. **10 parallel browsers**: Optimized for server load
3. **Image blocking**: Enabled for faster processing
4. **Rate limiting**: 2-4 second delays to avoid Amazon blocks

---

## 💡 Tips for Users

Share these instructions with your users:

1. Prepare a CSV or Excel file with an "ASIN" column
2. Maximum 1000 ASINs per file
3. Go to the shared ngrok URL
4. Upload your file
5. Wait for processing (progress shown on screen)
6. Download the results CSV when complete

---

## 🔌 API Endpoints

For developers who want to integrate:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/upload` | POST | Upload ASIN file |
| `/status/<job_id>` | GET | Get job status |
| `/download/<job_id>` | GET | Download results |
| `/health` | GET | Server health check |
| `/jobs` | GET | List all jobs (admin) |

---

## Need Help?

1. Check the console output for error messages
2. Ensure Playwright browsers are installed
3. Verify internet connection
4. Check if Amazon is blocking (try with different IP/proxy)
