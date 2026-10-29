from flask import Blueprint, jsonify, request
from models import Medicine, Store, StoreInventory, Supplier

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/search-suggestions')
def search_suggestions():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])

    pattern = f"%{q}%"
    medicines = Medicine.query.filter(
        (Medicine.name.ilike(pattern)) |
        (Medicine.generic_name.ilike(pattern))
    ).limit(8).all()

    results = []
    for m in medicines:
        results.append({
            'id': m.id,
            'name': m.name,
            'generic_name': m.generic_name,
            'strength': m.strength,
            'category': m.category,
            'is_generic': m.is_generic,
            'mrp': m.default_mrp
        })

    return jsonify(results)


@api_bp.route('/stores')
def get_stores():
    city = request.args.get('city', '').strip()
    query = Store.query.filter_by(is_verified=True)

    if city:
        query = query.filter(Store.city.ilike(f"%{city}%"))

    stores = query.all()
    results = []
    for s in stores:
        item_count = s.inventory.count()
        results.append({
            'id': s.id,
            'name': s.store_name,
            'address': s.address,
            'city': s.city,
            'area': s.area,
            'lat': s.latitude,
            'lng': s.longitude,
            'phone': s.phone,
            'hours': s.opening_hours,
            'medicine_count': item_count
        })

    return jsonify(results)


@api_bp.route('/medicine-stores/<int:medicine_id>')
def get_medicine_stores(medicine_id):
    inventories = StoreInventory.query.join(Store).filter(
        StoreInventory.medicine_id == medicine_id,
        Store.is_verified == True
    ).all()

    results = []
    for inv in inventories:
        results.append({
            'store_id': inv.store.id,
            'store_name': inv.store.store_name,
            'area': inv.store.area,
            'lat': inv.store.latitude,
            'lng': inv.store.longitude,
            'selling_price': inv.selling_price,
            'stock_quantity': inv.stock_quantity,
            'is_in_stock': inv.stock_quantity > 0
        })

    return jsonify(results)

