from flask import Flask, render_template, request, jsonify, make_response
from dotenv import load_dotenv
import os, re, time, praw, ollama, hashlib, pdfkit, ast

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, '../client/templates')
STATIC_FOLDER = os.path.join(BASE_DIR, '../client/static')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_SECRET'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('USER_AGENT')
)

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def extract_username(link):
    match = re.search(r"reddit\.com\/user\/([A-Za-z0-9_-]+)", link)
    return match.group(1) if match else None

def fetch_user_content(username, limit=2):
    try:
        redditor = reddit.redditor(username)
        posts = [f"[POST] {p.title}" for p in redditor.submissions.new(limit=limit)]
        comments = [f"[COMMENT] {c.body}" for c in redditor.comments.new(limit=limit)]
        return posts + comments
    except Exception as e:
        print("Reddit Scraping Error:", e)
        return []

def generate_persona(username, karma, age, user_content, retries=1):
    if not user_content:
        user_content = ["[COMMENT] No significant activity found."]

    content = "\n".join(user_content)
    prompt = f"""
Analyze the following Reddit user:

Username: {username}
Karma: {karma}
Age: {age} years

Activity:
{content}

Return a Python dictionary with:
- archetype (string)
- quote (1 line)
- personality (list of 3 traits)
- goal (1 line)
- frustration (1 line)

Only return the Python dictionary.
"""

    for attempt in range(retries + 1):
        try:
            res = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}], stream=False)
            result = res.get("message", {}).get("content", "").strip()

            if "```" in result:
                parts = result.split("```")
                for part in parts:
                    if "{" in part and "}" in part:
                        result = part
                        break

            return ast.literal_eval(result)
        except Exception as e:
            print(f"LLM Error attempt {attempt+1}:", e)
        time.sleep(2)
    return None

def save_to_txt(username, data):
    path = os.path.join(OUTPUT_FOLDER, f"{username}_persona.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"Persona for u/{username}\n\n")
        for k, v in data.items():
            f.write(f"{k.upper()}:\n{v}\n\n")
    return path

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        reddit_link = request.form.get('reddit_link')
        username = extract_username(reddit_link)
        if not username:
            return render_template('index.html', error="Invalid Reddit profile URL.")

        try:
            redditor = reddit.redditor(username)
            karma = redditor.link_karma + redditor.comment_karma
            age = int((time.time() - redditor.created_utc) // (365 * 24 * 60 * 60))
            avatar = getattr(redditor, 'icon_img', '').strip() or f"https://api.dicebear.com/7.x/thumbs/svg?seed={hashlib.md5(username.encode()).hexdigest()}"
            content = fetch_user_content(username)
        except Exception as e:
            print("Reddit API Error:", e)
            return render_template('index.html', error="Could not fetch Redditor info.")

        llm_data = generate_persona(username, karma, age, content)
        if not llm_data:
            return render_template('index.html', error="LLM failed to generate persona.")

        persona_data = {
            "name": username.title(),
            "username": username,
            "age": 25 + age,
            "occupation": "Redditor",
            "location": "Internet",
            "avatar": avatar,
            **llm_data
        }

        save_to_txt(username, persona_data)
        return render_template("persona.html", data=persona_data)

    return render_template("index.html", error=None)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    try:
        html = render_template("persona_pdf.html", data=data)
        pdf = pdfkit.from_string(html, False, configuration=PDFKIT_CONFIG)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{data.get("username")}.pdf"'
        return response
    except Exception as e:
        print("PDF Error:", e)
        return jsonify({"error": "PDF generation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
