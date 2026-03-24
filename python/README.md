# Stellar Spark Match - API Backend

This is the API backend powering the Stellar Spark Match platform. It is built as a complete replacement for the previous Express/Prisma architecture.

## Tech Stack
- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy** (SQLite local storage)
- **python-socketio** (ASGI Real-time server)
- **Firebase Admin SDK** (Token verification)

## Local Development Setup

1. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment & Secrets**
   - Place your `firebase-credentials.json` at the root.
   - Configure `.env` with `GOOGLE_APPLICATION_CREDENTIALS=./firebase-credentials.json`.

3. **Run Server**
   ```bash
   uvicorn main:sio_app --host 0.0.0.0 --port 8000 --reload
   ```

## Production Deployment
To easily run this API without installing Python dependencies manually:
```bash
docker-compose up --build -d
```
