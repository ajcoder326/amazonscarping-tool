# 🚀 Deployment Guide - Amazon Scraping Tool

## Quick Deployment on New PC

### Method 1: One-Click Setup (Recommended)

1. **Download the tool**:
   ```cmd
   git clone https://github.com/ajcoder326/amazonscarping-tool.git
   cd amazonscarping-tool
   ```

2. **Run setup as Administrator**:
   - Right-click `SETUP.bat`
   - Select "Run as administrator"
   - Follow the on-screen instructions

3. **Done!** Tool is ready to use.

### Method 2: Manual Setup

1. **Prerequisites**:
   - Install Python 3.10+ from [python.org](https://python.org/downloads)
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Clone and setup**:
   ```cmd
   git clone https://github.com/ajcoder326/amazonscarping-tool.git
   cd amazonscarping-tool
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   pip install playwright-stealth PyQt5
   playwright install chromium
   ```

## 📋 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 7+ (64-bit recommended) |
| **Python** | 3.10 or higher |
| **RAM** | 4GB+ (8GB+ for 30 parallel browsers) |
| **Storage** | 500MB+ free space |
| **Internet** | Stable broadband connection |
| **Browser** | Chromium (auto-installed by Playwright) |

## 🎯 Quick Start After Setup

### 1. Product Auditing
```cmd
# Easy way
run_audit.bat

# Manual way
python audit-new-exe/runner_linux.py -file "your_asins.xlsx"
```

### 2. Traffic Generation
```cmd
# GUI Mode (Recommended)
run_traffic_gui.bat

# CLI Mode
cd traffic-generator
python run_traffic.py -file "asins.xlsx" -limit 10
```

### 3. Test Installation
```cmd
test_setup.bat
```

## 📁 Directory Structure After Setup

```
amazonscarping-tool/
├── venv/                   # Python virtual environment
├── audit-new-exe/          # Main audit engine
├── traffic-generator/      # Traffic simulation
├── features/               # Data extractors
├── utils/                  # Helper utilities
├── cookies/                # Authentication files
├── run_audit.bat          # Quick audit launcher
├── run_traffic_gui.bat    # Quick traffic GUI launcher
├── test_setup.bat         # Installation tester
└── SETUP.bat              # Main setup script
```

## 🍪 Cookie Configuration

1. **Export cookies from Amazon.in**:
   - Install browser extension (Cookie Editor, EditThisCookie)
   - Login to Amazon.in
   - Export cookies as JSON
   - Save to `cookies/amazon_cookies.json`

2. **Test cookies**:
   ```cmd
   python test_cookies.py
   ```

## 🌐 Proxy Configuration (Optional)

1. **Create proxy file**:
   ```
   # Format: ip:port:username:password
   proxy1.example.com:8080:user1:pass1
   proxy2.example.com:8080:user2:pass2
   ```

2. **Test proxies**:
   ```cmd
   python test_proxy.py
   ```

## 🔧 Configuration Options

### Batch Processing Settings
Edit `audit-new-exe/runner_linux.py`:
```python
# Default settings
BATCH_SIZE = 5000        # ASINs per batch
COOLDOWN = 600          # Seconds between batches (10 min)
MAX_BROWSERS = 30       # Parallel browsers
```

### Traffic Generation Settings
Edit `traffic-generator/traffic_simulator.py`:
```python
# Timing settings
slow_mo=50              # Slow motion delay (ms)
DELAY_BETWEEN_ASINS = 20 # Seconds between ASINs
```

## 📊 Performance Optimization

### For High-Volume Processing
1. **Increase RAM**: 8GB+ recommended for 30 browsers
2. **Use SSD**: Faster I/O for large CSV files
3. **Stable Internet**: Avoid connection drops
4. **Close Other Apps**: Free up system resources

### For Stealth Mode
1. **Use Proxies**: Rotate IP addresses
2. **Fresh Cookies**: Update every 24-48 hours
3. **Longer Delays**: Increase cooldown periods
4. **Smaller Batches**: Reduce batch sizes

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Python not found** | Install Python 3.10+ and add to PATH |
| **Playwright browser missing** | Run `playwright install chromium` |
| **Permission denied** | Run setup as Administrator |
| **Cookies expired** | Re-export cookies from Amazon.in |
| **Proxy errors** | Test proxies with `test_proxy.py` |
| **Out of memory** | Reduce MAX_BROWSERS or increase RAM |

### Debug Mode
```cmd
# Enable verbose logging
set PYTHONPATH=%CD%
python -u audit-new-exe/runner_linux.py -file "test.xlsx" -limit 10
```

## 🔒 Security Best Practices

1. **Rate Limiting**: Use default cooldown periods
2. **Proxy Rotation**: Distribute requests across IPs
3. **Cookie Management**: Keep cookies fresh and secure
4. **Respectful Scraping**: Follow robots.txt guidelines
5. **Legal Compliance**: Ensure compliance with local laws

## 📈 Scaling for Production

### Single Machine
- **Max Browsers**: 30-50 (depending on RAM)
- **Batch Size**: 5000-10000 ASINs
- **Daily Capacity**: 50,000-100,000 ASINs

### Multi-Machine Setup
1. Deploy tool on multiple servers
2. Distribute ASIN lists across machines
3. Use different proxy pools per machine
4. Coordinate batch timing to avoid conflicts

## 🎯 Usage Examples

### Small Scale Testing (100 ASINs)
```cmd
python audit-new-exe/runner_linux.py -file "test.xlsx" -limit 100 -batch 50 -wait 60
```

### Medium Scale (10,000 ASINs)
```cmd
python audit-new-exe/runner_linux.py -file "medium.xlsx" -batch 2000 -wait 300
```

### Large Scale (50,000+ ASINs)
```cmd
python audit-new-exe/runner_linux.py -file "large.xlsx" -batch 5000 -wait 600
```

## 📞 Support & Updates

### Getting Help
1. Check this deployment guide
2. Review README.md for detailed usage
3. Test with `test_setup.bat`
4. Create GitHub issue for bugs

### Updating the Tool
```cmd
git pull origin main
pip install -r requirements.txt --upgrade
playwright install chromium
```

## 🎉 Success Checklist

After deployment, verify:
- [ ] Python 3.10+ installed and in PATH
- [ ] Virtual environment created and activated
- [ ] All packages installed successfully
- [ ] Playwright browser downloaded
- [ ] Quick start scripts created
- [ ] Test scripts pass
- [ ] Output directory created
- [ ] Cookies configured (optional)
- [ ] Proxies configured (optional)

---

**🎯 You're ready to start scraping!** 

Use `run_audit.bat` for product auditing or `run_traffic_gui.bat` for traffic generation.