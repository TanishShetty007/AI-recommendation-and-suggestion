import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import db
from models.product import Product
from models.wishlist import Wishlist
from models.alert import PriceAlert
from models.search import SearchQuery
from services.ecommerce_service import ECommerceService
from services.gemini_service import GeminiService

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    # If we have less than a few products, search for trending items to populate the page
    if Product.query.count() < 8:
        ECommerceService.search_products(query="trending consumer electronics", selected_category="Electronics")
    
    # Get featured deals (live data recently cached)
    featured = Product.query.order_by(Product.id.desc()).limit(4).all()
    
    # Get some AI Recommended products for the homepage
    ai_recs = Product.query.order_by(Product.rating.desc()).limit(3).all()
    
    # Inject AI explanations for homepage recommendations
    for p in ai_recs:
        p.ai_badge = p.specifications_dict().get("Best For", "Top Pick")
        p.ai_explanation = f"Matches maximum battery capacity and stellar photography review scores this week."

    return render_template('pages/index.html', featured=featured, ai_recs=ai_recs)

@pages_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', 'All')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    brand = request.args.get('brand')
    sort_by = request.args.get('sort_by')

    # Save to search query dashboard history if logged in or guest
    if query:
        uid = current_user.id if current_user.is_authenticated else None
        sq = SearchQuery(user_id=uid, query=query)
        db.session.add(sq)
        db.session.commit()

    products = ECommerceService.search_products(
        query=query,
        selected_category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        brand=brand,
        sort_by=sort_by
    )

    # Get distinct brands and categories for filtering sidebars
    all_brands = db.session.query(Product.brand).distinct().all()
    brands = [b[0] for b in all_brands if b[0]]
    
    all_categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in all_categories if c[0]]

    return render_template('pages/search.html', 
                           products=products, 
                           query=query, 
                           selected_category=category,
                           brands=brands,
                           categories=categories,
                           min_price=min_price,
                           max_price=max_price,
                           selected_brand=brand,
                           sort_by=sort_by)

@pages_bp.route('/product/<product_key>')
def product_detail(product_key):
    product = Product.query.filter_by(product_key=product_key).first_or_404()
    
    # Get specifications dictionary helper
    specs_dict = product.specifications_dict()
    
    # Retrieve AI Summary and Pros & Cons using GeminiService
    ai_summary = GeminiService.get_product_summary(product.name, specs_dict, product.description)
    pros_cons = GeminiService.get_pros_and_cons(product.name, specs_dict)
    
    # Retrieve Price History data points grouped by platform
    histories = product.price_histories
    price_data = {}
    for hist in histories:
        if hist.platform not in price_data:
            price_data[hist.platform] = []
        price_data[hist.platform].append({
            "date": hist.recorded_at.strftime("%Y-%m-%d"),
            "price": hist.price
        })

    # Sort each platform's pricing lists chronologically
    for plat in price_data:
        price_data[plat].sort(key=lambda d: d["date"])

    # Determine if this product is in the current user's wishlist
    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, product_id=product.id).first() is not None

    return render_template('pages/product_detail.html',
                           product=product,
                           specs=specs_dict,
                           ai_summary=ai_summary,
                           pros_cons=pros_cons,
                           price_data=price_data,
                           in_wishlist=in_wishlist)

@pages_bp.route('/compare')
def compare():
    # Retrieve products to compare from query parameters keys: ?ids=1,2,3
    ids_raw = request.args.get('ids', '')
    product_ids = []
    if ids_raw:
        try:
            product_ids = [int(x) for x in ids_raw.split(',') if x.strip()]
        except:
            product_ids = []

    products = []
    if product_ids:
        products = Product.query.filter(Product.id.in_(product_ids)).all()

    # Limit to maximum of 4 products
    products = products[:4]

    # Build specs dicts and collect all spec keys for template columns
    all_spec_keys = set()
    for p in products:
        p.specs = p.specifications_dict()
        all_spec_keys.update(p.specs.keys())
    spec_keys = sorted(all_spec_keys)

    # Generate AI Verdict if we have at least 2 products
    ai_analysis = ""
    if len(products) >= 2:
        ai_analysis = GeminiService.get_comparison_verdict(products)

    return render_template('pages/compare.html', products=products, spec_keys=spec_keys, ai_analysis=ai_analysis)

