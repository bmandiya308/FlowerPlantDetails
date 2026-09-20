# Bloom Atlas

A small Flask application for browsing flower details with an image-led collection and profile pages.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

Flower data currently lives in `app.py` so the app can be extended without adding a database before it is needed. Flower images are loaded from Unsplash URLs.