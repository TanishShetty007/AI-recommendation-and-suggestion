from datetime import datetime
from models import db

class PriceHistory(db.Model):
    __tablename__ = 'price_histories'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    platform = db.Column(db.String(100), nullable=False) # e.g., 'Amazon', 'Flipkart'
    price = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(PriceHistory, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'platform': self.platform,
            'price': self.price,
            'recorded_at': self.recorded_at.isoformat()
        }
