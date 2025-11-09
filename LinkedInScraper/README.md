# LinkedIn Profile Scraper

A Selenium-based scraper that collects public LinkedIn profile data and saves it to CSV.

## ⚠️ Important Disclaimer

**LinkedIn scraping may violate their Terms of Service.** This tool is for educational purposes and proof-of-skill demonstration only. Use responsibly:
- Only scrape public profile data
- Use a test LinkedIn account
- Respect rate limits and robots.txt
- Do not use for commercial purposes without proper authorization

## Features

- Scrapes ~20 LinkedIn profiles from a list of URLs
- Extracts: name, headline, location, company, experience, education, skills
- Saves data to CSV format
- Polite scraping with random delays (2-6 seconds)
- Robust error handling and logging
- Optional LinkedIn login for enhanced access

## Setup

### 1. Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate venv (macOS/Linux)
source venv/bin/activate

# Activate venv (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in this directory (or use the root `.env`):

```bash
LINKEDIN_EMAIL=your_test_account@example.com
LINKEDIN_PASSWORD=your_test_password
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver  # Optional, auto-downloads if not set
```

### 4. Prepare URLs File

Edit `urls.txt` to include LinkedIn profile URLs (one per line):

```
https://www.linkedin.com/in/username1/
https://www.linkedin.com/in/username2/
...
```

## Usage

### Basic Usage (No Login)

```bash
python3 scraper.py --urls urls.txt --output profiles.csv
```

### With LinkedIn Login (More Data)

```bash
python3 scraper.py --urls urls.txt --output profiles.csv --login
```

### Headless Mode (No Browser Window)

```bash
python3 scraper.py --urls urls.txt --output profiles.csv --headless
```

## Command-Line Arguments

- `--urls` : Path to text file containing LinkedIn profile URLs (default: `urls.txt`)
- `--output` : Output CSV file path (default: `profiles.csv`)
- `--headless` : Run browser in headless mode (no UI)
- `--login` : Attempt to login to LinkedIn using credentials from `.env`

## Output Format

The scraper creates a CSV file with these columns:

| Column | Description |
|--------|-------------|
| profile_url | LinkedIn profile URL |
| name | Full name |
| headline | Professional headline |
| location | Geographic location |
| current_company | Current company name |
| experience_summary | Summary of experience (first 200 chars) |
| education | Primary education institution |
| skills | Top 5 skills (comma-separated) |
| extraction_timestamp | ISO timestamp of extraction |

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver errors:

1. **Auto-download** (recommended): The script uses `webdriver-manager` to auto-download the correct driver
2. **Manual installation**: Download ChromeDriver from https://chromedriver.chromium.org/ and set `CHROME_DRIVER_PATH` in `.env`

### LinkedIn Blocking

If LinkedIn blocks requests:
- Reduce scraping frequency (the script already includes delays)
- Use a different IP address or VPN
- Ensure you're using a valid test account
- Try with `--login` flag for authenticated access

### Missing Data Fields

Some fields may be `None` if:
- The profile has privacy settings enabled
- The HTML structure has changed (LinkedIn updates frequently)
- You're not logged in (try `--login` flag)

## Logs

Check `scraper.log` for detailed execution logs and errors.

## Example Run

```bash
# Activate venv
source venv/bin/activate

# Run scraper
python3 scraper.py --urls urls.txt --output profiles.csv

# Expected output:
# 2025-11-09 10:30:00 - INFO - Loaded 20 URLs from urls.txt
# 2025-11-09 10:30:05 - INFO - Chrome WebDriver initialized successfully
# 2025-11-09 10:30:10 - INFO - Processing profile 1/20
# ...
# ==================================================
# SCRAPING SUMMARY
# ==================================================
# Total profiles scraped: 20
# Output file: profiles.csv
# Columns: name, headline, location, ...
# ==================================================
```

## Technical Notes

- Uses Selenium for browser automation
- BeautifulSoup for HTML parsing
- Fake UserAgent for randomized headers
- Pandas for CSV export
- Chrome WebDriver (auto-managed)

## License

MIT License - See root LICENSE file. Educational use only.

