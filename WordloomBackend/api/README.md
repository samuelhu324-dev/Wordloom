
# Wordloom API (FastAPI minimal)

## Run locally
```bash
cd wordloom_api
python -m venv .venv && . .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Default demo credentials:
- USER: admin
- PASS: admin123
- TOKEN: devtoken123

## Endpoints
- GET  /health
- POST /auth/login
- POST /entries           (Bearer token required)
- GET  /entries/recent    (Bearer token required)
- GET  /sources           (Bearer token required)
- PATCH /sources/rename   (Bearer token required)
