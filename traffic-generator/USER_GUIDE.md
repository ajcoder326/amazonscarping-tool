# 🚀 Amazon Traffic Simulator - Quick Start Guide for Users

## Download & Setup

### Step 1: Get the Application
You should have received: **Amazon_Traffic_Simulator.exe** (93.1 MB)

### Step 2: No Installation Required!
Simply double-click the EXE file to launch the application

---

## Prepare Your Files

### ASIN File (Excel or CSV)

Create an Excel (.xlsx) or CSV file with your Amazon product ASINs:

**Excel Example:**
```
ASIN
B0DK317TDD
B0CYPLPZRQ
B0CW5YN5HX
B0CR28WKYD
```

**CSV Example:**
```
ASIN
B0DK317TDD
B0CYPLPZRQ
B0CW5YN5HX
```

**Important**: Column must be named **ASIN**

### Cookie File (JSON)

You need to export your Amazon cookies as JSON file.

#### How to Export Cookies:

**For Chrome/Edge Users:**
1. Go to amazon.in and login to your account
2. Download "EditThisCookie" extension
3. Click the extension icon
4. Click "Export" 
5. Paste content into text editor
6. Save as `cookies.json`

**For Firefox Users:**
1. Go to amazon.in
2. Press F12 to open Developer Tools
3. Go to Storage → Cookies → amazon.in
4. Right-click and copy cookies
5. Format as JSON (or use Firefox Cookie Export extension)
6. Save as `cookies.json`

**Cookie File Format:**
```json
{
  "cookies": [
    {
      "domain": ".amazon.in",
      "name": "session-id",
      "value": "YOUR_SESSION_ID",
      "path": "/",
      "secure": true
    },
    {
      "domain": ".amazon.in",
      "name": "session-token",
      "value": "YOUR_SESSION_TOKEN",
      "path": "/",
      "secure": true
    }
  ]
}
```

---

## Run the Application

### Step 1: Launch
Double-click `Amazon_Traffic_Simulator.exe`

A window will appear:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Amazon Traffic Simulator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 FILE SELECTION
  ASIN File:     [Browse ASIN File]
  Cookie File:   [Browse Cookie File]

⚙️ SETTINGS (Optional)
  Limit ASINs:   [0]  (0 = All)
  Delay Seconds: [0]  (0 = Random)

[▶️ START SIMULATION]  [🔄 Clear All]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 2: Select Files

1. **Click "Browse ASIN File"**
   - Find your Excel or CSV file with ASINs
   - Select it

2. **Click "Browse Cookie File"**
   - Find your cookies.json file
   - Select it

### Step 3: Configure Settings (Optional)

**Limit ASINs** (Optional)
- Enter 0 to process all ASINs
- Enter a number to limit (e.g., 10 = first 10 ASINs)

**Delay Between ASINs** (Optional)
- Enter 0 for random delays (10-30 seconds)
- Enter a number for fixed delay (e.g., 20 = 20 seconds)

### Step 4: Start!

Click **▶️ START SIMULATION**

---

## Watch It Work

Once you click START:

✅ **Browser opens automatically**
✅ **Real-time log shows what's happening**
✅ **Progress bar tracks completion**
✅ **Each ASIN is processed in order**

### What You'll See:

```
======================================================================
🚀 AMAZON TRAFFIC SIMULATOR - STARTING
======================================================================
📊 Total ASINs to simulate: 100
🕐 Estimated time: ~42 minutes
🍪 Using 7 cookies for authentication
======================================================================

[1/100] Processing ASIN: B0DK317TDD
======================================================================
🎯 Simulating user visit for ASIN: B0DK317TDD
======================================================================
📱 Step 1: Visiting Amazon homepage...
✅ Homepage visited
📦 Step 2: Opening product page...
✅ Product page loaded: https://www.amazon.in/dp/B0DK317TDD
🍪 Cookies loaded: 7 cookies added
🖱️  Step 3: Simulating mouse movements...
📜 Step 4: Scrolling through product details...
🖼️  Step 5: Viewing product images...
📋 Step 6: Reading product information...
🛒 Step 7: Looking for Buy Now button...
✅ Clicking Buy Now button...
✅ Buy Now clicked!
⏱️  Step 8: Staying on page for realistic timing...
✅ Traffic simulation completed for B0DK317TDD
⏸️  Waiting 15.3s before next ASIN...
```

