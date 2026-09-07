import json
import random
from models import db
from models.product import Product
from models.price import PriceHistory

class ECommerceService:


    @staticmethod
    def search_products(query, selected_category=None, min_price=None, max_price=None, min_rating=None, brand=None, sort_by=None):
        """
        Queries SerpApi for live products.
        Stores them in the local database to use for comparison and wishlists.
        """
        from services.shopping_api import search_products as api_search_products
        
        # If no query but category specified, use category for api lookup
        # e.g for "Categories" view fetching
        api_query = query
        if not api_query and selected_category and selected_category != 'All':
            api_query = f"top {selected_category}"
        elif not api_query:
            api_query = "latest electronics"
        
        if api_query:
            try:
                live_data = api_search_products(api_query)
                if live_data and 'shopping_results' in live_data:
                    for item in live_data['shopping_results']:
                        product_id = item.get('product_id')
                        if not product_id:
                            product_id = f"serpapi-{item.get('position', random.randint(1000, 9999))}"
                            
                        db_prod = Product.query.filter_by(product_key=product_id).first()
                        if not db_prod:
                            base_p = item.get('extracted_price', 0.0)
                            prod_brand = item.get('source', 'Brand')
                            new_prod = Product(
                                product_key=product_id,
                                name=item.get('title', 'Unknown Product'),
                                brand=prod_brand,
                                category=selected_category if selected_category and selected_category != 'All' else 'Electronics',
                                image_url=item.get('thumbnail', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'),
                                description=item.get('title', ''),
                                rating=item.get('rating', round(random.uniform(3.5, 4.9), 1)),
                                review_count=item.get('reviews', random.randint(10, 500)),
                                specifications=json.dumps({"Source": item.get('source', 'Unknown')}),
                                amazon_price=base_p,
                                flipkart_price=round(base_p * random.uniform(0.95, 1.02), 2),
                                reliance_price=round(base_p * random.uniform(0.97, 1.04), 2),
                                croma_price=round(base_p * random.uniform(0.96, 1.03), 2),
                                vijaysales_price=round(base_p * random.uniform(0.98, 1.05), 2)
                            )
                            db.session.add(new_prod)
                            db.session.flush() # assign ID
                            
                            # Seed mock price history for it so charts don't break
                            from datetime import datetime, timedelta
                            prices_map = {
                                "Amazon": new_prod.amazon_price,
                                "Flipkart": new_prod.flipkart_price,
                                "Reliance Digital": new_prod.reliance_price,
                                "Croma": new_prod.croma_price,
                                "Vijay Sales": new_prod.vijaysales_price
                            }
                            for plat, current_platform_price in prices_map.items():
                                hist_price = current_platform_price
                                for days_back in range(7, -1, -1):
                                    hist_price = round(hist_price * (1 + random.uniform(-0.02, 0.02)), 2)
                                    if days_back == 0:
                                        hist_price = current_platform_price
                                    recorded_dt = datetime.utcnow() - timedelta(days=days_back)
                                    from models.price import PriceHistory
                                    hist = PriceHistory(
                                        product_id=new_prod.id,
                                        platform=plat,
                                        price=hist_price,
                                        recorded_at=recorded_dt
                                    )
                                    db.session.add(hist)
                            
                    db.session.commit()
            except Exception as e:
                print(f"SerpApi Error: {e}")

        stmt = Product.query
        
        # Apply word matching (simulating external APIs search)
        if query:
            clean_query = query.strip().lower()
            stmt = stmt.filter(db.or_(
                Product.name.ilike(f"%{clean_query}%"),
                Product.brand.ilike(f"%{clean_query}%"),
                Product.category.ilike(f"%{clean_query}%"),
                Product.description.ilike(f"%{clean_query}%")
            ))
            
        if selected_category and selected_category != 'All':
            stmt = stmt.filter(Product.category == selected_category)

        # Execute
        results = stmt.all()

        # Apply price filters, rating filters, brand filters in memory
        filtered_results = []
        for prod in results:
            # find min price across stores
            prices = [v for v in [prod.amazon_price, prod.flipkart_price, prod.reliance_price, prod.croma_price, prod.vijaysales_price] if v is not None]
            min_store_price = min(prices) if prices else 0.0

            if min_price is not None and min_store_price < min_price:
                continue
            if max_price is not None and min_store_price > max_price:
                continue
            if min_rating is not None and (prod.rating or 0.0) < min_rating:
                continue
            if brand and prod.brand and prod.brand.lower() != brand.lower():
                continue
                
            filtered_results.append(prod)

        # Sorters
        if sort_by == 'price_low':
            filtered_results.sort(key=lambda p: min([v for v in [p.amazon_price, p.flipkart_price, p.reliance_price, p.croma_price, p.vijaysales_price] if v is not None] or [0.0]))
        elif sort_by == 'price_high':
            filtered_results.sort(key=lambda p: min([v for v in [p.amazon_price, p.flipkart_price, p.reliance_price, p.croma_price, p.vijaysales_price] if v is not None] or [0.0]), reverse=True)
        elif sort_by == 'rating':
            filtered_results.sort(key=lambda p: p.rating or 0.0, reverse=True)

        return filtered_results
