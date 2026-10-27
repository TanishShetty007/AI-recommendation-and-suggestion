# wsgi.py - Entry point for production WSGI servers (Gunicorn / AWS Elastic Beanstalk)
from app import create_app

application = create_app()  # EB expects the variable to be named 'application'

if __name__ == "__main__":
    application.run()
