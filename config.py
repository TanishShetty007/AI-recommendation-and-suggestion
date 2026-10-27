import os

class Config:
    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shopsmart-dev-only-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'shopsmart-jwt-dev-key-change-in-production'
    JWT_EXPIRATION_HOURS = 24

    # ── Database ──────────────────────────────────────────────────────────────
    # Uses AWS RDS MySQL when MYSQL_* env vars are set; falls back to SQLite for local dev.
    MYSQL_HOST     = os.environ.get('MYSQL_HOST')
    MYSQL_USER     = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB       = os.environ.get('MYSQL_DB', 'shopsmart_db')
    MYSQL_PORT     = os.environ.get('MYSQL_PORT', '3306')

    if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        )
    else:
        # Local SQLite fallback – NOT suitable for multi-instance AWS deployments
        BASE_DIR     = os.path.abspath(os.path.dirname(__file__))
        INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
        os.makedirs(INSTANCE_DIR, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'shopsmart.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Recycle connections every 280s to avoid MySQL's default 8h wait_timeout
        "pool_recycle": 280,
        "pool_pre_ping": True,   # Validate connection health before use
    }

    # ── AI & External APIs ────────────────────────────────────────────────────
    GEMINI_API_KEY  = os.environ.get('GEMINI_API_KEY', '')
    SERPAPI_KEY     = os.environ.get('SERPAPI_KEY', '')

    # ── Flask Production Settings ─────────────────────────────────────────────
    DEBUG    = os.environ.get('FLASK_DEBUG', '0') == '1'
    TESTING  = False

    # ── Security Headers ──────────────────────────────────────────────────────
    SESSION_COOKIE_SECURE   = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