@pages_bp.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    # If POST, we generate recommendations based on preference answers
    recommendations_list = []
    ai_advice = ""
    budget = request.form.get('budget', '80000')
    category = request.form.get('category', 'Mobiles')
    usage = request.form.get('usage', 'Gaming')
    battery = request.form.get('battery', 'High')

    show_results = False

    if request.method == 'POST':
        show_results = True
        # Retrieve target advice
        ai_advice = GeminiService.get_recommendation_advice(budget, category, usage, battery)
        
        # Pull matching products under budget
        all_prods = Product.query.filter_by(category=category).all()
        for p in all_prods:
            prices = [v for v in [p.amazon_price, p.flipkart_price, p.reliance_price, p.croma_price, p.vijaysales_price] if v is not None]
            min_price = min(prices) if prices else 0.0
            if min_price <= float(budget):
                # Calculate an AI suitability score based on specs vs preferences
                score = 80
                specs = p.specifications_dict()
                
                # Check for usage match
                if usage == "Gaming":
                    if "Snapdragon 8" in specs.get("Processor", "") or "A16" in specs.get("Processor", "") or "M2" in specs.get("Processor", ""):
                        score += 15
                elif usage == "Photography":
                    if "48MP" in specs.get("Camera", "") or "50MP" in specs.get("Camera", ""):
                        score += 15
                
                # Check for battery match
                if battery == "High":
                    bat_val = specs.get("Battery", "")
                    if "5000" in bat_val or "5500" in bat_val or "18 hours" in bat_val:
                        score += 10

                p.ai_score = min(score, 99)
                p.min_price = min_price
                recommendations_list.append(p)

        # Sort by AI score
        recommendations_list.sort(key=lambda p: p.ai_score, reverse=True)

    return render_template('pages/recommendations.html',
                           show_results=show_results,
                           products=recommendations_list,
                           ai_advice=ai_advice,
                           budget=budget,
                           category=category,
                           usage=usage,
                           battery=battery)

@pages_bp.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    alerts = PriceAlert.query.filter_by(user_id=current_user.id).all()

    return render_template('pages/wishlist.html', wishlist_items=wishlist_items, alerts=alerts)

@pages_bp.route('/dashboard')
@login_required
def dashboard():
    # Aggregate statistics
    search_count = SearchQuery.query.filter_by(user_id=current_user.id).count()
    wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()
    alert_count = PriceAlert.query.filter_by(user_id=current_user.id, is_active=True).count()
    
    # Calculate mock total money saved
    money_saved = wishlist_count * 1850 + search_count * 150

    # Retrieve recent search history
    search_queries = SearchQuery.query.filter_by(user_id=current_user.id).order_by(SearchQuery.timestamp.desc()).limit(5).all()

    # Category distributions and mock trend lists
    categories_data = [
        {"name": "Mobiles", "percentage": 45},
        {"name": "Laptops", "percentage": 30},
        {"name": "Electronics", "percentage": 15},
        {"name": "Fashion", "percentage": 5},
        {"name": "Others", "percentage": 5}
    ]

    return render_template('pages/dashboard.html',
                           search_count=search_count,
                           wishlist_count=wishlist_count,
                           alert_count=alert_count,
                           money_saved=money_saved,
                           search_queries=search_queries,
                           categories_data=categories_data)

@pages_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handles updating profiles
        username = request.form.get('username')
        email = request.form.get('email')
        categories = request.form.getlist('preferred_categories') # array of boxes checked
        budget_min = request.form.get('budget_min', type=float)
        budget_max = request.form.get('budget_max', type=float)

        current_user.username = username
        current_user.email = email
        current_user.preferred_categories = ",".join(categories)
        if budget_min is not None:
            current_user.budget_min = budget_min
        if budget_max is not None:
            current_user.budget_max = budget_max

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('pages.profile'))

    # Load categories array
    pref_cats = current_user.preferred_categories.split(',') if current_user.preferred_categories else []
    
    return render_template('pages/profile.html', pref_categories=pref_cats)

@pages_bp.route('/settings')
@login_required
def settings():
    return render_template('pages/settings.html')

@pages_bp.route('/notifications')
@login_required
def notifications():
    alerts = PriceAlert.query.filter_by(user_id=current_user.id).all()
    return render_template('pages/notifications.html', alerts=alerts)

@pages_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


# Utility helper inject spec dictionary
def parse_specs(self):
    import json
    if not self.specifications:
        return {}
    try:
        return json.loads(self.specifications)
    except:
        return {"Details": self.specifications}

Product.specifications_dict = parse_specs
