from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to register them with the metadata
from models.user import User
from models.product import Product
from models.price import PriceHistory
from models.wishlist import Wishlist
from models.alert import PriceAlert
from models.search import SearchQuery
