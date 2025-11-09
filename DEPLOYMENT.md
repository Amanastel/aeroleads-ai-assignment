# Deployment Guide

Complete guide for deploying the applications to various hosting platforms.

## 🚀 Quick Deploy Options

| Platform | Free Tier | Best For | Difficulty |
|----------|-----------|----------|------------|
| **Render** | ✅ Yes (750 hrs/month) | Both apps | Easy ⭐ |
| **PythonAnywhere** | ✅ Yes (limited) | Both apps | Easy ⭐ |
| **Railway** | ✅ Trial ($5 credit) | Both apps | Easy ⭐ |
| **Heroku** | ❌ No (discontinued free tier) | - | - |
| **Vercel** | ⚠️ Serverless only | Blog Generator | Medium ⭐⭐ |

## Option 1: Deploy to Render (Recommended)

Render offers free hosting with 750 hours per month (enough for 2 apps running 24/7).

### Step-by-Step

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - AeroLeads assignment"
   git branch -M main
   git remote add origin https://github.com/yourusername/aeroleads-ai-assignment.git
   git push -u origin main
   ```

2. **Sign up for Render**
   - Go to https://render.com
   - Sign up with GitHub

3. **Deploy using render.yaml**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` and create both services
   - Set environment variables for each service:
     - Autodialer: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `OPENAI_API_KEY`
     - BlogGenerator: `OPENAI_API_KEY`

4. **Wait for deployment** (5-10 minutes)
   - Render will build and deploy both apps
   - You'll get URLs like:
     - `https://aeroleads-autodialer.onrender.com`
     - `https://aeroleads-bloggenerator.onrender.com`

5. **Test your deployments**
   ```bash
   curl https://aeroleads-autodialer.onrender.com/health
   curl https://aeroleads-bloggenerator.onrender.com/health
   ```

### Render Limitations (Free Tier)
- Apps spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds (cold start)
- 750 hours/month shared across all services
- No custom domains on free tier

## Option 2: Deploy to PythonAnywhere

PythonAnywhere offers free hosting for Python web apps.

### Autodialer Deployment

1. **Sign up at PythonAnywhere**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload code**
   - Files tab → Upload `Autodialer` folder
   - Or use Git:
     ```bash
     git clone https://github.com/yourusername/aeroleads-ai-assignment.git
     cd aeroleads-ai-assignment/Autodialer
     ```

3. **Create virtual environment**
   - Open Bash console:
     ```bash
     mkvirtualenv --python=/usr/bin/python3.10 autodialer
     cd aeroleads-ai-assignment/Autodialer
     pip install -r requirements.txt
     ```

4. **Configure Web App**
   - Web tab → Add a new web app
   - Choose "Manual configuration" → Python 3.10
   - Set source code directory: `/home/yourusername/aeroleads-ai-assignment/Autodialer`
   - Set virtual environment: `/home/yourusername/.virtualenvs/autodialer`

5. **Edit WSGI file** (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):
   ```python
   import sys
   import os
   
   # Add your project directory
   project_home = '/home/yourusername/aeroleads-ai-assignment/Autodialer'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   
   # Load environment variables
   from dotenv import load_dotenv
   load_dotenv(os.path.join(project_home, '.env'))
   
   # Import Flask app
   from app import app as application
   ```

6. **Set environment variables**
   - WSGI file or in app code:
     ```python
     os.environ['TWILIO_ACCOUNT_SID'] = 'your_sid'
     os.environ['TWILIO_AUTH_TOKEN'] = 'your_token'
     # ... etc
     ```

7. **Reload web app**
   - Web tab → Reload button
   - Access at: `https://yourusername.pythonanywhere.com`

### Blog Generator Deployment

Repeat the same steps for BlogGenerator, using a different subdomain or path.

### PythonAnywhere Limitations (Free Tier)
- Only one web app per account
- Limited CPU/bandwidth
- No HTTPS for custom domains
- Cannot make external API calls from some IPs (use paid tier)

## Option 3: Deploy to Railway

Railway offers $5 free trial credit (enough for testing).

### Steps

1. **Sign up at Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create new project**
   - Dashboard → New Project → Deploy from GitHub repo
   - Select your repository

3. **Configure services**
   
   **For Autodialer:**
   - Add service → Select Autodialer folder
   - Settings:
     - Root Directory: `Autodialer`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Variables tab → Add:
     - `TWILIO_ACCOUNT_SID`
     - `TWILIO_AUTH_TOKEN`
     - `TWILIO_PHONE_NUMBER`
     - `OPENAI_API_KEY`

   **For BlogGenerator:**
   - Repeat above steps with `BlogGenerator` folder

