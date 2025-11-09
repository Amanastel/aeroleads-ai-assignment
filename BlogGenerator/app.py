#!/usr/bin/env python3
"""
Blog Generator Web Application
Uses OpenAI API to generate full blog articles from titles.
"""

import os
import re
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from flask import Flask, render_template, request, jsonify, redirect, url_for
import markdown2
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

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_client = None

if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        openai_client = None
else:
    logger.warning("OPENAI_API_KEY not found. Blog generation will be disabled.")
    openai_client = None

# Generated blogs directory
GENERATED_DIR = Path(__file__).parent / 'generated'
GENERATED_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    """Convert title to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def generate_blog_with_openai(title: str, tone: str = 'professional', 
                               word_count: int = 800) -> Optional[Dict]:
    """
    Generate blog article using OpenAI API
    
    Args:
        title: Blog post title
        tone: Writing tone (professional, casual, technical, etc.)
        word_count: Target word count
    
    Returns:
        Dict with 'content', 'tags', 'excerpt' or None if failed
    """
    if not openai_client:
        logger.error("OpenAI client not initialized")
        return None
    
    try:
        prompt = f"""Write a comprehensive technical blog article with the following specifications:

Title: {title}

Requirements:
- Tone: {tone}
- Target length: {word_count} words
- Target audience: Intermediate to advanced software engineers and developers
- Include an engaging introduction
- 3-4 main sections with clear headings (use ## for sections)
- Include relevant code examples where applicable (use markdown code blocks)
- Add a conclusion with key takeaways
- Write in markdown format

Structure:
1. Introduction (hook the reader, explain what they'll learn)
2. Main content sections (3-4 sections with headings)
3. Practical examples or code snippets
4. Conclusion and next steps

At the end, include:
TAGS: [2-3 relevant tags, comma-separated]
"""

        logger.info(f"Generating blog for title: {title}")
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional technical blog writer with expertise in software development, programming, and technology. Write clear, informative, and engaging content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract tags from content
        tags = []
        tags_match = re.search(r'TAGS?:\s*\[?([^\]]+)\]?', content, re.IGNORECASE)
        if tags_match:
            tags_text = tags_match.group(1)
            tags = [tag.strip() for tag in tags_text.split(',')]
            # Remove tags line from content
            content = re.sub(r'\n*TAGS?:\s*\[?[^\]]+\]?\n*', '', content, flags=re.IGNORECASE)
        
        # Generate excerpt (first 150 characters)
        # Remove markdown formatting for excerpt
        plain_text = re.sub(r'[#*`\[\]()]', '', content)
        excerpt = ' '.join(plain_text.split()[:30]) + '...'
        
        logger.info(f"Successfully generated blog: {title}")
        
        return {
            'content': content.strip(),
            'tags': tags or ['technology', 'programming'],
            'excerpt': excerpt
        }
    
    except Exception as e:
        logger.error(f"Failed to generate blog for '{title}': {e}")
        return None


def save_blog(title: str, content: str, tags: List[str], excerpt: str) -> str:
    """
    Save blog as markdown file with frontmatter
    
    Returns:
        Filename of saved blog
    """
    slug = slugify(title)
    timestamp = datetime.now()
    
    # Create frontmatter
    frontmatter = f"""---
title: "{title}"
date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
slug: {slug}
tags: {json.dumps(tags)}
excerpt: "{excerpt}"
---

"""
    
    # Combine frontmatter and content
    full_content = frontmatter + content
    
    # Save to file
    filename = f"{slug}.md"
    filepath = GENERATED_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    logger.info(f"Saved blog to: {filepath}")
    return filename


def load_blog(filename: str) -> Optional[Dict]:
    """Load blog from markdown file"""
    filepath = GENERATED_DIR / filename
    
    if not filepath.exists():
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1].strip()
                markdown_content = parts[2].strip()
                
                # Parse frontmatter (simple YAML parsing)
                frontmatter = {}
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"')
                        
                        # Parse JSON for tags
                        if key == 'tags':
                            try:
                                frontmatter[key] = json.loads(value)
                            except:
                                frontmatter[key] = [value]
                        else:
                            frontmatter[key] = value
                
                # Convert markdown to HTML
                html_content = markdown2.markdown(
                    markdown_content,
                    extras=['fenced-code-blocks', 'tables', 'header-ids']
                )
                
                return {
                    'filename': filename,
                    'slug': frontmatter.get('slug', filename.replace('.md', '')),
                    'title': frontmatter.get('title', 'Untitled'),
                    'date': frontmatter.get('date', ''),
                    'tags': frontmatter.get('tags', []),
                    'excerpt': frontmatter.get('excerpt', ''),
                    'content': html_content,
                    'markdown': markdown_content
                }
    
    except Exception as e:
        logger.error(f"Failed to load blog {filename}: {e}")
    
    return None


def list_all_blogs() -> List[Dict]:
    """List all generated blogs"""
    blogs = []
    
    for filepath in GENERATED_DIR.glob('*.md'):
        blog = load_blog(filepath.name)
        if blog:
            blogs.append(blog)
    
    # Sort by date (newest first)
    blogs.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    return blogs


@app.route('/')
def index():
    """Main page - blog generator form"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate blogs from titles"""
    data = request.json
    titles = data.get('titles', [])
    tone = data.get('tone', 'professional')
    word_count = int(data.get('word_count', 800))
    
    if not titles:
        return jsonify({'success': False, 'error': 'No titles provided'}), 400
    
    if len(titles) > 10:
        return jsonify({'success': False, 'error': 'Maximum 10 titles allowed'}), 400
    
    if not openai_client:
        return jsonify({
            'success': False,
            'error': 'OpenAI API not configured. Please set OPENAI_API_KEY environment variable.'
        }), 500
    
    results = []
    
    for title in titles:
        title = title.strip()
        if not title:
            continue
        
        logger.info(f"Generating blog: {title}")
        
        # Generate blog
        blog_data = generate_blog_with_openai(title, tone, word_count)
        
        if blog_data:
            # Save blog
            filename = save_blog(
                title,
                blog_data['content'],
                blog_data['tags'],
                blog_data['excerpt']
            )
            
            results.append({
                'title': title,
                'success': True,
                'filename': filename,
                'slug': slugify(title)
            })
        else:
            results.append({
                'title': title,
                'success': False,
                'error': 'Failed to generate content'
            })
    
    return jsonify({
        'success': True,
        'results': results,
        'total_generated': len([r for r in results if r['success']])
    })


@app.route('/blog')
def blog_list():
    """List all blogs"""
    blogs = list_all_blogs()
    return render_template('blog_list.html', blogs=blogs)


@app.route('/blog/<slug>')
def blog_view(slug):
    """View single blog"""
    # Find blog by slug
    blogs = list_all_blogs()
    blog = next((b for b in blogs if b['slug'] == slug), None)
    
    if not blog:
        return "Blog not found", 404
    
    return render_template('blog_view.html', blog=blog)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'openai_configured': openai_client is not None,
        'total_blogs': len(list_all_blogs())
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')

