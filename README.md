# 🛍️ ShopSmart AI - Intelligent Product Recommendation & Suggestion System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

**ShopSmart AI** is a next-generation e-commerce web platform that leverages **Google Gemini AI** to deliver personalized shopping recommendations, intelligent natural language search, real-time price tracking, and comprehensive side-by-side product comparisons.

---

## ✨ Features

- 🤖 **AI-Powered Recommendations**: Utilizes Google Gemini to generate hyper-personalized product suggestions based on user search history, viewing behavior, and expressed preferences.
- 🔍 **Natural Language Search**: Go beyond exact keyword matching with AI-assisted intent extraction and semantic query analysis.
- ⚖️ **Product Comparison Matrix**: Compare multiple products side-by-side with automated AI summaries of strengths, weaknesses, and value ratings.
- 📉 **Price Drop Alerts**: Set target price alerts and receive automated notification updates when prices decrease.
- ❤️ **Wishlist & Saved Items**: Organize favorite products and track updates in real-time.
- 📊 **Interactive User Dashboard**: View shopping analytics, recent searches, active price alerts, and personalized suggestion feeds.
- 🔐 **Secure Authentication**: User registration, login management, and session security powered by Flask-Login and PyJWT.
- 🗄️ **Dual Database Support**: Zero-config local SQLite for development, seamless plug-and-play MySQL integration for production.

---

## 🏗️ Project Structure

```text
├── app.py                  # Application entry point and factory
├── config.py               # Environment and database configuration
├── requirements.txt        # Project dependencies
├── .env.example            # Environment variables template
├── models/                 # SQLAlchemy database models
│   ├── alert.py            # Price alert model
│   ├── price.py            # Historical price tracking model
│   ├── product.py          # Product catalog and specs
│   ├── search.py           # User search history
│   ├── user.py             # User account & auth model
│   └── wishlist.py         # Saved items model
├── routes/                 # Flask route blueprints
│   ├── api.py              # REST API endpoints
│   ├── auth.py             # Login, register, logout routes
│   └── pages.py            # Front-end view routes
├── services/               # Core business & AI services
│   ├── ecommerce_service.py# Product management & mock data
│   ├── gemini_service.py   # Google Gemini AI integration
│   └── shopping_api.py     # External API connectors
├── static/                 # Static assets (CSS, JS, images)
│   ├── css/
│   └── js/
└── templates/              # Jinja2 HTML templates
    ├── auth/               # Login & Register views
    ├── layouts/            # Base layouts & navigation
    └── pages/              # Product, search, comparison, and dashboard views
```

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TanishShetty007/AI-recommendation-and-suggestion.git
cd AI-recommendation-and-suggestion
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and configure your settings:
- Add your **Google Gemini API Key** (obtain free from [Google AI Studio](https://aistudio.google.com/apikey)).
- Adjust secret keys or MySQL credentials if needed.

```env
SECRET_KEY=your-flask-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`. Database tables will be automatically initialized on first run.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate
- **AI & ML**: Google Generative AI (Gemini 1.5 / Flash models)
- **Database**: SQLite (default local) / MySQL (via PyMySQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5 / Modern CSS
- **Security**: PyJWT, Cryptography, Werkzeug security

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
