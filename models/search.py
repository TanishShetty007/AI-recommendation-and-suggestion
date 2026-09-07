from datetime import datetime
from models import db

class SearchQuery(db.Model):
    __tablename__ = 'search_queries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Nullable for guest searches
    query = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'query': self.query,
            'timestamp': self.timestamp.isoformat()
        }
