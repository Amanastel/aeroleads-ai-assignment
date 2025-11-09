# Complete Setup Guide

Step-by-step instructions to set up and run all three applications with virtual environments.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.10 or higher installed (`python3 --version`)
- [ ] Git installed (`git --version`)
- [ ] Chrome browser installed
- [ ] Code editor (VS Code, PyCharm, etc.)
- [ ] Terminal/Command Prompt access

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/aeroleads-ai-assignment.git
cd aeroleads-ai-assignment
```

## Step 2: Set Up Environment Variables

```bash
# Copy the example file
cp env.example .env

# Edit .env with your actual credentials
# Use your preferred text editor
nano .env
# or
code .env
```

**Fill in these values:**

```bash
# LinkedIn Scraper
LINKEDIN_EMAIL=your_test_account@example.com
LINKEDIN_PASSWORD=your_test_password

# Twilio (Sign up at: https://www.twilio.com/try-twilio)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# OpenAI (Sign up at: https://platform.openai.com)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

FLASK_ENV=development
```

## Step 3: LinkedIn Scraper Setup

```bash
# Navigate to directory
cd LinkedInScraper

# Create virtual environment
python3 -m venv venv

# Activate venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Verify activation (should show venv path)
which python

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Test run (scrape 20 profiles)
python scraper.py --urls urls.txt --output profiles.csv

# Check output
ls -la profiles.csv
cat profiles.csv | head -5

# Deactivate when done
deactivate

# Go back to root
cd ..
```

**Expected Output:**
```
2025-11-09 10:30:00 - INFO - Loaded 20 URLs from urls.txt
2025-11-09 10:30:05 - INFO - Chrome WebDriver initialized successfully
...
==================================================
SCRAPING SUMMARY
==================================================
Total profiles scraped: 20
Output file: profiles.csv
==================================================
```

## Step 4: Autodialer Setup

```bash
# Navigate to directory
cd Autodialer

# Create virtual environment
python3 -m venv venv

# Activate venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Flask app
python app.py

# Open browser: http://localhost:5000
```

**Test the App:**
1. Open http://localhost:5000
2. Upload `numbers_sample.csv` or paste test numbers
3. Try AI command: `call 18001234567 and play 'Hello from AeroLeads'`
4. Check call logs

**To stop:** Press `Ctrl+C` in terminal

```bash
# Deactivate when done
deactivate

# Go back to root
cd ..
```

## Step 5: Blog Generator Setup

```bash
# Navigate to directory
cd BlogGenerator

# Create virtual environment
python3 -m venv venv

# Activate venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Flask app (port 5001)
python app.py

# Open browser: http://localhost:5001
```

**Test the App:**
1. Open http://localhost:5001
2. Enter 2-3 blog titles (one per line)
3. Select tone and word count
4. Click "Generate Blogs"
5. View generated blogs at http://localhost:5001/blog

**To stop:** Press `Ctrl+C` in terminal

```bash
# Deactivate when done
deactivate

# Go back to root
cd ..
```

## Quick Reference: Virtual Environment Commands

### Create venv
```bash
python3 -m venv venv
```

### Activate venv
```bash
# macOS/Linux
source venv/bin/activate

# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1
```

### Check if activated
```bash
# Should show path to venv's python
which python  # macOS/Linux
where python  # Windows
```

### Install packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Deactivate venv
```bash
deactivate
```

## Running Multiple Apps Simultaneously

To run multiple apps at once, use separate terminal windows:

**Terminal 1 (Autodialer):**
```bash
cd Autodialer
source venv/bin/activate
python app.py
# Runs on http://localhost:5000
```

**Terminal 2 (Blog Generator):**
```bash
cd BlogGenerator
source venv/bin/activate
python app.py
# Runs on http://localhost:5001
```

## Troubleshooting

### "python3: command not found"
- Install Python from python.org
- Or try `python` instead of `python3`

### "pip: command not found"
```bash
python3 -m ensurepip --upgrade
```

### Virtual environment not activating
**Windows PowerShell:** May need to enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port already in use
```bash
# Use different port
PORT=5002 python app.py
```

### ChromeDriver issues
The script auto-downloads ChromeDriver. If it fails:
```bash
# macOS with Homebrew
brew install chromedriver

# Or download manually from:
# https://chromedriver.chromium.org/downloads
```

### Module not found after installing
- Ensure venv is activated (check with `which python`)
- Try: `pip install --upgrade -r requirements.txt`

### OpenAI API errors
- Verify API key in .env
- Check billing is set up at platform.openai.com
- Check rate limits (3 req/min on free tier)

### Twilio errors
- Verify credentials in .env
- Check account balance
- For trial accounts, verify destination numbers

## Testing Workflow

### 1. Test LinkedIn Scraper
```bash
cd LinkedInScraper
source venv/bin/activate
python scraper.py --urls urls.txt --output test_profiles.csv
# Check: test_profiles.csv should have 20 rows
deactivate
cd ..
```

### 2. Test Autodialer
```bash
cd Autodialer
source venv/bin/activate
python app.py &  # Run in background
sleep 3
curl http://localhost:5000/health
# Should return: {"status":"ok",...}
fg  # Bring to foreground
# Press Ctrl+C to stop
deactivate
cd ..
```

### 3. Test Blog Generator
```bash
cd BlogGenerator
source venv/bin/activate
python app.py &  # Run in background
sleep 3
curl http://localhost:5001/health
# Should return: {"status":"ok",...}
fg  # Bring to foreground
# Press Ctrl+C to stop
deactivate
cd ..
```

## Next Steps

After successful local testing:

1. ✅ Record your 6-7 minute demo video
2. ✅ Deploy apps to Render/PythonAnywhere
3. ✅ Update README with demo URLs
4. ✅ Push to GitHub
5. ✅ Share video link

## Need Help?

Check individual README files:
- `LinkedInScraper/README.md`
- `Autodialer/README.md`
- `BlogGenerator/README.md`

Each contains detailed troubleshooting and usage instructions.

