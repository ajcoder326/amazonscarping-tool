# 🚀 Amazon Audit Tool - Server Deployment Guide

This guide explains how to deploy the Amazon Audit Tool on a remote server for production use.

---

## 📋 Prerequisites

- A Linux server (Ubuntu 20.04/22.04 recommended) or Windows Server
- Minimum 4GB RAM, 2 CPU cores
- Python 3.10+ installed
- Root/sudo access

---

## 🐧 Option 1: Deploy on Linux Server (Ubuntu/Debian)

### Step 1: Connect to Your Server

```bash
ssh user@your-server-ip
```

### Step 2: Update System & Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx
```

### Step 3: Upload Project Files

**Option A: Using SCP (from your local machine)**
```bash
scp -r "D:\audit updated v1 backup working\audit updated v1" user@your-server-ip:/home/user/
```

**Option B: Using Git (if you have a repo)**
```bash
cd /home/user
git clone https://your-repo-url.git audit-tool
```

### Step 4: Set Up Python Environment

```bash
cd /home/user/audit-tool
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask playwright openpyxl pandas gunicorn
playwright install chromium
playwright install-deps
```

### Step 5: Test the App

```bash
cd /home/user/audit-tool
export PYTHONPATH=/home/user/audit-tool
python web_app/app.py
```

Visit `http://your-server-ip:5000` to verify it works.

### Step 6: Set Up Gunicorn (Production Server)

Create a Gunicorn config file:

```bash
nano /home/user/audit-tool/gunicorn_config.py
```

Add this content:
```python
bind = "0.0.0.0:5000"
workers = 4
threads = 2
timeout = 300
keepalive = 5
errorlog = "/home/user/audit-tool/logs/error.log"
accesslog = "/home/user/audit-tool/logs/access.log"
```

Create logs directory:
```bash
mkdir -p /home/user/audit-tool/logs
```

### Step 7: Create Systemd Service (Auto-start on Boot)

```bash
sudo nano /etc/systemd/system/audit-tool.service
```

Add this content:
```ini
[Unit]
Description=Amazon Audit Tool Web Server
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/audit-tool
Environment="PYTHONPATH=/home/user/audit-tool"
Environment="PATH=/home/user/audit-tool/venv/bin"
ExecStart=/home/user/audit-tool/venv/bin/gunicorn -c gunicorn_config.py web_app.app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable audit-tool
sudo systemctl start audit-tool
sudo systemctl status audit-tool
```

### Step 8: Set Up Nginx (Reverse Proxy with SSL)

```bash
sudo nano /etc/nginx/sites-available/audit-tool
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
        client_max_body_size 50M;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/audit-tool /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Enable SSL with Let's Encrypt (Free HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

Follow the prompts. Certbot will auto-renew your certificate.

---

## 🪟 Option 2: Deploy on Windows Server

### Step 1: Install Python

Download and install Python 3.10+ from https://python.org

### Step 2: Copy Project Files

Copy the entire `audit updated v1` folder to the server (e.g., `C:\audit-tool`)

### Step 3: Set Up Environment

Open PowerShell as Administrator:

```powershell
cd C:\audit-tool
python -m venv venv
.\venv\Scripts\Activate
pip install flask playwright openpyxl pandas waitress
playwright install chromium
```

### Step 4: Create Startup Script

Create `C:\audit-tool\start_server.bat`:
```batch
@echo off
cd C:\audit-tool
set PYTHONPATH=C:\audit-tool
call venv\Scripts\activate
python -m waitress --host=0.0.0.0 --port=5000 web_app.app:app
```

### Step 5: Run as Windows Service

Install NSSM (Non-Sucking Service Manager):
1. Download from https://nssm.cc/download
2. Extract and run as admin:

```powershell
nssm install AuditTool
```

Configure:
- Path: `C:\audit-tool\venv\Scripts\python.exe`
- Startup directory: `C:\audit-tool`
- Arguments: `-m waitress --host=0.0.0.0 --port=5000 web_app.app:app`
- Environment: `PYTHONPATH=C:\audit-tool`

Start the service:
```powershell
nssm start AuditTool
```

### Step 6: Open Firewall Port

```powershell
New-NetFirewallRule -DisplayName "Audit Tool" -Direction Inbound -Port 5000 -Protocol TCP -Action Allow
```

---

## ☁️ Option 3: Deploy on Cloud Platforms

### AWS EC2

1. Launch Ubuntu 22.04 EC2 instance (t2.medium or larger)
2. Configure Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
3. SSH into instance and follow Linux deployment steps above
4. Use Elastic IP for static address

### Google Cloud Platform (GCP)

1. Create Compute Engine VM (e2-medium or larger, Ubuntu 22.04)
2. Allow HTTP/HTTPS in firewall rules
3. SSH and follow Linux deployment steps
4. Use static external IP

### DigitalOcean

1. Create Droplet (Basic, 2GB RAM, Ubuntu 22.04)
2. SSH and follow Linux deployment steps
3. Add domain in Networking settings

### Vultr / Linode / Hetzner

Same process - create Ubuntu server and follow Linux steps.

---

## 🔧 Configuration Options

### Environment Variables

Create `.env` file in project root:
```env
FLASK_ENV=production
MAX_CONCURRENT_JOBS=5
SECRET_KEY=your-super-secret-key-here
```

### Increase Workers for High Load

Edit `gunicorn_config.py`:
```python
workers = 8  # Increase for more concurrent users
threads = 4
```

### Increase File Upload Size

In Nginx config:
```nginx
client_max_body_size 100M;  # For larger files
```

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Application logs
tail -f /home/user/audit-tool/logs/error.log
tail -f /home/user/audit-tool/logs/access.log

# Service status
sudo systemctl status audit-tool

# Nginx logs
tail -f /var/log/nginx/error.log
```

### Check Service Status

```bash
sudo systemctl status audit-tool
sudo systemctl restart audit-tool
sudo systemctl stop audit-tool
```

---

## 🔒 Security Recommendations

1. **Use HTTPS** - Always enable SSL with Let's Encrypt
2. **Firewall** - Only open necessary ports (80, 443)
3. **Updates** - Keep system and packages updated
4. **Strong Secret Key** - Change the Flask secret key
5. **Rate Limiting** - Add rate limiting in Nginx for DDoS protection:

```nginx
limit_req_zone $binary_remote_addr zone=audit:10m rate=10r/s;

server {
    location / {
        limit_req zone=audit burst=20 nodelay;
        # ... rest of config
    }
}
```

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Playwright Browser Issues
```bash
playwright install-deps chromium
```

### Permission Denied
```bash
sudo chown -R user:user /home/user/audit-tool
chmod +x /home/user/audit-tool/venv/bin/*
```

### Service Won't Start
```bash
sudo journalctl -u audit-tool -f
```

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Start service | `sudo systemctl start audit-tool` |
| Stop service | `sudo systemctl stop audit-tool` |
| Restart service | `sudo systemctl restart audit-tool` |
| View status | `sudo systemctl status audit-tool` |
| View logs | `tail -f /home/user/audit-tool/logs/error.log` |
| Restart Nginx | `sudo systemctl restart nginx` |

---

## ✅ Deployment Checklist

- [ ] Server provisioned with 4GB+ RAM
- [ ] Python 3.10+ installed
- [ ] Project files uploaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Playwright browsers installed
- [ ] Gunicorn/Waitress configured
- [ ] Systemd service enabled
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Tested from external network

---

**Your tool will be accessible at:** `https://your-domain.com`

For questions or issues, check the logs first!
