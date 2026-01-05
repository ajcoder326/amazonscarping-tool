# 📦 Amazon Scraping Tool - Distribution Instructions

## 🎯 Repository Information

**GitHub Repository**: https://github.com/ajcoder326/amazonscarping-tool.git  
**Repository Owner**: ajcoder326  
**Tool Name**: Amazon Scraping Tool  

## 🚀 Installation Methods for New PCs

### Method 1: One-Click Download and Install (Easiest)

**For end users who want the simplest installation:**

1. **Download the installer**:
   ```
   https://raw.githubusercontent.com/ajcoder326/amazonscarping-tool/master/DOWNLOAD_AND_INSTALL.bat
   ```

2. **Run as Administrator**:
   - Right-click `DOWNLOAD_AND_INSTALL.bat`
   - Select "Run as administrator"
   - Follow the prompts

3. **Done!** Tool will be installed with desktop shortcuts.

### Method 2: Direct Repository Clone

**For technical users:**

```cmd
git clone https://github.com/ajcoder326/amazonscarping-tool.git
cd amazonscarping-tool
SETUP.bat
```

### Method 3: Manual Download

**If Git is not available:**

1. Go to: https://github.com/ajcoder326/amazonscarping-tool
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Run `SETUP.bat` as Administrator

## 📋 What Gets Installed

### Core Components
- **Python Virtual Environment** (`venv/`)
- **All Required Packages** (Playwright, Pandas, etc.)
- **Chromium Browser** (for automation)
- **Feature Extractors** (15+ product attributes)
- **Traffic Generator** (GUI and CLI)
- **Web Interface** (Flask app with ngrok)

### Desktop Shortcuts Created
- **Amazon Audit Tool** - Product data extraction
- **Amazon Traffic Generator** - User behavior simulation
- **Test Amazon Tool** - Installation verification

### Directory Structure
```
C:\AmazonScrapingTool\          # Default installation
├── venv\                       # Python environment
├── audit-new-exe\              # Main audit engine
├── traffic-generator\          # Traffic simulation
├── features\                   # Data extractors
├── utils\                      # Helper utilities
├── cookies\                    # Authentication
├── run_audit.bat              # Quick launchers
├── run_traffic_gui.bat        
└── test_setup.bat             
```

## 🔧 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 7+ (64-bit recommended) |
| **Python** | 3.10+ (auto-installed if missing) |
| **RAM** | 4GB+ (8GB+ for optimal performance) |
| **Storage** | 500MB+ free space |
| **Internet** | Stable broadband connection |

## 📊 Performance Specifications

### Audit System
- **Speed**: 150-200 ASINs per minute
- **Parallel Browsers**: 30 concurrent sessions
- **Batch Size**: 5000 ASINs (configurable)
- **Cooldown**: 10 minutes between batches
- **Daily Capacity**: 50,000-100,000 ASINs

### Traffic Generator
- **Speed**: 20-30 seconds per ASIN
- **Behavior**: Human-like mouse movements, scrolling
- **Engagement**: Buy Now button clicks
- **Stealth**: Anti-detection measures

## 🛠️ Maintenance & Updates

### Update Existing Installation
```cmd
# Navigate to installation directory
cd C:\AmazonScrapingTool
UPDATE_TOOL.bat
```

### Manual Update
```cmd
git pull origin master
pip install -r requirements.txt --upgrade
playwright install chromium
```

## 📚 Documentation Included

- **README.md** - Complete usage guide
- **DEPLOYMENT_GUIDE.md** - Detailed setup instructions
- **QUICK_START.txt** - Quick reference
- **COOKIES_GUIDE.md** - Cookie export instructions
- **USER_GUIDE.md** - GUI application guide

## 🔒 Security Features

- **Rate Limiting** - Built-in delays and cooldowns
- **Proxy Support** - IP rotation capabilities
- **Cookie Management** - Session persistence
- **Anti-Detection** - Stealth mode, randomized agents
- **Headful Browsers** - Visible automation for authenticity

## 🎯 Use Cases

### Product Research
- Extract pricing, ratings, reviews
- Monitor competitor products
- Track availability and stock
- Analyze market trends

### Traffic Generation
- Simulate user engagement
- Generate authentic browsing patterns
- Click Buy Now buttons
- Create realistic traffic signals

## 📞 Support & Troubleshooting

### Common Issues
1. **Python not found** → Install Python 3.10+ with PATH
2. **Browser missing** → Run `playwright install chromium`
3. **Permission denied** → Run as Administrator
4. **Cookies expired** → Re-export from Amazon.in

### Getting Help
- Check documentation in installation folder
- Review troubleshooting section in README.md
- Create issue on GitHub repository
- Test with `test_setup.bat`

## 🚀 Quick Start After Installation

### 1. Product Auditing
```cmd
# Double-click desktop shortcut: "Amazon Audit Tool"
# OR manually:
run_audit.bat
```

### 2. Traffic Generation
```cmd
# Double-click desktop shortcut: "Amazon Traffic Generator"
# OR manually:
run_traffic_gui.bat
```

### 3. Test Installation
```cmd
# Double-click desktop shortcut: "Test Amazon Tool"
# OR manually:
test_setup.bat
```

## 📈 Scaling Options

### Single Machine
- Max 30-50 parallel browsers
- 50,000-100,000 ASINs per day
- Requires 8GB+ RAM for optimal performance

### Multi-Machine
- Deploy on multiple servers
- Distribute ASIN lists
- Use different proxy pools
- Coordinate batch timing

## 🎉 Distribution Checklist

Before sharing with users:

- [ ] Repository is public and accessible
- [ ] All installation scripts are tested
- [ ] Documentation is complete and accurate
- [ ] Desktop shortcuts work correctly
- [ ] Sample files are included
- [ ] Troubleshooting guide is comprehensive
- [ ] Update mechanism is functional

---

## 📋 Quick Distribution Summary

**Repository**: https://github.com/ajcoder326/amazonscarping-tool  
**One-Click Installer**: `DOWNLOAD_AND_INSTALL.bat`  
**Manual Setup**: `SETUP.bat`  
**Update Tool**: `UPDATE_TOOL.bat`  

**Installation Time**: 10-15 minutes  
**Default Location**: `C:\AmazonScrapingTool\`  
**Desktop Shortcuts**: 3 shortcuts created  
**Ready to Use**: Immediately after installation  

🚀 **The tool is now ready for distribution and deployment on any Windows PC!**