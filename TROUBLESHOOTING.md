# 🛠️ Troubleshooting Guide - Amazon Scraping Tool

## 🚨 Common Installation Issues

### Issue 1: NumPy Compilation Error (C++ Compiler Missing)

**Error Message:**
```
ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc'], ['clang'], ['clang-cl'], ['pgcc']]
Failed to activate VS environment: Could not find C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe
```

**Cause:** Windows doesn't have C++ build tools needed to compile NumPy from source.

**Solutions (in order of preference):**

#### Solution 1: Use Windows Safe Setup (Recommended)
```cmd
# Use the safe setup script instead
SETUP_WINDOWS_SAFE.bat
```

#### Solution 2: Install Visual Studio Build Tools
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "C++ build tools" workload
3. Restart computer
4. Run `SETUP.bat` again

#### Solution 3: Use Compatible Requirements
```cmd
# Use older, compatible package versions
pip install -r requirements_compatible.txt
```

#### Solution 4: Use Pre-compiled Wheels Only
```cmd
pip install --only-binary=all numpy pandas openpyxl playwright
```

### Issue 2: Python Version Compatibility

**Error Message:**
```
Python version too old/new
```

**Solution:**
- **Recommended:** Python 3.9, 3.10, or 3.11
- **Avoid:** Python 3.12+ (compatibility issues with some packages)
- **Minimum:** Python 3.8

**Download:** https://python.org/downloads/

### Issue 3: Playwright Browser Installation Failed

**Error Message:**
```
Failed to install Playwright browsers
```

**Solutions:**
```cmd
# Manual browser installation
python -m playwright install chromium

# If that fails, try with dependencies
python -m playwright install-deps
python -m playwright install chromium

# Alternative: Use system Chrome
python -m playwright install chromium --with-deps
```

### Issue 4: Permission Denied Errors

**Error Message:**
```
Permission denied / Access denied
```

**Solutions:**
1. **Run as Administrator:**
   - Right-click setup script
   - Select "Run as administrator"

2. **Check antivirus:**
   - Temporarily disable antivirus
   - Add installation folder to exclusions

3. **Use different location:**
   ```cmd
   # Install to user directory instead
   mkdir %USERPROFILE%\AmazonTool
   cd %USERPROFILE%\AmazonTool
   git clone https://github.com/ajcoder326/amazonscarping-tool.git .
   ```

### Issue 5: Git Not Found

**Error Message:**
```
'git' is not recognized as an internal or external command
```

**Solutions:**
1. **Install Git:**
   - Download: https://git-scm.com/download/win
   - During installation, select "Add to PATH"

2. **Use Manual Download:**
   - Go to: https://github.com/ajcoder326/amazonscarping-tool
   - Click "Code" → "Download ZIP"
   - Extract and run setup

### Issue 6: PyQt5 Installation Failed

**Error Message:**
```
Failed to install PyQt5
```

**Impact:** GUI traffic generator won't work (CLI still works)

**Solutions:**
```cmd
# Try alternative PyQt5 installation
pip install PyQt5-Qt5==5.15.2
pip install PyQt5==5.15.7

# Or use PySide2 as alternative
pip install PySide2
```

### Issue 7: Cookies Not Working

**Symptoms:**
- "Suppressed Detail Page Removed" for live products
- Frequent captchas or blocks

**Solutions:**
1. **Re-export cookies:**
   - Login to Amazon.in in fresh browser
   - Export cookies using browser extension
   - Replace `cookies/amazon_cookies.json`

2. **Check cookie format:**
   ```json
   [
     {
       "domain": ".amazon.in",
       "name": "session-id",
       "value": "your-session-id",
       "path": "/",
       "secure": true
     }
   ]
   ```

3. **Test cookies:**
   ```cmd
   python test_cookies.py
   ```

### Issue 8: Proxy Connection Errors

**Error Message:**
```
Proxy connection failed / Timeout
```

**Solutions:**
1. **Test proxies:**
   ```cmd
   python test_proxy.py
   ```

2. **Check proxy format:**
   ```
   # Authenticated
   ip:port:username:password
   
   # Non-authenticated
   ip:port
   ```

3. **Use backup proxies:**
   - Configure both primary and backup proxy files
   - Tool will automatically fallback

### Issue 9: Memory/Performance Issues

**Symptoms:**
- System becomes slow
- Browser crashes
- Out of memory errors

**Solutions:**
1. **Reduce parallel browsers:**
   ```python
   # Edit main_linux.py
   MAX_BROWSERS = 15  # Reduce from 30
   ```

2. **Increase virtual memory:**
   - Windows Settings → System → About → Advanced system settings
   - Performance → Settings → Advanced → Virtual memory

3. **Close other applications:**
   - Free up RAM before running tool

### Issue 10: Firewall/Antivirus Blocking

**Symptoms:**
- Downloads fail
- Browser automation blocked
- Network timeouts

**Solutions:**
1. **Add to firewall exceptions:**
   - Python.exe
   - Chromium browser
   - Installation directory

2. **Temporarily disable antivirus:**
   - During installation only
   - Re-enable after setup

## 🔧 Advanced Troubleshooting

### Debug Mode
```cmd
# Enable verbose logging
set PYTHONPATH=%CD%
python -u audit-new-exe/runner_linux.py -file "test.xlsx" -limit 5
```

### Clean Installation
```cmd
# Remove everything and start fresh
rmdir /s /q venv
rmdir /s /q __pycache__
del *.pyc /s
SETUP_WINDOWS_SAFE.bat
```

### Check System Requirements
```cmd
# Verify system specs
systeminfo | findstr "Total Physical Memory"
python --version
pip --version
```

### Manual Package Installation
```cmd
# Install packages one by one to identify issues
pip install numpy==1.24.3
pip install pandas==1.5.3
pip install openpyxl==3.1.2
pip install playwright==1.40.0
pip install aiofiles==23.2.1
pip install requests==2.31.0
```

## 📞 Getting Help

### Before Asking for Help:
1. ✅ Try `SETUP_WINDOWS_SAFE.bat` first
2. ✅ Run as Administrator
3. ✅ Check Python version (3.9-3.11 recommended)
4. ✅ Temporarily disable antivirus
5. ✅ Check internet connection

### Information to Provide:
- Windows version
- Python version (`python --version`)
- Full error message
- Steps you tried
- Installation method used

### Where to Get Help:
- GitHub Issues: https://github.com/ajcoder326/amazonscarping-tool/issues
- Check existing issues first
- Provide complete error logs

## 🎯 Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| **C++ Compiler Error** | Use `SETUP_WINDOWS_SAFE.bat` |
| **Permission Denied** | Run as Administrator |
| **Git Not Found** | Download ZIP instead |
| **PyQt5 Failed** | Skip GUI, use CLI mode |
| **Cookies Expired** | Re-export from Amazon.in |
| **Proxy Errors** | Test with `test_proxy.py` |
| **Memory Issues** | Reduce MAX_BROWSERS to 15 |
| **Firewall Block** | Add Python to exceptions |

## ✅ Success Checklist

After troubleshooting, verify:
- [ ] Python 3.9-3.11 installed
- [ ] Virtual environment created
- [ ] All packages installed without errors
- [ ] Playwright browser downloaded
- [ ] Test scripts pass
- [ ] Desktop shortcuts created
- [ ] Sample audit runs successfully

---

**💡 Pro Tip:** Use `SETUP_WINDOWS_SAFE.bat` for most reliable installation on Windows systems!