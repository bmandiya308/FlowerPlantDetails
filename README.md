# Petal

A Flask-based garden community with a photo and video feed. Visitors can publish a post with a name, caption, and one image or video. Posts and uploaded media are stored locally in SQLite and the `instance/uploads` folder. The flower atlas remains available at `/flowers`.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

Accepted media: JPG, JPEG, PNG, GIF, WEBP, MP4, WEBM, and MOV, up to 100 MB per request. Set a strong `SECRET_KEY` environment variable outside local development. For hosted use, configure durable storage for the database and uploaded files; the included local filesystem storage is not a substitute for object storage or a persistent disk.

Run tests with:

```powershell
python -m unittest discover -s tests
```