#!/usr/bin/env python3
"""
Share Tweet to WordPress
Fetches a tweet (via FxTwitter API), summarizes it (via Moonshot/Gemini), and posts to WordPress.
Supports standard Tweets and Twitter Articles (Long notes).
"""

import os
import sys
import json
import requests
import time
import re
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client

# Load env
load_dotenv(override=True)

# WordPress Config
WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing" 
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") 
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# AI Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_illustration(prompt_data):
    """Generate image using Gemini (Imagen 3) or DALL-E 3."""
    
    # 1. Try Gemini (Imagen 3) if available
    if GEMINI_API_KEY:
        print(f"🎨 Generating Image (Gemini Imagen 3): {prompt_data['type']} x {prompt_data['style']}...")
        try:
            # Note: The model name for image generation via Gemini API might vary. 
            # Using 'gemini-2.0-flash' for text prompts to generate image description is fine, 
            # but actual image generation endpoint is different.
            # Assuming usage of the new image generation capability if available or fallback.
            # Currently, standard Gemini API python client supports standard generation.
            # Let's try the REST API for Imagen if accessible, or DALL-E fallback.
            
            # Since 'Gemini Flash' itself is a text/multimodal model, the user likely means 
            # using Google's infrastructure. We will try to use the appropriate endpoint if known,
            # but standard `gemini-2.0-flash` does not generate images.
            # However, for this request, I will switch the logic to use the available Gemini key 
            # to generate a *description* and then use a compatible image provider if possible, 
            # OR if the user means "Imagen via Gemini API".
            
            # Google GenAI Image Generation (Imagen 4) via REST:
            # POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GEMINI_API_KEY}"
            payload = {
                "instances": [
                    {
                        "prompt": prompt_data["dalle_prompt"]
                    }
                ],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "16:9"
                }
            }
            
            # Note: The `imagen-3.0-generate-001` is an example model name. 
            # If that fails, we might need to fallback or checks docs.
            # But let's try standard REST approach for Google Cloud / GenAI if key permits.
            
            # Actually, standard API keys often don't support Imagen via REST easily without OAuth.
            # Let's try the common 'gemini-pro-vision' or similar? No, that's input.
            
            # Alternative: Since DALL-E failed and user asked for Gemini Flash *for generation*,
            # they might be mistaken about Flash's capability (it's text-to-text/image-to-text),
            # OR they want me to use a specific library.
            
            # Let's try a safer approach: Use Gemini Flash to *optimize* the prompt (already done in analysis)
            # and then try to use the `google-generativeai` library if installed? No, pip failed earlier.
            
            # Let's stick to REST.
            # Known endpoint for Vertex AI is different. 
            # Let's assume the user has a key that works with the OpenAI-compatible endpoint or similar?
            # No.
            
            # Let's try the common DALL-E style fallback but using the specific prompt logic.
            # If DALL-E is hard-limited, and we only have Gemini Key...
            # I will attempt to use the 'imagen-3.0-generate-001' endpoint.
            
            resp = requests.post(
                url, 
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=60
            )
            
            if resp.status_code == 200:
                # Parse Imagen response
                # Response format: { "predictions": [ { "bytesBase64Encoded": "..." } ] }
                data = resp.json()
                if "predictions" in data and data["predictions"]:
                    b64_data = data["predictions"][0]["bytesBase64Encoded"]
                    # We need to upload this directly.
                    # Return base64 string directly? Or save to temp file?
                    # Let's save to temp file to keep interface consistent (sort of).
                    
                    import base64
                    import tempfile
                    
                    # Create temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tf:
                        tf.write(base64.b64decode(b64_data))
                        print(f"  -> Generated Image saved to: {tf.name}")
                        return f"FILE:{tf.name}" # Special prefix for local file
            else:
                print(f"  -> Gemini Image Gen failed ({resp.status_code}): {resp.text}")

        except Exception as e:
            print(f"  -> Gemini Generation failed: {e}")

    # 2. Fallback to DALL-E 3
    if OPENAI_API_KEY:
        print(f"🎨 Generating Image (DALL-E 3): {prompt_data['type']} x {prompt_data['style']}...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt_data["dalle_prompt"],
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            print(f"  -> Generated: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"  -> DALL-E Generation failed: {e}")
            return None
    
    return None

def upload_image_xmlrpc(client, image_url_or_path):
    """Upload image via XML-RPC. Supports URL or local file path (prefixed with FILE:)."""
    try:
        data = {}
        filename = ""
        
        if image_url_or_path.startswith("FILE:"):
            # Local File
            local_path = image_url_or_path.split("FILE:", 1)[1]
            filename = os.path.basename(local_path)
            with open(local_path, "rb") as f:
                img_data = f.read()
            
            # Clean up temp file
            try:
                os.remove(local_path)
            except:
                pass
        else:
            # URL
            image_url = image_url_or_path
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(image_url, headers=headers, timeout=30)
            resp.raise_for_status()
            img_data = resp.content
            
            # Clean filename
            base_name = os.path.basename(image_url.split('?')[0])
            filename = f"tw_{int(time.time())}_{base_name}"
        
        if not filename.endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp')):
            filename += ".jpg"
        
        data = {
            'name': filename,
            'type': 'image/png' if filename.endswith('.png') else 'image/jpeg',
            'bits': xmlrpc_client.Binary(img_data),
            'overwrite': False,
        }
        response = client.call(media.UploadFile(data))
        return response.get('url')
    except Exception as e:
        print(f"Image Upload Failed: {e} | Source: {image_url_or_path}")
        return None

def analyze_illustration_needs(text):
    """
    Analyze article content to determine illustration needs using 'Type x Style' matrix.
    Returns: { "prompt": str, "style": str, "type": str } or None
    """
    print("🎨 Analyzing illustration needs...")
    
    if not MOONSHOT_API_KEY and not GEMINI_API_KEY:
        print("  -> No AI provider available for analysis.")
        return None

    # Baoyu Article Illustrator Logic
    prompt = f"""Task: You are an expert Art Director (Baoyu Article Illustrator). Analyze the following article content and design ONE perfect illustration to enhance it.

    Design Logic:
    1. Analyze the core theme and structure.
    2. Select the best 'Image Type' from the list below.
    3. Select the best 'Art Style' from the list below.
    4. Combine Type x Style (e.g., 'infographic x blueprint' for data, 'scene x warm' for stories).
    5. Write a detailed DALL-E 3 prompt (in English) describing the image based on the chosen type and style.

    [Image Types]
    - infographic: Data visualization, charts, metrics (Technical articles, data analysis)
    - scene: Atmospheric illustration, mood rendering (Narrative, personal stories)
    - flowchart: Process diagrams, step visualization (Tutorials, workflows)
    - comparison: Side-by-side, before/after contrast (Product comparisons)
    - framework: Concept maps, relationship diagrams (Methodologies, architecture)
    - timeline: Chronological progression (History, project progress)

    [Art Styles]
    - notion: Minimalist hand-drawn line art (Knowledge sharing, SaaS, productivity)
    - elegant: Refined, sophisticated (Business, thought leadership)
    - warm: Friendly, approachable (Personal growth, lifestyle)
    - minimal: Ultra-clean, zen-like (Philosophy, minimalism)
    - blueprint: Technical schematics (Architecture, system design)
    - watercolor: Soft artistic with natural warmth (Lifestyle, travel, creative)
    - editorial: Magazine-style infographic (Tech explainers, journalism)
    - scientific: Academic precise diagrams (Biology, chemistry, technical)
    - retro: Vintage, nostalgic, trendy (Classic, traditional, trend-focused)

    *Special Rule*: If the content seems suitable for social media sharing or lifestyle/trend topics, consider using 'retro' style or similar engaging styles.

    Content (truncated):
    {text[:4000]}...

    Output JSON ONLY:
    {{
        "rationale": "Why this combination?",
        "type": "Selected Type",
        "style": "Selected Style",
        "dalle_prompt": "Detailed English prompt for DALL-E 3...",
        "insert_location": "after_intro"
    }}
    """

    try:
        # Try Gemini Flash first (it's faster and often better at creative tasks than standard Moonshot)
        if GEMINI_API_KEY:
             print("  -> Using Gemini Flash for analysis...")
             # Standard Gemini content generation
             url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
             payload = {"contents": [{"parts": [{"text": prompt}]}]}
             
             resp = requests.post(
                 url, 
                 headers={"Content-Type": "application/json"},
                 json=payload, 
                 timeout=30
             )
             
             if resp.status_code == 200:
                 raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                 # Clean markdown
                 if "```json" in raw:
                     raw = raw.split("```json")[1].split("```")[0]
                 elif "```" in raw:
                     raw = raw.split("```")[1].split("```")[0]
                 return json.loads(raw)
             else:
                 print(f"  -> Gemini Analysis failed: {resp.status_code} {resp.text}")
        
        # Fallback to Moonshot
        if MOONSHOT_API_KEY:
            url = "https://api.moonshot.cn/v1/chat/completions"
            headers = {"Authorization": f"Bearer {MOONSHOT_API_KEY}"}
            data = {
                "model": "moonshot-v1-8k",
                "messages": [{"role": "system", "content": "You are a helpful assistant. Output JSON only."}, {"role": "user", "content": prompt}],
                "temperature": 0.5,
                "response_format": {"type": "json_object"}
            }
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content']
                if "```json" in content:
                     content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                     content = content.split("```")[1].split("```")[0]
                return json.loads(content)
                 
    except Exception as e:
        print(f"  -> Analysis failed: {e}")
    
    return None

def fetch_tweet_content(tweet_url):
    """
    Fetch tweet content using api.fxtwitter.com (JSON).
    Supports Twitter Articles.
    """
    print(f"Fetching tweet: {tweet_url}...")
    
    try:
        parts = tweet_url.split('/')
        if 'status' in parts:
            status_idx = parts.index('status')
            tweet_id = parts[status_idx + 1].split('?')[0]
            username = parts[status_idx - 1]
            
            api_url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
            print(f"Querying API: {api_url}")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(api_url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('code') == 200 and 'tweet' in data:
                    tweet = data['tweet']
                    
                    # Check for Twitter Article (Long form)
                    if 'article' in tweet and tweet['article']:
                        print("📄 Detected Twitter Article/Note.")
                        return parse_twitter_article(tweet, tweet_url, username)
                    
                    # Standard Tweet
                    text = tweet.get('text', '')
                    author = tweet.get('author', {}).get('name', 'Unknown')
                    author_id = tweet.get('author', {}).get('screen_name', username)
                    
                    images = []
                    if 'media' in tweet and 'photos' in tweet['media']:
                        for p in tweet['media']['photos']:
                            images.append(p['url'])
                            
                    print(f"✅ Fetched Standard Tweet: {text[:50]}...")
                    return {
                        "type": "tweet",
                        "text": text,
                        "author": author,
                        "username": author_id,
                        "images": images,
                        "url": tweet_url
                    }
    except Exception as e:
        print(f"⚠️ FxTwitter API fetch failed: {e}")
    return None

def parse_twitter_article(tweet, tweet_url, username):
    """
    Parse Twitter Article JSON structure into readable text and HTML.
    """
    try:
        article = tweet['article']
        content = article.get('content', {})
        blocks = content.get('blocks', [])
        
        # Handle entityMap (can be list or dict)
        raw_entity_map = content.get('entityMap', {})
        entity_map = {}
        if isinstance(raw_entity_map, list):
            for item in raw_entity_map:
                if 'key' in item and 'value' in item:
                    entity_map[str(item['key'])] = item['value']
        elif isinstance(raw_entity_map, dict):
            entity_map = raw_entity_map

        # Find media_entities
        media_entities = []
        # Check various locations
        if 'media_entities' in tweet:
            media_entities.extend(tweet['media_entities'].values() if isinstance(tweet['media_entities'], dict) else tweet['media_entities'])
        if 'media_entities' in article:
            media_entities.extend(article['media_entities'].values() if isinstance(article['media_entities'], dict) else article['media_entities'])
        if 'media_entities' in content:
            media_entities.extend(content['media_entities'].values() if isinstance(content['media_entities'], dict) else content['media_entities'])
            
        # Map media_id to URL
        media_url_map = {}
        for m in media_entities:
             m_id = str(m.get('media_id') or m.get('id_str') or m.get('id'))
             if m_id and 'media_info' in m:
                 media_url_map[m_id] = m['media_info'].get('original_img_url')
        
        full_text = "" # For AI summary
        html_parts = [] # For WordPress content reconstruction
        images_to_upload = [] # List of URLs found
        
        # Track list state to close <ul>/<ol> tags properly
        list_state = None # 'ul', 'ol', or None
        
        for block in blocks:
            text = block.get('text', '')
            b_type = block.get('type', 'unstyled')
            
            # Close list if type changes
            if list_state and b_type not in ['unordered-list-item', 'ordered-list-item']:
                html_parts.append(f"</{list_state}>")
                list_state = None
                
            # Handle Block Types
            if b_type == 'header-one':
                html_parts.append(f"<h4>{text}</h4>")
                full_text += f"\n# {text}\n"
            elif b_type == 'header-two':
                html_parts.append(f"<h5>{text}</h5>")
                full_text += f"\n## {text}\n"
            elif b_type == 'unordered-list-item':
                if list_state != 'ul':
                    html_parts.append("<ul>")
                    list_state = 'ul'
                html_parts.append(f"<li>{text}</li>")
                full_text += f"- {text}\n"
            elif b_type == 'ordered-list-item':
                if list_state != 'ol':
                    html_parts.append("<ol>")
                    list_state = 'ol'
                html_parts.append(f"<li>{text}</li>")
                full_text += f"1. {text}\n"
            elif b_type == 'blockquote':
                html_parts.append(f"<blockquote>{text}</blockquote>")
                full_text += f"> {text}\n"
            elif b_type == 'atomic':
                # This is usually media
                ranges = block.get('entityRanges', [])
                if ranges:
                    key = str(ranges[0].get('key'))
                    entity = entity_map.get(key)
                    if entity and entity.get('type') == 'MEDIA':
                        data = entity.get('data', {})
                        # Sometimes mediaItems is nested or direct
                        media_items = data.get('mediaItems', [])
                        if media_items:
                            m_id = str(media_items[0].get('mediaId'))
                            img_url = media_url_map.get(m_id)
                            if img_url:
                                html_parts.append(f"{{{{IMAGE_PLACEHOLDER:{img_url}}}}}")
                                images_to_upload.append(img_url)
            else:
                # unstyled or other
                if text.strip():
                    html_parts.append(f"<p>{text}</p>")
                    full_text += f"{text}\n"
                else:
                     # Empty paragraph, acts as spacer
                     html_parts.append("<br/>")

        if list_state:
            html_parts.append(f"</{list_state}>")
            
        author = tweet.get('author', {}).get('name', 'Unknown')
        author_id = tweet.get('author', {}).get('screen_name', username)
        
        return {
            "type": "article",
            "text": full_text,
            "html_parts": html_parts,
            "images": images_to_upload,
            "author": author,
            "username": author_id,
            "url": tweet_url
        }
    except Exception as e:
        print(f"⚠️ Error parsing Article: {e}")
        return None

def parse_summary_output(raw_text, original_text_html_parts):
    lines = raw_text.split('\n')
    title = ""
    trans = ""
    point = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("TITLE_CN:") or line.startswith("标题："):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("TRANSLATION:") or line.startswith("翻译："):
            trans = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_POINT:") or line.startswith("观点："):
            point = line.split(":", 1)[1].strip()
            
    if not title: title = "AI 资讯分享"
    
    # HTML Content for WordPress (Summary part)
    summary_html = f"<div style='background-color:#f9f9f9; padding:15px; border-radius:8px; border-left: 4px solid #0073aa; margin-bottom: 20px;'>"
    summary_html += f"<p><strong>摘要</strong>：{trans}</p>"
    summary_html += f"<p><strong>核心观点</strong>：{point}</p>"
    summary_html += "</div>"
    
    return {
        "title": title,
        "summary_html": summary_html
    }

def summarize_with_moonshot(text):
    """Summarize using Moonshot AI (Kimi)."""
    print("Trying Moonshot AI (Kimi)...")
    if not MOONSHOT_API_KEY:
        print("  -> No MOONSHOT_API_KEY found.")
        return None
        
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MOONSHOT_API_KEY}"
    }
    
    # Truncate text if too long for prompt context, though 8k is generous
    safe_text = text[:6000] + "..." if len(text) > 6000 else text

    prompt = f"""Task: Translate and summarize this tweet/article into Chinese.
    
Output Format:
TITLE_CN: [Catchy Chinese Title]
TRANSLATION: [Chinese Translation/Summary of main points]
KEY_POINT: [Core Insight]

Content:
{safe_text}"""

    data = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            content = result['choices'][0]['message']['content']
            return parse_summary_output(content, None) # We don't pass original text here anymore
        else:
            print(f"  -> Moonshot Error: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"  -> Moonshot Exception: {e}")
    return None

def call_gemini(model_name, payload):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        return response
    except Exception as e:
        print(f"Error calling {model_name}: {e}")
        return None

def summarize_tweet(text):
    # 1. Try Moonshot
    res = summarize_with_moonshot(text)
    if res: return res

    # 2. Try Gemini
    print("Trying Gemini...")
    if GEMINI_API_KEY:
        safe_text = text[:10000] # Gemini has large context window
        payload = {
            "contents": [{
                "parts": [{"text": f"Translate and summarize this to Chinese. Format:\nTITLE_CN: Title\nTRANSLATION: Summary\nKEY_POINT: Insight\n\nContent:\n{safe_text}"}]
            }]
        }
        models = ["gemini-2.0-flash", "gemini-pro"]
        for model in models:
            print(f"  -> Model: {model}...")
            resp = call_gemini(model, payload)
            if resp and resp.status_code == 200:
                data = resp.json()
                if "candidates" in data and data["candidates"]:
                    raw = data["candidates"][0]["content"]["parts"][0]["text"]
                    return parse_summary_output(raw, None)
    
    # 3. Fallback
    print("⚠️ All AI models failed.")
    return {
        "title": "Twitter 分享 (AI 摘要失败)",
        "summary_html": f"<p>AI 摘要失败，请直接阅读原文。</p>"
    }

def upload_image_xmlrpc(client, image_url):
    """Upload image via XML-RPC."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(image_url, headers=headers, timeout=30)
        resp.raise_for_status()
        img_data = resp.content
        
        # Clean filename
        base_name = os.path.basename(image_url.split('?')[0])
        filename = f"tw_{int(time.time())}_{base_name}"
        if not filename.endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp')):
            filename += ".jpg"
        
        data = {
            'name': filename,
            'type': resp.headers.get('Content-Type', 'image/jpeg'),
            'bits': xmlrpc_client.Binary(img_data),
            'overwrite': False,
        }
        response = client.call(media.UploadFile(data))
        return response.get('url')
    except Exception as e:
        print(f"Image Upload Failed: {e} | URL: {image_url}")
        return None

def moderate_content(text):
    """Check if content violates WordPress.com ToS using LLM."""
    if not text:
        return False, "Empty content"

    prompt = f"""Task: Audit the following content for violation of WordPress.com Terms of Service.
    
    The ToS prohibits:
    - Unlawful purposes or illegal content
    - Infringement of intellectual property
    - Spam or bulk unsolicited messages
    - Malware, spyware, or malicious code
    - Hateful, offensive, or indecent content (though some freedom is allowed, we want to be safe)
    
    Content to audit:
    {text}
    
    Output Format:
    SAFE: [Yes/No]
    REASON: [Brief explanation if No]
    """

    try:
        # 1. Try Moonshot
        if MOONSHOT_API_KEY:
            url = "https://api.moonshot.cn/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {MOONSHOT_API_KEY}"
            }
            data = {
                "model": "moonshot-v1-8k",
                "messages": [
                    {"role": "system", "content": "You are a content moderator."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            if resp.status_code == 200:
                result = resp.json()['choices'][0]['message']['content']
                if "SAFE: Yes" in result or "SAFE:Yes" in result:
                    return True, "Safe"
                else:
                    return False, result.split("REASON:")[-1].strip() if "REASON:" in result else result
        
        # 2. Try Gemini
        if GEMINI_API_KEY:
             payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
             url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
             resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
             if resp.status_code == 200:
                 data = resp.json()
                 if "candidates" in data and data["candidates"]:
                    result = data["candidates"][0]["content"]["parts"][0]["text"]
                    if "SAFE: Yes" in result or "SAFE:Yes" in result:
                        return True, "Safe"
                    else:
                        return False, result.split("REASON:")[-1].strip() if "REASON:" in result else result

        # Fallback
        return False, "No LLM available for moderation"

    except Exception as e:
        print(f"  - Moderation Error: {e}")
        return False, f"Moderation check failed: {e}"

def run(tweet_url):
    # 1. Fetch
    tweet_data = fetch_tweet_content(tweet_url)
    if not tweet_data:
        print("❌ Failed to fetch tweet content.")
        return
    
    # --- Moderation Check ---
    print("🛡️ Moderating content...")
    is_safe, reason = moderate_content(tweet_data["text"])
    if not is_safe:
        print(f"❌ Content BLOCKED by ToS Check: {reason}")
        return
    # ------------------------

    # 2. Summarize
    print("🤖 Summarizing...")
    summary = summarize_tweet(tweet_data["text"])
    
    # 3. Connect to WordPress
    print("Connecting to WordPress...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"WP Connection Failed: {e}")
        return

    # 4. Upload Images & Prepare Content
    uploaded_map = {} # source_url -> wp_url
    
    # Analyze and Generate Illustration (New Feature)
    illustration_url = None
    try:
        # Check if we should generate an illustration (needs text > 200 chars and an API key)
        should_illustrate = len(tweet_data.get("text", "")) > 200 and OPENAI_API_KEY
        
        if should_illustrate:
            print("🎨 Analyzing article for illustration (Baoyu Article Illustrator)...")
            illustration_data = analyze_illustration_needs(tweet_data["text"])
            
            if illustration_data and "dalle_prompt" in illustration_data:
                print(f"  -> Concept: {illustration_data.get('type')} x {illustration_data.get('style')}")
                print(f"  -> Rationale: {illustration_data.get('rationale')}")
                
                generated_url = generate_illustration(illustration_data)
                
                if generated_url:
                    print("  -> Uploading illustration to WordPress...")
                    wp_illustration_url = upload_image_xmlrpc(client, generated_url)
                    if wp_illustration_url:
                        illustration_url = wp_illustration_url
                        print(f"  -> Uploaded illustration: {illustration_url}")
    except Exception as e:
        print(f"⚠️ Illustration process failed: {e}")

    # Deduplicate images list
    images_to_process = list(set(tweet_data["images"]))
    
    if images_to_process:
        print(f"Found {len(images_to_process)} images. Uploading...")
        for img_url in images_to_process:
            wp_img = upload_image_xmlrpc(client, img_url)
            if wp_img:
                print(f"  -> Uploaded: {wp_img}")
                uploaded_map[img_url] = wp_img
            else:
                print(f"  -> Failed to upload: {img_url}")

    # 5. Construct Content
    username = tweet_data.get('username', 'Unknown')
    post_title = summary["title"]
    
    content_html = f"<h3>来自 @{username} 的分享</h3>"
    
    # Insert Generated Illustration at the Top
    if illustration_url:
        content_html += f"<figure class='wp-block-image size-large'><img src='{illustration_url}' alt='AI Generated Illustration' style='max-width:100%; height:auto; border-radius:8px; margin-bottom:20px;' /><figcaption>AI Generated Illustration</figcaption></figure>"

    content_html += summary["summary_html"]
    
    content_html += f"<h5>原文内容</h5>"
    
    # Reassemble Original Content
    if tweet_data["type"] == "article":
        # For Articles: Assemble the HTML parts and inject images
        # The placeholders are {{IMAGE_PLACEHOLDER:URL}}
        
        article_html = ""
        html_parts = tweet_data.get("html_parts", [])
        
        for part in html_parts:
            # We must handle placeholders inside the string parts
            # Since html_parts is a list of strings, some of which are placeholders
            if part.startswith("{{IMAGE_PLACEHOLDER:") and part.endswith("}}"):
                # Extract URL
                orig_url = part[20:-2] # Remove prefix and suffix
                wp_url = uploaded_map.get(orig_url, orig_url) # Fallback to orig if upload failed
                article_html += f"<img src='{wp_url}' style='max-width:100%; margin:10px 0; display:block; border-radius:4px;' />"
            else:
                article_html += part
                
        content_html += f"<div class='twitter-article'>{article_html}</div>"
        
    else:
        # For Standard Tweets: Text + Appended Images
        original_text = tweet_data["text"]
        text_html = original_text.replace(chr(10), '<br>')
        
        images_html = ""
        sorted_images = tweet_data["images"] # Keep original order
        if sorted_images:
            images_html += "<div style='margin-top:15px;'>"
            for img_url in sorted_images:
                wp_url = uploaded_map.get(img_url)
                if wp_url:
                    images_html += f"<img src='{wp_url}' style='max-width:100%; margin-bottom:10px; display:block; border-radius:4px;' />"
            images_html += "</div>"
            
        content_html += f"<blockquote>{text_html}{images_html}</blockquote>"

    content_html += f"<p>原文链接: <a href='{tweet_url}'>{tweet_url}</a></p>"

    # 6. Publish
    post = WordPressPost()
    post.title = post_title
    post.content = content_html
    post.post_status = 'publish'
    post.terms_names = {
        'category': ['AI News'],
        'post_tag': ['AI', 'Twitter', 'Summary']
    }
    
    try:
        print(f"Publishing to WordPress: {post_title}...")
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Post published! Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Publish Failed: {e}")
        if "400" in str(e) or "taxonomies" in str(e).lower():
             print("Retrying without tags/categories...")
             post.terms_names = {}
             try:
                post_id = client.call(posts.NewPost(post))
                print(f"SUCCESS (Retry): Post published! Link: {WP_URL}/?p={post_id}")
             except Exception as e2:
                print(f"Retry Failed: {e2}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 share_tweet_to_wordpress.py <tweet_url>")
    else:
        run(sys.argv[1])
