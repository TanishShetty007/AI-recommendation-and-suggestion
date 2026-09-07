from models import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_key = db.Column(db.String(100), unique=True, nullable=False) # e.g., 'iphone-15-128gb'
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True, default=4.0)
    review_count = db.Column(db.Integer, nullable=True, default=0)
    specifications = db.Column(db.Text, nullable=True) # JSON or serialized text
    
    # Store pricing from different platforms (latest cached values)
    amazon_price = db.Column(db.Float, nullable=True)
    flipkart_price = db.Column(db.Float, nullable=True)
    reliance_price = db.Column(db.Float, nullable=True)
    croma_price = db.Column(db.Float, nullable=True)
    vijaysales_price = db.Column(db.Float, nullable=True)

    # Relationships
    wishlist_entries = db.relationship('Wishlist', backref='product', lazy=True, cascade="all, delete-orphan")
    price_histories = db.relationship('PriceHistory', backref='product', lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship('PriceAlert', backref='product', lazy=True, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)


    def to_dict(self):
        import json
        specs = {}
        if self.specifications:
            try:
                specs = json.loads(self.specifications)
            except:
                # Fallback to string if not JSON
                specs = {"details": self.specifications}
        
        return {
            'id': self.id,
            'product_key': self.product_key,
            'name': self.name,
            'brand': self.brand,
            'category': self.category,
            'image_url': self.image_url,
            'description': self.description,
            'rating': self.rating,
            'review_count': self.review_count,
            'specifications': specs,
            'platforms': {
                'Amazon': self.amazon_price,
                'Flipkart': self.flipkart_price,
                'Reliance Digital': self.reliance_price,
                'Croma': self.croma_price,
                'Vijay Sales': self.vijaysales_price
            }
        }
