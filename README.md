# AeroLeads AI Assignment - Complete Portfolio

A comprehensive 3-part coding assignment showcasing web scraping, API integration, and AI-powered content generation.

## 🎯 Project Overview

This repository contains three independent applications:

1. **LinkedInScraper** - Selenium-based LinkedIn profile scraper
2. **Autodialer** - Twilio-powered automated calling system with AI command parsing
3. **BlogGenerator** - AI blog article generator using OpenAI GPT

## 📁 Repository Structure

```
aeroleads-ai-assignment/
├── LinkedInScraper/          # LinkedIn profile scraper
│   ├── scraper.py           # Main scraper script
│   ├── requirements.txt     # Dependencies
│   ├── urls.txt            # Sample LinkedIn URLs
│   └── README.md           # Setup instructions
│
├── Autodialer/              # Twilio autodialer app
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Dependencies
│   ├── templates/          # HTML templates
│   ├── static/js/          # JavaScript files
│   ├── numbers_sample.csv  # Sample phone numbers
│   └── README.md          # Setup instructions
│
├── BlogGenerator/           # AI blog generator
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Dependencies
│   ├── templates/          # HTML templates
│   ├── generated/          # Generated blog files
│   ├── titles.txt         # Sample blog titles
│   └── README.md          # Setup instructions
│
├── env.example             # Environment variables template
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Git
- Chrome browser (for LinkedIn scraper)

### Clone Repository

```bash
git clone https://github.com/amanastel/aeroleads-ai-assignment.git
cd aeroleads-ai-assignment
```

### Setup Environment Variables

Copy the example env file and add your credentials:

```bash
cp env.example .env
```

Edit `.env` with your actual credentials:

```bash
# LinkedIn Scraper
LINKEDIN_EMAIL=your_test_account@example.com
LINKEDIN_PASSWORD=your_test_password
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver

# Twilio (Autodialer)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# OpenAI (Blog Generator)
OPENAI_API_KEY=your_openai_api_key

# Flask
FLASK_ENV=development
```

## 📋 Running Each Application

### 1️⃣ LinkedIn Scraper

```bash
# Navigate to directory
cd LinkedInScraper

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run scraper
python scraper.py --urls urls.txt --output profiles.csv

# Output: profiles.csv with 20 LinkedIn profiles
```

**What it does:**
- Scrapes 20 LinkedIn public profiles
- Extracts: name, headline, location, company, experience, education, skills
- Saves to CSV format
- Includes polite delays (2-6 seconds) between requests
- Robust error handling and logging

### 2️⃣ Autodialer

```bash
# Navigate to directory
cd Autodialer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Flask app
python app.py

# Access at: http://localhost:5000
```

**What it does:**
- Upload/paste up to 100 phone numbers
- Initiate calls via Twilio API
- AI command parser: `"call 919876543210 and play 'Hello from AeroLeads'"`
- Real-time call logs and statistics
- Download logs as CSV

**Features:**
- Batch calling with custom messages
- Natural language AI commands (with OpenAI) or regex fallback
- Status tracking (total, in-progress, answered, failed)
- Twilio webhook support for status updates

### 3️⃣ Blog Generator

```bash
# Navigate to directory
cd BlogGenerator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Flask app
python app.py

