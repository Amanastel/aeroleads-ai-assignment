#!/usr/bin/env python3
"""
Quick test script to verify OpenAI API key is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv('../.env')

def test_api_key():
    """Test if OpenAI API key is configured and working"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        print("   Make sure you've created .env file with your API key")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ ERROR: API key format looks incorrect")
        print(f"   Key starts with: {api_key[:10]}...")
        return False
    
    print(f"✅ API Key found: {api_key[:15]}...")
    print(f"   Key length: {len(api_key)} characters")
    
    # Test OpenAI import and connection
    try:
        import openai
        openai.api_key = api_key
        
        print("\n🔄 Testing API connection...")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello from AeroLeads'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API connection successful!")
        print(f"   Response: {result}")
        print("\n🎉 Your OpenAI API key is working correctly!")
        return True
        
    except ImportError:
        print("❌ ERROR: openai library not installed")
        print("   Run: pip install openai")
        return False
    except Exception as e:
        error_msg = str(e)
        if "Invalid API key" in error_msg or "authentication" in error_msg.lower():
            print(f"❌ ERROR: Invalid API key")
            print(f"   {error_msg[:100]}")
        elif "rate limit" in error_msg.lower():
            print(f"⚠️  WARNING: Rate limit hit (but key is valid)")
            print(f"   {error_msg[:100]}")
        else:
            print(f"❌ ERROR: {error_msg[:200]}")
        return False

if __name__ == '__main__':
    success = test_api_key()
    sys.exit(0 if success else 1)

