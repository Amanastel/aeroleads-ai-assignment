# Autodialer Web Application

A Flask-based web app that initiates phone calls via Twilio API with AI-powered natural language command parsing.

## ⚠️ Important Safety Disclaimer

**ONLY use this tool with proper consent and test numbers.** Automated calling without consent may violate laws and regulations. For this demo:
- Use Twilio test credentials or verified test numbers
- Use toll-free numbers (1-800) for testing
- Do NOT call real personal numbers without explicit permission
- Be aware of Do Not Call regulations in your jurisdiction

## Features

- Upload phone numbers via CSV or paste (up to 100)
- Initiate calls sequentially via Twilio API
- AI command parser: type natural language to trigger calls
  - Example: `"call 919876543210 and play 'Hello from AeroLeads'"`
- Real-time call logs with status tracking
- Statistics dashboard (total, in-progress, answered, failed)
- Download call logs as CSV
- Webhook support for Twilio status callbacks

## Setup

### 1. Create Virtual Environment

```bash
# Navigate to Autodialer directory
cd Autodialer

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

### 3. Configure Twilio Account

1. Sign up for Twilio at https://www.twilio.com/try-twilio
2. Get your Account SID and Auth Token from the console
3. Get a Twilio phone number (or use test credentials)

### 4. Set Environment Variables

Create a `.env` file in this directory:

```bash
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# Optional: For AI command parsing with OpenAI
OPENAI_API_KEY=your_openai_api_key

FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-change-in-production
```

### 5. Configure Twilio Webhooks (Optional)

For receiving call status updates:

1. If testing locally, use ngrok:
   ```bash
   ngrok http 5000
   ```

2. Set the webhook URL in Twilio console or in code:
   - Webhook URL: `https://your-domain.com/twilio/callback`
   - Method: POST

## Usage

### Start the Application

```bash
# Make sure venv is activated
source venv/bin/activate

# Run Flask app
python app.py

# Or use flask run
flask run
```

The app will be available at: **http://localhost:5000**

### Using the Web Interface

1. **Upload Numbers**
   - Upload CSV file (with `phone_number` column)
   - Or paste numbers (one per line)
   - Click "Upload Numbers"

2. **AI Command Prompt**
   - Type natural language commands like:
     - `"call 919876543210 and play 'Hello from AeroLeads'"`
     - `"make a call to 18001234567 with message Hi, this is a demo"`
   - Click "Execute AI Command"

3. **Start Batch Calling**
   - Enter custom message
   - Click "Start Calling" (calls up to 5 numbers for demo)

4. **Monitor Calls**
   - View real-time statistics
   - Check call logs table
   - Download logs as CSV

## API Endpoints

### POST /upload-numbers
Upload phone numbers via CSV file or text

**Request:**
- Form data: `file` (CSV) or `numbers` (text)

**Response:**
```json
{
  "success": true,
  "count": 20,
  "numbers": ["18001234567", "..."]
}
```

### POST /start-calls
Start calling numbers from queue

**Request:**
- Form data: `message` (optional)

**Response:**
```json
{
  "success": true,
  "calls_initiated": 5,
  "results": [...]
}
```

### POST /ai-command
Execute natural language command

**Request:**
```json
{
  "command": "call 919876543210 and play 'Hello'"
}
```

**Response:**
```json
{
  "success": true,
  "parsed": {
    "numbers": ["919876543210"],
    "message": "Hello"
  },
  "calls_initiated": 1,
  "results": [...]
}
```

### GET /logs
Get call logs and statistics

**Response:**
```json
{
  "logs": [...],
  "stats": {
    "total": 10,
    "answered": 7,
    "failed": 2,
    "in_progress": 1
  }
}
```

### GET /logs/download
Download call logs as CSV file

### POST /twilio/callback
Twilio status callback webhook (configured in Twilio console)

## AI Command Parser

The AI command parser supports two modes:

### 1. Regex-based Parsing (Default)
- Extracts phone numbers using regex patterns
- Looks for quoted text as message
- Falls back to default message if not found

### 2. OpenAI-based Parsing (Optional)
- Requires `OPENAI_API_KEY` in environment
- Uses GPT-3.5 to parse natural language
- More flexible and accurate

**Supported command formats:**
- `call [number] and play '[message]'`
- `make a call to [number] with message [message]`
- `dial [number] say '[message]'`

## Testing with Twilio

### Using Twilio Test Credentials

For testing without making real calls, use Twilio's Magic Phone Numbers:
- Any number containing `555` will simulate different call statuses
- See: https://www.twilio.com/docs/iam/test-credentials

### Test Phone Numbers

Use the provided `numbers_sample.csv` which contains 20 toll-free numbers safe for testing.

## Deployment

### Deploy to Render

1. Create `render.yaml` (see root README)
2. Push to GitHub
3. Connect Render to your repo
4. Set environment variables in Render dashboard
5. Deploy!

### Deploy to PythonAnywhere

1. Upload code to PythonAnywhere
2. Create virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 autodialer
   pip install -r requirements.txt
   ```
3. Configure WSGI file to point to `app.py`
4. Set environment variables in web app settings
5. Reload web app

## Troubleshooting

### "Twilio client not initialized"
- Check that `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` are set correctly
- Verify credentials at https://www.twilio.com/console

### "Invalid phone number format"
- Phone numbers must be in E.164 format: `+[country code][number]`
- Examples: `+919876543210`, `+18001234567`

### Calls not connecting
- Verify Twilio phone number is correct
- Check account balance (free trial has limitations)
- Ensure destination numbers are verified (for trial accounts)
- Check Twilio debugger: https://www.twilio.com/console/debugger

### AI commands not working
- If using OpenAI: check `OPENAI_API_KEY` is valid
- Fallback regex parser should work without API key
- Check logs for parsing errors

## Technical Stack

- **Backend:** Flask 3.0
- **API:** Twilio Python SDK
- **AI:** OpenAI API (optional)
- **Frontend:** Vanilla JavaScript + Modern CSS
- **Data:** In-memory storage (use database in production)

## Security Notes

- Store environment variables securely (never commit `.env`)
- Use HTTPS in production
- Implement rate limiting for production
- Add authentication for production deployment
- Comply with TCPA and Do Not Call regulations
- Log all calls for compliance and auditing

## License

MIT License - See root LICENSE file. Educational use only.

