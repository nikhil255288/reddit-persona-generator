# 🧠 Reddit Persona Generator

A Flask + LLaMA-powered AI project that generates a **persona profile** for any Reddit user, based on their posts and comments. Just input a Reddit profile link and get a styled persona card with traits, motivations, frustrations, and goals — downloadable as PDF!

---

## 🚀 Features

✅ **Live Reddit Data Scraping** with [PRAW](https://praw.readthedocs.io/)  
✅ **Local LLM integration** using [Ollama + LLaMA 3](https://ollama.com/)  
✅ **AI Persona Generation** (Archetype, Quote, Traits, Goals, Frustrations)  
✅ **Frontend Styling** with HTML/CSS and persona layout  
✅ **PDF Export** using `pdfkit` and `wkhtmltopdf`  
✅ **Dynamic Avatars** via Reddit profile or DiceBear fallback  
✅ **Frontend Deployed** on Netlify  
✅ **GitHub Project with Clean Commit History**  
✅ **Environment Variables via `.env`**  
✅ **Fully Modular Backend-Frontend Separation**

---

## 🌐 Deployment

| Service     | Status       | Link                                       |
|-------------|--------------|--------------------------------------------|
| 🔗 GitHub   | ✅ Pushed     | [GitHub Repo](https://github.com/nikhil255288/reddit-persona-generator) |
| 🌍 Frontend | ✅ Live       | [Netlify](https://reddit-persona-generator.netlify.app/) |
| ⚙️ Backend  | ❌ Local Only | LLaMA 3 via Ollama (Not yet deployed)     |

> 📝 Note: Backend uses `ollama` which currently runs locally; not deployable on Render or Replit.

---

## 🧪 How It Works

1. 🔗 User submits a Reddit profile link  
2. 🧠 Backend fetches posts + comments using PRAW  
3. 🤖 Local LLM (LLaMA 3 via Ollama) generates a concise persona dictionary  
4. 📄 Persona displayed with HTML/CSS, downloadable as PDF  
5. 🧍‍♂️ Traits, goals, and frustrations styled in card layout  

---

## 📸 Screenshots

| Result 1 | Result 2 | Result 3 |
|----------|----------|----------|
| ![screenshot1](client/screenshots/screenshot1.png) | ![screenshot2](client/screenshots/screenshot2.png) | ![screenshot3](client/screenshots/screenshot3.png) |

---

## 📂 Folder Structure

