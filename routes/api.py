from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db
from models.product import Product
from models.wishlist import Wishlist
from models.alert import PriceAlert
from models.search import SearchQuery

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/wishlist/toggle', methods=['POST'])
@login_required
def toggle_wishlist():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
        
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
        
    entry = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if entry:
        db.session.delete(entry)
        
        # Also clean up price alert if any
        alert = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if alert:
            db.session.delete(alert)
            
        db.session.commit()
        return jsonify({'status': 'success', 'added': False, 'message': 'Product removed from wishlist'})
    else:
        new_entry = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'status': 'success', 'added': True, 'message': 'Product added to wishlist'})

@api_bp.route('/wishlist/alert', methods=['POST'])
@login_required
def update_wishlist_alert():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    target_price = data.get('target_price')
    is_active = data.get('is_active', True)

    if not product_id or target_price is None:
        return jsonify({'error': 'Product ID and Target Price are required'}), 400

    alert = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if alert:
        alert.target_price = float(target_price)
        alert.is_active = bool(is_active)
    else:
        alert = PriceAlert(
            user_id=current_user.id,
            product_id=product_id,
            target_price=float(target_price),
            is_active=bool(is_active)
        )
        db.session.add(alert)
        
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Alert threshold updated successfully'})

@api_bp.route('/wishlist/remove', methods=['POST'])
@login_required
def remove_wishlist():
    data = request.get_json() or {}
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    entry = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not entry:
        return jsonify({'error': 'Product not found in wishlist'}), 404

    db.session.delete(entry)
    
    # Also delete alert
    alert = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if alert:
        db.session.delete(alert)

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Item deleted from wishlist'})

@api_bp.route('/dashboard/analytics', methods=['GET'])
@login_required
def dashboard_analytics():
    # Returns data points for the dashboard charts package
    # Chart 1: Daily Search Trends (last 7 days query count)
    search_labels = ["Jul 29", "Jul 30", "Jul 31", "Aug 01", "Aug 02", "Aug 03", "Aug 04"]
    search_data = [5, 8, 12, 6, 14, 18, 22] # Mock query numbers
    
    # Chart 2: Category distribution percentage
    # (Matches what pages.py dashboard uses but formatted clean)
    category_labels = ["Mobiles", "Laptops", "Electronics", "Fashion", "Others"]
    category_data = [45, 30, 15, 5, 5]
    
    return jsonify({
        'status': 'success',
        'search_trends': {
            'labels': search_labels,
            'data': search_data
        },
        'categories': {
            'labels': category_labels,
            'data': category_data
        }
    })
