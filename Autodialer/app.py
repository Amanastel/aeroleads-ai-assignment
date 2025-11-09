#!/usr/bin/env python3
"""
Autodialer Web Application
A Flask app that initiates calls via Twilio API with AI-powered command parsing.
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from flask import Flask, render_template, request, jsonify, send_file
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.info("Twilio client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Twilio client: {e}")
else:
    logger.warning("Twilio credentials not found. Some features will be disabled.")

# In-memory storage for call logs (use database in production)
call_logs = []
phone_numbers_queue = []


class AICommandParser:
    """Parse natural language commands to extract phone numbers and messages"""
    
    @staticmethod
    def parse_command(command: str) -> Optional[Dict]:
        """
        Parse AI command to extract phone number and message
        Examples:
            "call 919876543210 and play 'Hello from AeroLeads'"
            "make a call to 18001234567 with message Hi, this is a demo"
        """
        # Clean the command
        command = command.strip()
        
        # Try OpenAI-based parsing first (if API key available)
        openai_result = AICommandParser._parse_with_openai(command)
        if openai_result:
            return openai_result
        
        # Fallback to regex-based parsing
        return AICommandParser._parse_with_regex(command)
    
    @staticmethod
    def _parse_with_regex(command: str) -> Optional[Dict]:
        """Parse command using regex patterns"""
        result = {'numbers': [], 'message': 'Hello, this is a test call from AeroLeads.'}
        
        # Extract phone numbers (10-13 digits, may include + or country code)
        phone_patterns = [
            r'\+?\d{10,13}',  # International format
            r'\d{10}',        # 10 digit format
            r'91\d{10}',      # India format with country code
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, command)
            if matches:
                result['numbers'].extend(matches)
                break
        
        # Remove duplicates and clean numbers
        result['numbers'] = list(set(result['numbers']))
        
        # Extract message from quotes or after keywords
        message_patterns = [
            r'["\'](.+?)["\']',  # Text in quotes
            r'(?:message|play|say)[\s:]+(.+?)(?:\s+to|\s+and|$)',  # After keywords
        ]
        
        for pattern in message_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                result['message'] = match.group(1).strip()
                break
        
        # Validate we found at least one number
        if result['numbers']:
            logger.info(f"Parsed command - Numbers: {result['numbers']}, Message: {result['message']}")
            return result
        
        logger.warning(f"Could not parse phone number from command: {command}")
        return None
    
    @staticmethod
    def _parse_with_openai(command: str) -> Optional[Dict]:
        """Parse command using OpenAI API (optional enhancement)"""
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                return None
            
            openai.api_key = api_key
            
            prompt = f"""Extract phone numbers and message from this command. Return ONLY valid JSON.
Command: "{command}"

Return format:
{{"numbers": ["phone1", "phone2"], "message": "text to say"}}

