import os
import sys
from app import create_app
from models import db
from models.user import User
from models.product import Product
from models.wishlist import Wishlist
from models.alert import PriceAlert
from models.search import SearchQuery
from services.ecommerce_service import ECommerceService

def run_verification():
    print("====== Starting Verification ======")
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    client = app.test_client()

    with app.app_context():
        print("1. Creating database tables in memory...")
        db.create_all()
        
        print("2. Seeding mock catalog database...")
        ECommerceService.initialize_mock_database()
        product_count = Product.query.count()
        print(f"   Created {product_count} products.")
        assert product_count > 0, "Products seeding failed."

        print("3. Creating verification test user account...")
        user = User(username="testverifier", email="verify@shopsmart.ai")
        user.set_password("verifysecret123")
        db.session.add(user)
        db.session.commit()
        print("   Created test user successfully.")

        # Test index page GET
        print("4. Testing Landing View GET /")
        res = client.get('/')
        assert res.status_code == 200, f"Landing page failed with {res.status_code}"
        assert b"ShopSmart AI" in res.data, "Landing page payload missing Brand mark."
        print("   ✓ Landing page loaded successfully.")

        # Test search query
        print("5. Testing Search GET /search?q=iPhone")
        res = client.get('/search?q=iPhone')
        assert res.status_code == 200
        assert b"iPhone" in res.data, "Search recommendations failed."
        print("   ✓ Search page returned correct listings.")

        # Test product detail page
        print("6. Testing Detail View GET /product/apple-iphone-15-128gb")
        res = client.get('/product/apple-iphone-15-128gb')
        assert res.status_code == 200, f"Detail page failed: {res.status_code}"
        assert b"iPhone 15" in res.data, "Detail page specifications wrong."
        print("   ✓ Product detail page verified successfully.")

        # Test register auth POST
        print("7. Testing Authentication Register POST")
        res = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@shopsmart.ai',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"newuser" in res.data or b"login" in res.data, "Auth register failed."
        print("   ✓ User registration blueprint verified.")

        # Test login auth POST
        print("8. Testing Authentication Login POST")
        res = client.post('/auth/login', data={
            'email': 'verify@shopsmart.ai',
            'password': 'verifysecret123'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"testverifier" in res.data, "Auth login flow failed."
        print("   ✓ User login blueprint verified.")

    print("\n====== Automated Verification Passed Successfully! ======")

if __name__ == '__main__':
    run_verification()