---

## Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| **"File not found" error** | Use full path (C:\Users\Name\...) not just filename |
| **"Invalid JSON" error** | Check if cookies.json is valid JSON - use jsonlint.com |
| **Cookies expired** | Export fresh cookies from Amazon - login again first |
| **Browser not opening** | Check internet connection, disable firewall temporarily |
| **Very slow** | Normal - automation is slow to mimic human behavior |
| **Simulation stops** | Check console output for specific error message |

---

## What Happens

For each ASIN in your file:

1. **Optionally visits homepage** (30% chance)
2. **Opens product page** on Amazon
3. **Simulates human behavior**:
   - Random mouse movements
   - Scrolling through page
   - Reading product details
   - Viewing images
4. **Clicks "Buy Now"** button
5. **Waits** on the page briefly (realistic timing)
6. **Moves to next ASIN** after delay

---

## Estimated Times

| Number of ASINs | Estimated Time |
|-----------------|----------------|
| 10 | ~4 minutes |
| 50 | ~21 minutes |
| 100 | ~42 minutes |
| 500 | ~3.5 hours |

*Times vary based on delay setting and internet speed*

---

## Important Notes

⚠️ **Cookies**: Keep your cookies secure and don't share them  
⚠️ **Amazon Account**: Use cookies from your own verified account  
⚠️ **Delays**: Use appropriate delays to avoid rate limiting  
⚠️ **Monitoring**: Keep an eye on the simulation (check periodically)  
⚠️ **Errors**: If errors occur, check the output log for details  

---

## Advanced Settings

### Limit ASINs
- **0** = Process all ASINs in file (default)
- **5** = Process only first 5 ASINs
- **100** = Process first 100 ASINs

### Delay Between ASINs
- **0** = Random 10-30 seconds between ASINs (default)
- **15** = Fixed 15 seconds between ASINs
- **30** = Fixed 30 seconds between ASINs

---

## ✅ Requirements Checklist

Before running:
- [ ] Windows 7 or later (Windows 10/11 recommended)
- [ ] At least 4GB RAM
- [ ] 100MB+ free disk space
- [ ] Active internet connection
- [ ] Excel or CSV file with ASINs
- [ ] JSON file with Amazon cookies
- [ ] Amazon cookies not expired

---

## Support & Troubleshooting

### Check the Output Log
- Always check the green text log for error details
- It shows exactly what went wrong
- Helpful for debugging issues

### Validate Files
1. **ASIN File**:
   - Open in Excel/Notepad
   - Check column header is "ASIN"
   - Verify ASINs are valid

2. **Cookie File**:
   - Validate JSON at: jsonlint.com
   - Check file is not corrupted
   - Ensure cookies are not expired

### Test with Few ASINs First
- Start with limit set to 5
- Make sure everything works
- Then run full simulation

---

## When It's Done

Once simulation completes:
- ✅ Success message appears
- ✅ Progress bar reaches 100%
- ✅ Browser windows close
- ✅ Application ready for new run

---

## 🎯 Ready to Go!

You now have everything you need:
1. ✅ Application (EXE)
2. ✅ ASIN file (Excel/CSV)
3. ✅ Cookie file (JSON)
4. ✅ Instructions (this guide)

**Double-click the EXE and start!** 🚀

---

## Questions or Issues?

Check these resources:
- Output log (green text during execution)
- This guide (FAQ section above)
- Cookie export guides (links provided)
- Error messages (read carefully)

**Good luck!** 🎉
