# 🧪 How to Test All Applications

Complete step-by-step guide to test all three applications locally.

## Prerequisites

1. **Python 3.10+** installed
2. **Chrome browser** installed (for LinkedIn Scraper)
3. **Environment variables** configured in `.env` file

## Quick Setup

```bash
# 1. Copy environment template
cp env.example .env

# 2. Edit .env and add your credentials:
#    - OPENAI_API_KEY (required for Blog Generator)
#    - TWILIO credentials (optional, for Autodialer)
#    - LINKEDIN credentials (optional, for Scraper)
```

---

## 1️⃣ Testing LinkedIn Scraper

### Step 1: Setup
```bash
cd LinkedInScraper

# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Run Scraper
```bash
# Basic test (scrapes 20 profiles)
python scraper.py --urls urls.txt --output profiles.csv

# With login (more data)
python scraper.py --urls urls.txt --output profiles.csv --login

# Headless mode (no browser window)
python scraper.py --urls urls.txt --output profiles.csv --headless
```

### Step 3: Verify Output
```bash
# Check if CSV was created
ls -la profiles.csv

# View first few lines
head -5 profiles.csv

# Count profiles (should be 20 + header = 21 lines)
wc -l profiles.csv
```

### Expected Output
```
2025-11-09 10:30:00 - INFO - Loaded 20 URLs from urls.txt
2025-11-09 10:30:05 - INFO - Chrome WebDriver initialized successfully
2025-11-09 10:30:10 - INFO - Processing profile 1/20
...
==================================================
SCRAPING SUMMARY
==================================================
Total profiles scraped: 20
Output file: profiles.csv
==================================================
```

### Troubleshooting
- **ChromeDriver error**: Script auto-downloads it, or install manually
- **LinkedIn blocking**: Use `--login` flag or reduce scraping speed
- **No data extracted**: Some profiles may have privacy settings

---

## 2️⃣ Testing Autodialer

### Step 1: Setup
```bash
cd Autodialer

# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Start Flask App
```bash
# Run the app
python app.py

# You should see:
# * Running on http://127.0.0.1:5000
```

### Step 3: Test in Browser

1. **Open browser**: http://localhost:5000

2. **Test Upload Numbers**:
   - Click "Upload CSV File" or paste numbers in text area:
     ```
     18001234567
     18001234568
     18001234569
     ```
   - Click "Upload Numbers"
   - Should show: "Successfully loaded X phone numbers"

3. **Test AI Command**:
   - In AI Command box, type:
     ```
     call 18001234567 and play 'Hello from AeroLeads'
     ```
   - Click "Execute AI Command"
   - Should parse and attempt to call (may fail if Twilio not configured)

4. **Test Batch Calling**:
   - Enter message: "Hello, this is a test call"
   - Click "Start Calling"
   - Check call logs table for status

5. **Check Statistics**:
   - View stats: Total, In Progress, Answered, Failed
   - Download logs as CSV

### Step 4: Test API Endpoints (Optional)

```bash
# Health check
curl http://localhost:5000/health

# Upload numbers
curl -X POST http://localhost:5000/upload-numbers \
  -F "numbers=18001234567
18001234568"

# Get logs
curl http://localhost:5000/logs

# AI command
curl -X POST http://localhost:5000/ai-command \
  -H "Content-Type: application/json" \
  -d '{"command":"call 18001234567 and play Hello"}'
```

### Expected Behavior
- ✅ Web interface loads
- ✅ Numbers can be uploaded
- ✅ AI command parser works
- ✅ Call logs display
- ⚠️ Actual calls require valid Twilio credentials

### Troubleshooting
- **Port 5000 in use**: Use `PORT=5001 python app.py`
- **Twilio errors**: Check credentials in `.env`
- **AI command fails**: Falls back to regex parser (still works)

---

## 3️⃣ Testing Blog Generator

### Step 1: Setup
```bash
cd BlogGenerator

# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Verify API Key
```bash
# Quick test
python -c "import os; from dotenv import load_dotenv; load_dotenv('../.env'); print('✅ API Key found!' if os.getenv('OPENAI_API_KEY') else '❌ API Key missing')"
```

### Step 3: Start Flask App
```bash
# Run the app
python app.py

# You should see:
# * Running on http://127.0.0.1:5001
```

### Step 4: Test in Browser

1. **Open browser**: http://localhost:5001

2. **Generate Blogs**:
   - Enter 2-3 blog titles (one per line):
     ```
     Getting Started with Python FastAPI
     Building Scalable Microservices
     Introduction to Docker Containers
     ```
   - Select tone: Professional
   - Set word count: 800
   - Click "🚀 Generate Blogs"
   - Wait 10-20 seconds (watch progress bar)

3. **View Generated Blogs**:
   - Click "📚 View All Blogs"
   - See list of generated articles
   - Click any blog to read full article

4. **Check Generated Files**:
   ```bash
   ls -la generated/
   # Should show .md files for each generated blog
   ```

### Step 5: Test API Endpoints (Optional)

```bash
# Health check
curl http://localhost:5001/health

