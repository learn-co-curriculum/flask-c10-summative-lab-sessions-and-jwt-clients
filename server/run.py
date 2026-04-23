"""
Application entry point.

Run with:
    python run.py

Or via Flask CLI:
    flask run --port 5555
"""
import os

from dotenv import load_dotenv

# Load environment variables from .env (if present) before importing the app
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
