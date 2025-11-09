# AI Blog Generator

A Flask web application that generates full blog articles from titles using OpenAI's GPT API.

## Features

- Generate up to 10 blog articles at once
- AI-powered content creation using OpenAI GPT-3.5
- Customizable writing tone (professional, casual, technical, beginner-friendly)
- Configurable word count (400-2000 words)
- Markdown format with frontmatter
- Beautiful web UI for browsing generated blogs
- Automatic tagging and excerpt generation
- Persistent storage in markdown files

## Setup

### 1. Create Virtual Environment

```bash
# Navigate to BlogGenerator directory
cd BlogGenerator

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

### 3. Configure OpenAI API Key

Sign up for OpenAI at https://platform.openai.com/ and get your API key.

Create a `.env` file in this directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here

FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-change-in-production
```

## Usage

### Start the Application

```bash
# Make sure venv is activated
source venv/bin/activate

# Run Flask app (default port 5001)
python app.py

# Or use flask run with custom port
PORT=5001 flask run
```

The app will be available at: **http://localhost:5001**

### Generate Blogs

1. **Go to the home page** (`http://localhost:5001`)

2. **Enter blog titles** (one per line, up to 10):
   ```
   Getting Started with Python FastAPI
   Building Scalable Microservices
   Best Practices for REST API Design
   Introduction to Docker Containers
   Advanced Git Workflows for Teams
   ```

3. **Configure options**:
   - **Tone**: Professional, Casual, Technical, or Beginner-Friendly
   - **Word Count**: 400-2000 words (default: 800)

4. **Click "Generate Blogs"**
   - Watch the progress bar as blogs are generated
   - See results for each title (success/failed)

5. **View Generated Blogs**
   - Click "View All Blogs" to see the blog list
   - Click any blog card to read the full article
   - Blogs are saved in the `generated/` directory

## API Endpoints

### POST /generate
Generate blog articles from titles

**Request:**
```json
{
  "titles": [
    "Getting Started with Python",
    "Introduction to Docker"
  ],
  "tone": "professional",
  "word_count": 800
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "title": "Getting Started with Python",
      "success": true,
      "filename": "getting-started-with-python.md",
      "slug": "getting-started-with-python"
    }
  ],
  "total_generated": 1
}
```

### GET /blog
List all generated blogs

Returns HTML page with all blog cards.

### GET /blog/{slug}
View a specific blog article

Returns HTML page with full blog content rendered from markdown.

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "openai_configured": true,
  "total_blogs": 5
}
```

## Generated File Format

Blogs are saved as markdown files with YAML frontmatter:

```markdown
---
title: "Getting Started with Python"
date: 2025-11-09 10:00:00
slug: getting-started-with-python
tags: ["python", "programming", "tutorial"]
excerpt: "Learn the basics of Python programming..."
---

## Introduction

Your blog content here in markdown format...

## Main Section

More content with code examples...

```python
def hello_world():
    print("Hello, World!")
```

## Conclusion

Final thoughts and key takeaways...
```

## Directory Structure

```
BlogGenerator/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── templates/
│   ├── index.html         # Blog generator form
│   ├── blog_list.html     # All blogs listing
│   └── blog_view.html     # Single blog view
└── generated/             # Generated blog markdown files
    ├── sample-blog.md
    └── ...
```

## Customization

### Change OpenAI Model

Edit `app.py` and modify the model parameter:

```python
response = openai_client.chat.completions.create(
    model="gpt-4",  # Change to gpt-4 for better quality
    # ... other parameters
)
```

### Adjust Generation Prompt

Modify the `generate_blog_with_openai()` function in `app.py` to customize:
- Structure requirements
- Section headings
- Code example preferences
- Target audience
- Writing style

### Add More Tones

Add options in `templates/index.html`:

```html
<select id="tone">
    <option value="professional">Professional</option>
    <option value="casual">Casual</option>
    <option value="technical">Technical</option>
    <option value="humorous">Humorous</option>  <!-- New -->
    <option value="academic">Academic</option>   <!-- New -->
</select>
```

## Deployment

### Deploy to Render

1. Create `render.yaml` in project root (see main README)
2. Push to GitHub
3. Connect Render to your repository
4. Set `OPENAI_API_KEY` environment variable in Render dashboard
5. Deploy!

### Deploy to PythonAnywhere

1. Upload code to PythonAnywhere
2. Create virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 bloggenerator
   pip install -r requirements.txt
   ```
3. Configure WSGI file:
   ```python
   import sys
   path = '/home/yourusername/BlogGenerator'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
4. Set `OPENAI_API_KEY` in web app settings
5. Reload web app

## Troubleshooting

### "OpenAI client not initialized"
- Check that `OPENAI_API_KEY` is set correctly in `.env`
- Verify API key is valid at https://platform.openai.com/account/api-keys
- Ensure you have billing set up on OpenAI account

### API Rate Limits
- OpenAI has rate limits based on your plan
- Free tier: 3 requests/minute
- If you hit limits, wait and retry
- Consider upgrading to paid plan for higher limits

### Generation Fails
- Check OpenAI API status: https://status.openai.com/
- Verify you have sufficient credits
- Check logs for specific error messages
- Try reducing `max_tokens` in code if hitting token limits

### Port Already in Use
If port 5001 is taken, use a different port:
```bash
PORT=5002 python app.py
```

## Cost Considerations

**OpenAI API Pricing (as of 2025):**
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens
- Average blog (800 words) = ~1000-1500 tokens
- Cost per blog: $0.002-0.003 (GPT-3.5)

**10 blogs ≈ $0.02-0.03 with GPT-3.5-turbo**

## Alternative LLM Providers

To use other providers, modify the generation function:

### Google Gemini

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt)
content = response.text
```

### Anthropic Claude

```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)
content = message.content[0].text
```

## Technical Stack

- **Backend:** Flask 3.0
- **AI:** OpenAI GPT-3.5-turbo
- **Templating:** Jinja2
- **Markdown:** markdown2
- **Frontend:** Vanilla JavaScript + Modern CSS
- **Storage:** File-based (markdown files)

## License

MIT License - See root LICENSE file. Educational use only.

