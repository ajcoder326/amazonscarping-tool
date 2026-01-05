#!/bin/bash
#===============================================================
# Amazon Audit Tool - Automated Linux Server Deployment Script
# Domain: horal-agnes-acetated.ngrok-free.dev (using ngrok)
#===============================================================

set -e  # Exit on any error

echo "============================================================"
echo "🚀 Amazon Audit Tool - Server Deployment"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/home/$USER/audit-tool"
NGROK_DOMAIN="horal-agnes-acetated.ngrok-free.dev"
NGROK_AUTHTOKEN="2xTQsa09A1r16K6rfkQpT87RAw3_5EERz7pZ1qkj9hmXNK2ow"

echo -e "${YELLOW}Step 1: Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${YELLOW}Step 2: Installing dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv curl wget unzip

echo -e "${YELLOW}Step 3: Creating application directory...${NC}"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

echo -e "${YELLOW}Step 4: Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${YELLOW}Step 5: Installing Python packages...${NC}"
pip install --upgrade pip
pip install flask playwright openpyxl pandas gunicorn

echo -e "${YELLOW}Step 6: Installing Playwright browsers...${NC}"
playwright install chromium
playwright install-deps chromium

echo -e "${YELLOW}Step 7: Installing ngrok...${NC}"
if ! command -v ngrok &> /dev/null; then
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install ngrok -y
fi

echo -e "${YELLOW}Step 8: Configuring ngrok authentication...${NC}"
ngrok config add-authtoken $NGROK_AUTHTOKEN

echo -e "${YELLOW}Step 9: Creating Gunicorn config...${NC}"
mkdir -p logs
cat > gunicorn_config.py << 'EOF'
bind = "0.0.0.0:5000"
workers = 4
threads = 2
timeout = 600
keepalive = 5
errorlog = "logs/error.log"
accesslog = "logs/access.log"
capture_output = True
EOF

echo -e "${YELLOW}Step 10: Creating systemd service for the app...${NC}"
sudo tee /etc/systemd/system/audit-tool.service > /dev/null << EOF
[Unit]
Description=Amazon Audit Tool Web Server
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment="PYTHONPATH=$APP_DIR"
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn -c gunicorn_config.py web_app.app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${YELLOW}Step 11: Creating systemd service for ngrok...${NC}"
sudo tee /etc/systemd/system/ngrok-tunnel.service > /dev/null << EOF
[Unit]
Description=ngrok tunnel for Audit Tool
After=network.target audit-tool.service

[Service]
User=$USER
ExecStart=/usr/bin/ngrok http 5000 --domain=$NGROK_DOMAIN
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${YELLOW}Step 12: Creating startup script...${NC}"
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export PYTHONPATH=$(pwd)
gunicorn -c gunicorn_config.py web_app.app:app
EOF
chmod +x start.sh

echo -e "${YELLOW}Step 13: Creating ngrok startup script...${NC}"
cat > start_ngrok.sh << EOF
#!/bin/bash
ngrok http 5000 --domain=$NGROK_DOMAIN
EOF
chmod +x start_ngrok.sh

echo -e "${YELLOW}Step 14: Enabling and starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable audit-tool
sudo systemctl enable ngrok-tunnel

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "📁 Application installed at: ${YELLOW}$APP_DIR${NC}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Copy your project files to $APP_DIR${NC}"
echo "   You need to upload these folders/files:"
echo "   - web_app/"
echo "   - features/"
echo "   - utils/"
echo ""
echo -e "${YELLOW}After copying files, run these commands:${NC}"
echo "   sudo systemctl start audit-tool"
echo "   sudo systemctl start ngrok-tunnel"
echo ""
echo -e "🌐 Your tool will be accessible at:"
echo -e "   ${GREEN}https://$NGROK_DOMAIN${NC}"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "   sudo systemctl status audit-tool    # Check app status"
echo "   sudo systemctl status ngrok-tunnel  # Check ngrok status"
echo "   sudo systemctl restart audit-tool   # Restart app"
echo "   tail -f $APP_DIR/logs/error.log     # View logs"
echo ""
echo "============================================================"