If no message is specified, use: "Hello, this is a call from AeroLeads."
"""
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a command parser. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response (may have markdown backticks)
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                if result.get('numbers'):
                    logger.info(f"OpenAI parsed command - {result}")
                    return result
        
        except Exception as e:
            logger.warning(f"OpenAI parsing failed: {e}")
        
        return None


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    # Remove spaces and dashes
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's a valid format (10-13 digits)
    if re.match(r'^\+?\d{10,13}$', phone):
        return True
    
    return False


def format_phone_number(phone: str) -> str:
    """Format phone number for Twilio (E.164 format)"""
    # Remove all non-digit characters except +
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Add + if not present and starts with country code
    if not phone.startswith('+'):
        if phone.startswith('91') and len(phone) == 12:  # India
            phone = '+' + phone
        elif phone.startswith('1') and len(phone) == 11:  # US
            phone = '+' + phone
        elif len(phone) == 10:  # Assume US if 10 digits
            phone = '+1' + phone
        else:
            phone = '+' + phone
    
    return phone


def make_call(to_number: str, message: str) -> Dict:
    """
    Initiate a call using Twilio API
    Returns call log dict with status
    """
    if not twilio_client:
        return {
            'to_number': to_number,
            'message': message,
            'status': 'failed',
            'error': 'Twilio client not initialized',
            'timestamp': datetime.now().isoformat()
        }
    
    try:
        # Validate and format phone number
        if not validate_phone_number(to_number):
            raise ValueError(f"Invalid phone number format: {to_number}")
        
        formatted_number = format_phone_number(to_number)
        
        # Create TwiML response
        twiml = f'<Response><Say voice="alice">{message}</Say></Response>'
        
        # Make the call
        call = twilio_client.calls.create(
            to=formatted_number,
            from_=TWILIO_PHONE_NUMBER,
            twiml=twiml
        )
        
        log_entry = {
            'call_sid': call.sid,
            'to_number': to_number,
            'formatted_number': formatted_number,
            'message': message,
            'status': call.status,
            'timestamp': datetime.now().isoformat(),
            'error': None
        }
        
        logger.info(f"Call initiated: {call.sid} to {formatted_number}")
        return log_entry
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to make call to {to_number}: {error_msg}")
        
        return {
            'call_sid': None,
            'to_number': to_number,
            'formatted_number': None,
            'message': message,
            'status': 'failed',
            'timestamp': datetime.now().isoformat(),
            'error': error_msg
        }


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/upload-numbers', methods=['POST'])
def upload_numbers():
    """Handle phone number upload (CSV or pasted text)"""
    global phone_numbers_queue
    
    try:
        # Check if file upload or text paste
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            
            # Read CSV
            df = pd.read_csv(file)
            
            # Try to find phone number column
            phone_col = None
            for col in df.columns:
                if 'phone' in col.lower() or 'number' in col.lower():
                    phone_col = col
                    break
            
            if phone_col:
                numbers = df[phone_col].astype(str).tolist()
            else:
                # Use first column
                numbers = df.iloc[:, 0].astype(str).tolist()
        
        else:
            # Text paste
            text = request.form.get('numbers', '')
            numbers = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Validate and clean numbers
        valid_numbers = []
        for num in numbers:
            # Remove non-digit characters for validation
            clean_num = re.sub(r'[^\d+]', '', num)
            if validate_phone_number(clean_num):
                valid_numbers.append(clean_num)
        
        phone_numbers_queue = valid_numbers
        
        logger.info(f"Loaded {len(valid_numbers)} valid phone numbers")
        
        return jsonify({
            'success': True,
            'count': len(valid_numbers),
            'numbers': valid_numbers[:10]  # Return first 10 for preview
        })
    
    except Exception as e:
        logger.error(f"Error uploading numbers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/start-calls', methods=['POST'])
def start_calls():
    """Start calling numbers from the queue"""
    global call_logs
    
    if not phone_numbers_queue:
        return jsonify({'success': False, 'error': 'No phone numbers in queue'}), 400
    
    # Get optional message
    message = request.form.get('message', 'Hello, this is a test call from AeroLeads.')
    
    # Limit for demo (don't call all at once)
    max_calls = min(len(phone_numbers_queue), 5)
    
    results = []
    for i in range(max_calls):
        number = phone_numbers_queue[i]
        log_entry = make_call(number, message)
        call_logs.append(log_entry)
        results.append(log_entry)
    
    return jsonify({
        'success': True,
        'calls_initiated': len(results),
        'results': results
    })


@app.route('/ai-command', methods=['POST'])
def ai_command():
    """Handle AI natural language command"""
    global call_logs
    
    try:
        command = request.json.get('command', '')
        
        if not command:
            return jsonify({'success': False, 'error': 'No command provided'}), 400
        
        # Parse command
        parsed = AICommandParser.parse_command(command)
        
        if not parsed or not parsed.get('numbers'):
            return jsonify({
                'success': False,
                'error': 'Could not extract phone number from command'
            }), 400
        
        # Make calls to extracted numbers
        results = []
        for number in parsed['numbers']:
            log_entry = make_call(number, parsed['message'])
            call_logs.append(log_entry)
            results.append(log_entry)
        
        return jsonify({
            'success': True,
            'parsed': parsed,
            'calls_initiated': len(results),
            'results': results
        })
    
    except Exception as e:
        logger.error(f"Error processing AI command: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/logs', methods=['GET'])
def get_logs():
    """Get call logs"""
    # Calculate stats
    total = len(call_logs)
    answered = len([log for log in call_logs if log['status'] in ['in-progress', 'completed', 'answered']])
    failed = len([log for log in call_logs if log['status'] == 'failed' or log.get('error')])
    in_progress = len([log for log in call_logs if log['status'] == 'in-progress'])
    
    return jsonify({
        'logs': call_logs,
        'stats': {
            'total': total,
            'answered': answered,
            'failed': failed,
            'in_progress': in_progress
        }
    })


@app.route('/logs/download', methods=['GET'])
def download_logs():
    """Download call logs as CSV"""
    if not call_logs:
        return "No logs available", 404
    
    df = pd.DataFrame(call_logs)
    output_file = 'call_logs.csv'
    df.to_csv(output_file, index=False)
    
    return send_file(output_file, as_attachment=True)


@app.route('/twilio/callback', methods=['POST'])
def twilio_callback():
    """Twilio status callback endpoint"""
    call_sid = request.form.get('CallSid')
    call_status = request.form.get('CallStatus')
    
    # Update log entry
    for log in call_logs:
        if log.get('call_sid') == call_sid:
            log['status'] = call_status
            logger.info(f"Updated call {call_sid} status to {call_status}")
            break
    
    return '', 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'twilio_configured': twilio_client is not None,
        'queue_size': len(phone_numbers_queue),
        'total_calls': len(call_logs)
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')

