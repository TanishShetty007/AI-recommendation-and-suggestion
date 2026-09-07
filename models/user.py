from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(500), nullable=True)
    
    # Preferences
    preferred_categories = db.Column(db.String(550), nullable=True, default='Mobiles,Laptops,Electronics')
    budget_min = db.Column(db.Float, nullable=True, default=20000.0)
    budget_max = db.Column(db.Float, nullable=True, default=80000.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    wishlists = db.relationship('Wishlist', backref='user', lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship('PriceAlert', backref='user', lazy=True, cascade="all, delete-orphan")
    searches = db.relationship('SearchQuery', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'preferred_categories': self.preferred_categories.split(',') if self.preferred_categories else [],
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'created_at': self.created_at.isoformat()
        }