# Generate blog
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "titles": ["Test Blog Article"],
    "tone": "professional",
    "word_count": 400
  }'

# List blogs
curl http://localhost:5001/blog
```

### Expected Behavior
- ✅ Web interface loads
- ✅ Blogs generate successfully (10-20 seconds each)
- ✅ Markdown files created in `generated/` folder
- ✅ Blog listing page shows all articles
- ✅ Blog view page displays formatted content

### Troubleshooting
- **API key error**: Check `.env` file has `OPENAI_API_KEY`
- **Rate limit**: Wait 1 minute between requests (free tier: 3 req/min)
- **Generation fails**: Check OpenAI account has credits
- **Port 5001 in use**: Use `PORT=5002 python app.py`

---

## 🚀 Quick Test All Apps

### Automated Test Script

```bash
# Run comprehensive test
python3 test_all_apps.py
```

This will test:
- ✅ LinkedIn Scraper setup
- ✅ Autodialer endpoints
- ✅ Blog Generator with actual API call

### Manual Quick Test

```bash
# Terminal 1: Autodialer
cd Autodialer && source venv/bin/activate && python app.py
# Open: http://localhost:5000

# Terminal 2: Blog Generator
cd BlogGenerator && source venv/bin/activate && python app.py
# Open: http://localhost:5001

# Terminal 3: LinkedIn Scraper
cd LinkedInScraper && source venv/bin/activate && python scraper.py --urls urls.txt --output test.csv
```

---

## ✅ Test Checklist

### LinkedIn Scraper
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Scraper runs without errors
- [ ] CSV file created with 20 profiles
- [ ] Data includes: name, headline, location, etc.

### Autodialer
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Flask app starts on port 5000
- [ ] Web interface loads
- [ ] Can upload/paste numbers
- [ ] AI command parser works
- [ ] Call logs display
- [ ] Statistics show correctly

### Blog Generator
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] OpenAI API key configured
- [ ] Flask app starts on port 5001
- [ ] Web interface loads
- [ ] Can generate blogs
- [ ] Blogs appear in listing
- [ ] Blog view displays correctly
- [ ] Markdown files created

---

## 🐛 Common Issues & Solutions

### Issue: ModuleNotFoundError
**Solution**: Make sure venv is activated and dependencies installed
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution**: Use different port
```bash
PORT=5002 python app.py
```

### Issue: OpenAI API errors
**Solution**: 
- Check API key in `.env`
- Verify account has credits
- Check rate limits (wait 1 min between requests)

### Issue: ChromeDriver not found
**Solution**: Script auto-downloads it, or install manually:
```bash
# macOS
brew install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

### Issue: Twilio authentication error
**Solution**: 
- Check credentials in `.env`
- Verify Account SID and Auth Token
- For testing, endpoints work without valid credentials

---

## 📊 Expected Test Results

### LinkedIn Scraper
- **Time**: 5-10 minutes (20 profiles with delays)
- **Output**: `profiles.csv` with 20 rows
- **Success Rate**: 80-100% (some profiles may be private)

### Autodialer
- **Time**: Instant (web interface)
- **Output**: Web UI with call logs
- **Success Rate**: 100% (UI works, calls need Twilio)

### Blog Generator
- **Time**: 10-20 seconds per blog
- **Output**: Markdown files in `generated/` folder
- **Success Rate**: 100% (if API key valid)

---

## 🎬 For Video Demo

**Recommended test sequence for recording:**

1. **LinkedIn Scraper** (1-2 min)
   - Show `urls.txt` file
   - Run scraper (maybe just 2-3 profiles for demo)
   - Open `profiles.csv` in Excel/viewer

2. **Autodialer** (2-3 min)
   - Show web interface
   - Upload sample numbers
   - Try AI command: `"call 18001234567 and play 'Hello from AeroLeads'"`
   - Show call logs

3. **Blog Generator** (2-3 min)
   - Show web interface
   - Generate 2-3 blogs
   - Show blog listing
   - Open one blog article

**Total demo time: 5-8 minutes** ✅

---

## 📝 Test Log Template

```
Date: ___________
Tester: ___________

LinkedIn Scraper:
[ ] Setup complete
[ ] Scraper ran successfully
[ ] Output file created: ___________
[ ] Profiles scraped: ___/20

Autodialer:
[ ] Setup complete
[ ] App running on: http://localhost:5000
[ ] Upload numbers: Working / Not working
[ ] AI command: Working / Not working
[ ] Call logs: Working / Not working

Blog Generator:
[ ] Setup complete
[ ] App running on: http://localhost:5001
[ ] API key: Configured / Missing
[ ] Blog generation: Working / Not working
[ ] Blogs generated: ___

Notes:
_______________________________________
_______________________________________
```

---

**Happy Testing!** 🎉

If you encounter any issues, check the individual README files in each folder for detailed troubleshooting.