4. **Deploy**
   - Railway auto-deploys on git push
   - You'll get URLs for each service

### Railway Limitations
- $5 trial credit (runs out after usage)
- Need credit card for continued use ($5/month minimum)

## Option 4: Deploy to Fly.io

Free tier available with credit card.

### Quick Deploy

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Deploy Autodialer**
   ```bash
   cd Autodialer
   
   # Create fly.toml
   fly launch --name aeroleads-autodialer
   
   # Set secrets
   fly secrets set TWILIO_ACCOUNT_SID="your_sid"
   fly secrets set TWILIO_AUTH_TOKEN="your_token"
   fly secrets set TWILIO_PHONE_NUMBER="your_number"
   fly secrets set OPENAI_API_KEY="your_key"
   
   # Deploy
   fly deploy
   ```

4. **Repeat for BlogGenerator**

## 🔐 Security Best Practices for Deployment

### Environment Variables
- **Never** commit API keys to GitHub
- Use platform's secret management:
  - Render: Environment Variables tab
  - PythonAnywhere: Set in WSGI or use python-dotenv
  - Railway: Variables tab
  - Fly.io: `fly secrets set`

### HTTPS
- All platforms provide free HTTPS
- Always use HTTPS URLs in production

### Rate Limiting
For production, add rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/generate', methods=['POST'])
@limiter.limit("10 per hour")
def generate():
    # Your code
    pass
```

### Authentication
For production deployments, add authentication:

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == os.getenv('ADMIN_USER') and password == os.getenv('ADMIN_PASS'):
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')
```

## 🧪 Testing Deployed Apps

### Autodialer
```bash
# Health check
curl https://your-autodialer-url.com/health

# Test upload (from local)
curl -X POST https://your-autodialer-url.com/upload-numbers \
  -F "numbers=18001234567
18001234568"
```

### Blog Generator
```bash
# Health check
curl https://your-bloggenerator-url.com/health

# Test generation
curl -X POST https://your-bloggenerator-url.com/generate \
  -H "Content-Type: application/json" \
  -d '{"titles":["Test Blog"],"tone":"professional","word_count":800}'
```

## 📊 Monitoring

### Render
- Logs tab shows real-time logs
- Metrics tab shows CPU/memory usage
- Events tab shows deployment history

### PythonAnywhere
- Log files in Files tab: `/var/log/`
- Error log: Web tab → Log files

### Railway
- Deployments tab shows logs
- Metrics tab shows usage

## 💰 Cost Estimates

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Render** | 750 hrs/month | $7/month per service |
| **PythonAnywhere** | 1 web app | $5/month (Hacker) |
| **Railway** | $5 trial | $5/month minimum |
| **Fly.io** | 3 VMs (256MB) | $1.94/month per VM |

For this demo project, **Render's free tier is recommended** - enough for both apps running 24/7.

## 🎬 Video Demo Hosting URLs

Once deployed, update README.md with your URLs:

```markdown
## 🌐 Hosted Deployments

| Application | Platform | URL |
|-------------|----------|-----|
| **Autodialer** | Render | https://aeroleads-autodialer.onrender.com |
| **BlogGenerator** | Render | https://aeroleads-bloggenerator.onrender.com |
```

## ❓ Troubleshooting Deployment

### Build Fails
- Check Python version in platform settings (use 3.10+)
- Verify all dependencies in requirements.txt
- Check logs for specific error messages

### App Crashes on Start
- Verify environment variables are set
- Check that PORT environment variable is used:
  ```python
  port = int(os.getenv('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
  ```

### API Calls Fail
- Verify API keys are set correctly
- Check if platform allows external API calls
- Test with curl from deployment logs

### Cold Starts (Render Free Tier)
- Apps sleep after 15 min inactivity
- First request takes 30-60 sec
- Upgrade to paid tier for always-on

## 📝 Deployment Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] All sensitive data removed from code
- [ ] Environment variables documented
- [ ] requirements.txt updated
- [ ] Gunicorn added to requirements
- [ ] PORT environment variable handled
- [ ] Health check endpoints working
- [ ] README updated with deployment URLs

## 🎉 Post-Deployment

After successful deployment:
1. Test all features thoroughly
2. Record video demo using deployed URLs
3. Update README with live demo links
4. Monitor logs for errors
5. Check API usage/costs

---

**Need help?** Check platform documentation:
- Render: https://render.com/docs
- PythonAnywhere: https://help.pythonanywhere.com
- Railway: https://docs.railway.app
- Fly.io: https://fly.io/docs

