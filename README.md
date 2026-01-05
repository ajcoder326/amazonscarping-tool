# Amazon Scraping Tool 🚀

A comprehensive Python-based automation tool for Amazon product auditing and traffic generation with advanced anti-detection features.

## 🌟 Features

### 📊 Product Audit System
- **Batch Processing**: Handle 5000+ ASINs per batch with automatic cooldown
- **Parallel Execution**: 30 concurrent browsers for maximum speed
- **Data Extraction**: 15+ product attributes (price, ratings, reviews, BSR, availability, etc.)
- **Anti-Detection**: Stealth mode, randomized user agents, viewport variations
- **Proxy Support**: Authenticated proxy rotation for IP diversity
- **Cookie Authentication**: Amazon session persistence

### 🎯 Traffic Generation
- **Human-like Behavior**: Realistic mouse movements, scrolling, page interactions
- **Buy Now Clicks**: Generate engagement signals
- **GUI Interface**: User-friendly PyQt5 application
- **Visible Browsers**: Headful mode for authentic traffic simulation

### 🛡️ Anti-Detection Features
- Playwright stealth mode
- Canvas fingerprint randomization
- User agent rotation (7 different browsers)
- Viewport randomization (5 different screen sizes)
- Random delays and human-like timing
- Proxy rotation support

## 📋 Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows 7+ (primary target)
- **RAM**: 4GB+ recommended
- **Storage**: 500MB+ free space
- **Internet**: Active connection required

## 🚀 Quick Setup

### Option 1: One-Click Setup (Recommended)
1. Download or clone this repository
2. Run `SETUP.bat` as Administrator
3. Follow the on-screen instructions
4. Tool will be ready to use!

### Option 2: Manual Setup
```cmd
# Clone repository
git clone https://github.com/ajcoder326/amazonscarping-tool.git
cd amazonscarping-tool

# Run setup
SETUP.bat
```

## 📖 Usage

### Product Auditing
```cmd
# Basic usage
run_audit.bat

# With custom file
python audit-new-exe/runner_linux.py -file "your_asins.xlsx" -batch 5000 -wait 600

# Test with limited ASINs
python audit-new-exe/runner_linux.py -file "test.xlsx" -limit 100
```

### Traffic Generation
```cmd
# GUI Mode (Recommended)
cd traffic-generator
python gui_app.py

# CLI Mode
python run_traffic.py -file "asins.xlsx" -limit 10 -delay 20
```

### Web Interface
```cmd
# Start web server
START.bat

# Access via browser at http://localhost:5000
# Or use ngrok public URL
```

## 📊 Performance

- **Speed**: 150-200 ASINs per minute (audit mode)
- **Throughput**: 9,000-12,000 ASINs per hour
- **Parallel Browsers**: 30 concurrent sessions
- **Large Scale**: Handle 35,000+ ASINs in 7-9 hours

## 🍪 Cookie Management

1. Export cookies from Amazon.in using browser extension
2. Save to `cookies/amazon_cookies.json`
3. Test with `python test_cookies.py`
4. Update when cookies expire

## 🌐 Proxy Configuration

Supports both authenticated and non-authenticated proxies:
```
# Authenticated format
ip:port:username:password

# Non-authenticated format  
ip:port
```

## 📁 Project Structure

```
├── audit-new-exe/          # Main audit engine
├── features/               # Product attribute extractors
├── traffic-generator/      # Traffic simulation system
├── utils/                  # Helper utilities
├── web_app/               # Flask web interface
├── cookies/               # Authentication files
├── requirements.txt       # Python dependencies
├── SETUP.bat             # One-click setup script
└── README.md             # This file
```

## 🔧 Configuration

### Batch Settings
- **Batch Size**: 5000 ASINs (configurable)
- **Cooldown**: 10 minutes between batches
- **Parallel Browsers**: 30 (adjustable in main_linux.py)

### Output Location
- Default: `C:\Users\{user}\Documents\Audited_files\`
- Format: `{filename}_{timestamp}.csv`

## 📚 Documentation

- `QUICK_START.txt` - Setup and execution guide
- `traffic-generator/USER_GUIDE.md` - GUI application guide
- `traffic-generator/COOKIES_GUIDE.md` - Cookie export instructions
- `traffic-generator/HEADFULL_BROWSER_SETUP.md` - Browser configuration

## 🛠️ Troubleshooting

### Common Issues
1. **Python not found**: Install Python 3.10+ and add to PATH
2. **Playwright browser missing**: Run `playwright install chromium`
3. **Cookies expired**: Re-export cookies from Amazon.in
4. **Proxy errors**: Test proxies with `python test_proxy.py`

### Performance Optimization
- Close unnecessary applications
- Use SSD storage for better I/O
- Ensure stable internet connection
- Monitor RAM usage with 30 parallel browsers

## 🔒 Security & Ethics

- **Rate Limiting**: Built-in delays and cooldowns
- **Respectful Scraping**: Follows robots.txt guidelines
- **Anti-Detection**: Mimics human behavior patterns
- **Proxy Support**: Distributes requests across IPs

## 📄 License

This project is for educational and research purposes. Please comply with Amazon's Terms of Service and applicable laws.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🎯 Roadmap

- [ ] Support for additional Amazon marketplaces
- [ ] Enhanced proxy management
- [ ] Real-time monitoring dashboard
- [ ] API endpoint for external integration
- [ ] Docker containerization

---

**⚠️ Disclaimer**: This tool is for educational and research purposes. Users are responsible for complying with Amazon's Terms of Service and applicable laws. Use responsibly and ethically.