# Access at: http://localhost:5001
```

**What it does:**
- Generate up to 10 blog articles from titles
- AI-powered content using OpenAI GPT-3.5
- Customizable tone and word count
- Saves as markdown with frontmatter
- Beautiful web UI to browse and read blogs

**Features:**
- Professional, casual, technical, or beginner-friendly tones
- 400-2000 word articles
- Automatic tagging and excerpt generation
- Full markdown support with code blocks

## 🔑 API Keys & Credentials

### Required Services

| Service | Purpose | Sign Up Link | Cost |
|---------|---------|--------------|------|
| **LinkedIn** | Test account for scraping | https://linkedin.com | Free |
| **Twilio** | Phone calling API | https://www.twilio.com/try-twilio | Free trial ($15 credit) |
| **OpenAI** | Blog content generation | https://platform.openai.com | Pay-as-you-go (~$0.02/10 blogs) |

### Getting API Keys

**Twilio:**
1. Sign up at Twilio
2. Verify your email and phone
3. Get Account SID and Auth Token from Console
4. Get a free Twilio phone number

**OpenAI:**
1. Sign up at OpenAI Platform
2. Add payment method (required even for trial)
3. Go to API Keys section
4. Create new secret key

## ⚠️ Important Safety & Legal Disclaimers

### LinkedIn Scraping
- **LinkedIn's Terms of Service prohibit automated scraping**
- This tool is for **educational purposes and proof-of-skill only**
- Only use with test accounts and public data
- Respect robots.txt and rate limits
- Do not use for commercial purposes

### Autodialer
- **Only call numbers with explicit consent**
- Use Twilio test credentials or toll-free numbers for demos
- Comply with TCPA (Telephone Consumer Protection Act)
- Respect Do Not Call registries
- Be aware of local telecommunications laws
- **Never call real personal numbers without permission**

### General
- Never commit API keys to version control
- Use environment variables for all secrets
- Be mindful of API rate limits and costs
- This is a demonstration project - use responsibly

## 🎬 Video Demo

**YouTube Link (Unlisted):** [Coming Soon - Upload your video here]

### Video Contents (6-7 minutes):
- 0:00-0:20: Introduction and repo overview
- 0:20-1:40: LinkedIn Scraper demo
- 1:40-3:10: Autodialer with AI command demo
- 3:10-5:00: Blog Generator creating 5 articles
- 5:00-6:00: Deployment notes and code walkthrough
- 6:00-6:30: Closing (salary, notice period, contact)

## 🌐 Hosted Deployments

| Application | Platform | URL |
|-------------|----------|-----|
| **Autodialer** | Render / PythonAnywhere | [Add your URL] |
| **BlogGenerator** | Render / PythonAnywhere | [Add your URL] |

*Note: LinkedIn Scraper runs locally (requires Chrome)*

## 📦 Deployment Instructions

### Deploy to Render (Recommended)

1. **Create `render.yaml` in project root:**

```yaml
services:
  - type: web
    name: autodialer
    env: python
    buildCommand: "cd Autodialer && pip install -r requirements.txt"
    startCommand: "cd Autodialer && gunicorn app:app"
    envVars:
      - key: TWILIO_ACCOUNT_SID
        sync: false
      - key: TWILIO_AUTH_TOKEN
        sync: false
      - key: TWILIO_PHONE_NUMBER
        sync: false
      - key: OPENAI_API_KEY
        sync: false

  - type: web
    name: bloggenerator
    env: python
    buildCommand: "cd BlogGenerator && pip install -r requirements.txt"
    startCommand: "cd BlogGenerator && gunicorn app:app"
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

2. **Push to GitHub**
3. **Connect Render to your repository**
4. **Set environment variables in Render dashboard**
5. **Deploy!**

### Deploy to PythonAnywhere

1. Upload code via Files tab
2. Create virtual environment in Bash console:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myapp
   pip install -r requirements.txt
   ```
3. Configure WSGI file to point to your app
4. Set environment variables in Web tab
5. Reload web app

## 🧪 Testing

### Test Files Included

- `LinkedInScraper/urls.txt` - 20 sample LinkedIn profile URLs
- `Autodialer/numbers_sample.csv` - 20 safe toll-free numbers
- `BlogGenerator/titles.txt` - 10 sample blog titles
- `BlogGenerator/generated/sample-blog.md` - Example generated blog

### Local Testing with ngrok (for Twilio webhooks)

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5000

# Copy the HTTPS URL and set as webhook in Twilio console
# Format: https://your-url.ngrok.io/twilio/callback
```

## 🛠️ Technical Stack

| Component | Technologies |
|-----------|-------------|
| **Languages** | Python 3.10+ |
| **Web Framework** | Flask 3.0 |
| **Scraping** | Selenium, BeautifulSoup4 |
| **APIs** | Twilio (calling), OpenAI (AI generation) |
| **Frontend** | Vanilla JavaScript, Modern CSS |
| **Data** | Pandas, CSV, Markdown |
| **Server** | Gunicorn (production) |

