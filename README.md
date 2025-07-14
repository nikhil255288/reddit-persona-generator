# Reddit Persona Generator 🧠

A Flask-based web app that generates a user persona from any public Reddit profile using:
- 🔍 Reddit API (via PRAW) for scraping user activity
- 🧠 LLaMA 3 (via Ollama) for persona generation
- 📄 WeasyPrint/pdfkit for exporting persona to PDF

## 🌐 Features
- Enter any Reddit user profile URL
- Generates a rich persona (traits, motivations, frustrations, etc.)
- Visual persona card with PDF export
- DiceBear avatars fallback if not available

## 📦 Tech Stack
- Python (Flask)
- Jinja2, HTML/CSS
- Reddit API (PRAW)
- Ollama + LLaMA 3
- WeasyPrint/pdfkit for PDF
- Hosted locally or deployable

## 📸 Demo
![screenshot](client/static/avatar.png) <!-- Replace with your screenshot -->

## 🚀 Getting Started

```bash
git clone https://github.com/nikhil255288/reddit-persona-generator.git
cd reddit-persona-generator
pip install -r requirements.txt
