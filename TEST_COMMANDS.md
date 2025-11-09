# Quick Test Commands

Copy-paste commands to quickly test each application.

## 🧪 LinkedIn Scraper Tests

```bash
# Navigate and activate
cd LinkedInScraper
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt

# Test scrape (20 profiles)
python scraper.py --urls urls.txt --output test_output.csv

# Verify output
head -5 test_output.csv
wc -l test_output.csv  # Should show 21 lines (20 + header)

# Cleanup
rm test_output.csv
deactivate
cd ..
```

## 🤙 Autodialer Tests

```bash
# Navigate and activate
cd Autodialer
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt

# Start server
python app.py &
sleep 3

# Test health endpoint
curl http://localhost:5000/health

# Test upload (paste numbers)
curl -X POST http://localhost:5000/upload-numbers \
  -F "numbers=18001234567
18001234568
18001234569"

# Test AI command endpoint
curl -X POST http://localhost:5000/ai-command \
  -H "Content-Type: application/json" \
  -d '{"command":"call 18001234567 and play Hello from AeroLeads"}'

# Get logs
curl http://localhost:5000/logs

# Stop server
fg
# Press Ctrl+C

deactivate
cd ..
```

### Browser Test (Autodialer)
1. Open http://localhost:5000
2. Paste these numbers:
   ```
   18001234567
   18001234568
   18001234569
   ```
3. Click "Upload Numbers"
4. Try AI command: `call 18001234567 and play 'Hello from AeroLeads'`
5. Check call logs table

## ✍️ Blog Generator Tests

```bash
# Navigate and activate
cd BlogGenerator
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt

# Start server
python app.py &
sleep 3

# Test health endpoint
curl http://localhost:5001/health

# Test blog generation
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "titles": ["Getting Started with Python", "Introduction to Docker"],
    "tone": "professional",
    "word_count": 800
  }'

# List blogs
curl http://localhost:5001/blog

# Stop server
fg
# Press Ctrl+C

deactivate
cd ..
```

### Browser Test (Blog Generator)
1. Open http://localhost:5001
2. Enter these titles (one per line):
   ```
   Getting Started with Python FastAPI
   Building Scalable Microservices
   Introduction to Docker Containers
   ```
3. Select tone: Professional
4. Word count: 800
5. Click "Generate Blogs"
6. View all blogs at: http://localhost:5001/blog

## 🔍 Quick Verification

### Check if Python is correct version
```bash
python3 --version
# Should be 3.10 or higher
```

### Check if venv is activated
```bash
which python
# Should show path to venv, not system python
# Example: /path/to/aeroleads-ai-assignment/Autodialer/venv/bin/python
```

### Check if packages installed correctly
```bash
pip list | grep Flask
pip list | grep selenium
pip list | grep twilio
pip list | grep openai
```

### Check environment variables
```bash
# Show all env vars (be careful with sensitive data)
cat .env

# Check specific variable is set
echo $OPENAI_API_KEY
echo $TWILIO_ACCOUNT_SID
```

## 🚨 Common Issues Quick Fix

### ModuleNotFoundError
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
PORT=5002 python app.py
```

### ChromeDriver not found
```bash
# macOS with Homebrew
brew install chromedriver

# Or let script auto-download (should work automatically)
```

### Permission denied (ChromeDriver)
```bash
# macOS
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
```

## 📊 Complete Test Suite

Run all tests in sequence:

```bash
#!/bin/bash

echo "=== Testing LinkedIn Scraper ==="
cd LinkedInScraper
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python scraper.py --urls urls.txt --output test.csv --headless
echo "✓ Scraper test complete (check test.csv)"
deactivate
cd ..

echo ""
echo "=== Testing Autodialer ==="
cd Autodialer
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python app.py &
APP_PID=$!
sleep 5
curl -s http://localhost:5000/health
echo "✓ Autodialer test complete"
kill $APP_PID
deactivate
cd ..

echo ""
echo "=== Testing Blog Generator ==="
cd BlogGenerator
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python app.py &
APP_PID=$!
sleep 5
curl -s http://localhost:5001/health
echo "✓ Blog Generator test complete"
kill $APP_PID
deactivate
cd ..

echo ""
echo "=== All Tests Complete ==="
```

Save as `run_all_tests.sh` and execute:
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

## 🎬 Video Demo Test Sequence

Perfect sequence for screen recording:

### 1. LinkedIn Scraper (1-2 min)
```bash
cd LinkedInScraper
source venv/bin/activate
python scraper.py --urls urls.txt --output demo_profiles.csv
# Show: terminal output, then open CSV in Excel/viewer
```

### 2. Autodialer (2-3 min)
```bash
cd Autodialer
source venv/bin/activate
python app.py
# Browser: http://localhost:5000
# Demo: Upload numbers, AI command, show logs
```

### 3. Blog Generator (2-3 min)
```bash
cd BlogGenerator
source venv/bin/activate
python app.py
# Browser: http://localhost:5001
# Demo: Generate 3 blogs, view list, open one article
```

## ✅ Pre-Submission Checklist

Run these before submitting:

```bash
# 1. Check all files exist
ls -la LinkedInScraper/scraper.py
ls -la Autodialer/app.py
ls -la BlogGenerator/app.py
ls -la README.md
ls -la env.example

# 2. Check no sensitive data committed
grep -r "sk-" . --exclude-dir=venv --exclude-dir=.git
grep -r "AC[a-z0-9]" . --exclude-dir=venv --exclude-dir=.git

# 3. Check .gitignore working
git status | grep ".env"  # Should NOT appear

# 4. Test all three apps work
# (run test commands above)

# 5. Record video

# 6. Deploy and get URLs

# 7. Update README with:
#    - Video link
#    - Deployment URLs
#    - Personal info (salary, notice period)
```

## 🎯 Quick Reference

| App | Port | Health Check URL |
|-----|------|------------------|
| Autodialer | 5000 | http://localhost:5000/health |
| Blog Generator | 5001 | http://localhost:5001/health |

| Action | Command |
|--------|---------|
| Activate venv | `source venv/bin/activate` |
| Deactivate venv | `deactivate` |
| Install deps | `pip install -r requirements.txt` |
| Run Flask | `python app.py` |
| Stop Flask | `Ctrl+C` |

---

**Pro Tip:** Keep these commands handy while recording your video demo!

