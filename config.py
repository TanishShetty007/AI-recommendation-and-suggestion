import os

class Config:
    # Key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'shopsmart-secret-dev-key')
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'shopsmart-jwt-secret-key')
    JWT_EXPIRATION_HOURS = 24

    # Database Configuration
    # Defaults to local SQLite database if MySQL environment parameters are not specified
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'shopsmart_db')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')

    if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    else:
        # Fallback to local SQLite DB
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        # Ensure instance folder exists
        INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
        os.makedirs(INSTANCE_DIR, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'shopsmart.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI API Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