## 📊 Features Summary

### LinkedIn Scraper
✅ Selenium automation  
✅ BeautifulSoup HTML parsing  
✅ CSV export with pandas  
✅ Polite scraping (random delays)  
✅ Robust error handling  
✅ Logging to file  

### Autodialer
✅ Flask web app  
✅ Twilio API integration  
✅ AI command parser (OpenAI + regex fallback)  
✅ Real-time call logs  
✅ Statistics dashboard  
✅ CSV upload/download  
✅ Webhook support  

### Blog Generator
✅ OpenAI GPT integration  
✅ Batch generation (up to 10)  
✅ Customizable tone & length  
✅ Markdown with frontmatter  
✅ Beautiful web UI  
✅ Blog browsing & reading  

## 📝 Code Quality

- ✅ **Written from scratch** (not copied from other sources)
- ✅ **Modular and commented** for maintainability
- ✅ **Error handling** with try-catch blocks
- ✅ **Logging** for debugging
- ✅ **Environment variables** for configuration
- ✅ **Type hints** where applicable
- ✅ **RESTful API design**

## 🐛 Troubleshooting

### Common Issues

**ChromeDriver errors:**
- Install Chrome browser
- Let script auto-download driver, or manually set `CHROME_DRIVER_PATH`

**Twilio errors:**
- Verify Account SID and Auth Token
- Check account balance
- Ensure destination numbers are verified (trial accounts)

**OpenAI errors:**
- Verify API key is valid
- Check you have billing set up
- Monitor rate limits (3 req/min on free tier)

**Port already in use:**
```bash
# Use different ports
PORT=5001 python app.py
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file.

**IMPORTANT:** This code was built from scratch as a proof-of-skill assignment. Use responsibly and only for educational purposes.

## 👨‍💻 Developer Information

**Name:** Aman Kumar  
**Current Salary:** [Add your current salary]  
**Expected Salary:** [Add your expected salary]  
**Notice Period:** [Add your notice period]  
**Contact:** [Add your email/phone]  
**LinkedIn:** [Add your LinkedIn profile]  
**GitHub:** https://github.com/yourusername/aeroleads-ai-assignment

---

## 📹 YouTube Video Checklist

Use this for your video description:

```
AeroLeads AI Assignment - 3-Part Coding Portfolio

Repository: https://github.com/yourusername/aeroleads-ai-assignment

Timestamps:
0:00 - Introduction
0:20 - LinkedIn Scraper Demo
1:40 - Autodialer with AI Commands
3:10 - Blog Generator (5 articles)
5:00 - Code Walkthrough & Deployment
6:00 - Developer Info & Closing

Tech Stack: Python, Flask, Selenium, Twilio, OpenAI

Components:
1. LinkedIn Scraper - Scrapes 20 profiles to CSV
2. Autodialer - Twilio calling with AI parser
3. Blog Generator - AI-powered content creation

Run Locally:
git clone https://github.com/yourusername/aeroleads-ai-assignment.git
cd aeroleads-ai-assignment
# Follow README for setup

Live Demos:
- Autodialer: [Your URL]
- Blog Generator: [Your URL]

Contact: [Your Email]
Current Salary: [Amount]
Expected Salary: [Amount]
Notice Period: [Period]
```

---

## 🎯 Assignment Completion Checklist

- ✅ LinkedIn Scraper - Scrapes 20 profiles
- ✅ Autodialer - Twilio integration with AI parser
- ✅ Blog Generator - OpenAI GPT integration
- ✅ All apps have virtual environment setup
- ✅ READMEs for each component
- ✅ Sample data files included
- ✅ Environment variables documented
- ✅ Safety disclaimers included
- ✅ MIT License
- ⬜ Record 6-7 minute video demo
- ⬜ Deploy apps to hosting platform
- ⬜ Update README with demo URLs
- ⬜ Update README with personal info
- ⬜ Push to GitHub
- ⬜ Share video link in README

---

**Built with ❤️ for AeroLeads | Educational Use Only**

