# EduRAG – Intelligent Tutor Using RAG and LangChain

EduRAG is a Django-based backend system for an AI-powered educational tutor that uses Retrieval-Augmented Generation (RAG) and LLMs (like Hugging Face) to provide smart, context-aware answers to student queries.

---

## Features

- Upload lesson content with metadata (topic, grade, etc.)
- Store documents in SQLite database
- Vector embedding via `sentence-transformers`
- Semantic retrieval with FAISS
- Context-aware QA with Hugging Face LLMs
- Configurable tutor personas (friendly, strict, humorous)
- REST API endpoints for uploading content and asking questions

---

## Local Deployment

Locally setup backend using **Gunicorn** + **Nginx**

---

### Requirements

- Python 3.12+
- Django installed
- Setup virtual environment with `python -m venv env`
- Install requirements `pip install -r requirements.txt`
- Gunicorn: `pip install gunicorn`
- Nginx: Install nginx `sudo pacman -S nginx`[Arch]  (A quick google will help for other linux distribution)
- Start Nginx with `sudo systemctl nginx start`

---
### Setup Nginx
- Configuration file for nginx is located as `/etc/nginx/`
- Create directory as `/etc/nginx/sites-available/` and `/etc/nginx/sites-enabled/`
- inside `sites-available` create a config file named `edurag` (Name can be anything you like)
- Add the content below 
```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
	proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

}
```

- Create symlink `sudo ln -s /etc/nginx/sites-available/edurag /etc/nginx/sites-enabled/`
- Check for syntax error on nginx `sudo nginx -t`
- Reload `sudo systemctl reload nginx`
- Start gunicorn at 8000 port
```
    gunicorn edurag.wsgi:application --bind 127.0.0.1:8000
```
- Now you should see the project homepage at `localhost:80` which is redirected from `localhost:8000`