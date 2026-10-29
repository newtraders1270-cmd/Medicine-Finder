import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Medicine, Store, StoreInventory, Reservation, User, Supplier
from routes.auth_routes import login_required

customer_bp = Blueprint('customer', __name__)

def generate_reservation_code():
    return 'MED-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@customer_bp.route('/')
def index():
    # Highlights & Statistics
    total_medicines = Medicine.query.count()
    total_stores = Store.query.filter_by(is_verified=True).count()
    total_suppliers = Supplier.query.filter_by(is_verified=True).count()
    
    # Featured / Popular Medicines
    featured_medicines = Medicine.query.order_by(Medicine.name).limit(8).all()
    categories = db.session.query(Medicine.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    # All cities available
    cities = db.session.query(Store.city).distinct().all()
    cities = [c[0] for c in cities if c[0]]

    return render_template(
        'index.html',
        total_medicines=total_medicines,
        total_stores=total_stores,
        total_suppliers=total_suppliers,
        featured_medicines=featured_medicines,
        categories=categories,
        cities=cities
    )


@customer_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    city = request.args.get('city', '').strip()
    area = request.args.get('area', '').strip()
    category = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'price_asc')
    in_stock_only = request.args.get('in_stock', '0') == '1'

    if not query and not category:
        flash('Please enter a medicine name, salt/generic composition, or select a category.', 'info')
        return redirect(url_for('customer.index'))

    # Base query for medicines
    med_query = Medicine.query
    if query:
        search_pattern = f"%{query}%"
        med_query = med_query.filter(
            (Medicine.name.ilike(search_pattern)) |
            (Medicine.generic_name.ilike(search_pattern)) |
            (Medicine.uses.ilike(search_pattern)) |
            (Medicine.manufacturer.ilike(search_pattern))
        )
    if category:
        med_query = med_query.filter(Medicine.category == category)

    matching_medicines = med_query.all()
    medicine_ids = [m.id for m in matching_medicines]

    # Find store inventory entries for these medicines
    inventory_query = StoreInventory.query.join(Store).filter(
        StoreInventory.medicine_id.in_(medicine_ids),
        Store.is_verified == True
    )

    if city:
        inventory_query = inventory_query.filter(Store.city.ilike(f"%{city}%"))
    if area:
        inventory_query = inventory_query.filter(Store.area.ilike(f"%{area}%"))
    if in_stock_only:
        inventory_query = inventory_query.filter(StoreInventory.stock_quantity > 0)

    # Sorting
    if sort_by == 'price_desc':
        inventory_query = inventory_query.order_by(StoreInventory.selling_price.desc())
    elif sort_by == 'stock_desc':
        inventory_query = inventory_query.order_by(StoreInventory.stock_quantity.desc())
    else:  # default price_asc
        inventory_query = inventory_query.order_by(StoreInventory.selling_price.asc())

    inventory_results = inventory_query.all()

    # Smart Recommendation / Generic Substitute Calculation
    generic_advice = []
    # If the user searched for a specific medicine, find if cheaper generic alternatives exist
    for med in matching_medicines[:3]:
        if not med.is_generic:
            # Find generic medicines with the same generic_name
            generics = Medicine.query.filter(
                Medicine.generic_name.ilike(med.generic_name),
                Medicine.is_generic == True
            ).all()

            for gen in generics:
                # Find lowest selling price for this generic in stock
                gen_inv = StoreInventory.query.join(Store).filter(
                    StoreInventory.medicine_id == gen.id,
                    StoreInventory.stock_quantity > 0,
                    Store.is_verified == True
                ).order_by(StoreInventory.selling_price.asc()).first()

                if gen_inv and med.default_mrp > 0:
                    savings = round(med.default_mrp - gen_inv.selling_price, 2)
                    savings_pct = round((savings / med.default_mrp) * 100)
                    if savings > 0:
                        generic_advice.append({
                            'brand_medicine': med,
                            'generic_medicine': gen,
                            'generic_inventory': gen_inv,
                            'savings_amount': savings,
                            'savings_percent': savings_pct
                        })

    # Available cities & categories for filter bar
    cities = [c[0] for c in db.session.query(Store.city).distinct().all() if c[0]]
    categories = [c[0] for c in db.session.query(Medicine.category).distinct().all() if c[0]]

    # Identify Best Price Store & Nearest Store if results exist
    best_price_item = None
    if inventory_results:
        in_stock_items = [item for item in inventory_results if item.stock_quantity > 0]
        if in_stock_items:
            best_price_item = min(in_stock_items, key=lambda x: x.selling_price)

    return render_template(
        'customer/search_results.html',
        query=query,
        selected_city=city,
        selected_area=area,
        selected_category=category,
        sort_by=sort_by,
        in_stock_only=in_stock_only,
        medicines=matching_medicines,
        inventory_results=inventory_results,
        generic_advice=generic_advice,
        best_price_item=best_price_item,
        cities=cities,
        categories=categories
    )


@customer_bp.route('/medicine/<int:medicine_id>')
def medicine_detail(medicine_id):
    medicine = db.get_or_404(Medicine, medicine_id)
    
    # Stores stocking this medicine
    stock_entries = StoreInventory.query.join(Store).filter(
        StoreInventory.medicine_id == medicine.id,
        Store.is_verified == True
    ).order_by(StoreInventory.selling_price.asc()).all()

    # Find generic equivalents or branded versions with the same salt
    alternatives = Medicine.query.filter(
        Medicine.generic_name.ilike(medicine.generic_name),
        Medicine.id != medicine.id
    ).all()

    # Price stats
    prices = [entry.selling_price for entry in stock_entries if entry.stock_quantity > 0]
    min_price = min(prices) if prices else medicine.default_mrp
    max_price = max(prices) if prices else medicine.default_mrp
    total_stock = sum(entry.stock_quantity for entry in stock_entries)

    return render_template(
        'customer/medicine_detail.html',
        medicine=medicine,
        stock_entries=stock_entries,
        alternatives=alternatives,
        min_price=min_price,
        max_price=max_price,
        total_stock=total_stock
    )


@customer_bp.route('/store-locator')
def store_locator():
    city = request.args.get('city', '').strip()
    stores_query = Store.query.filter_by(is_verified=True)
    if city:
        stores_query = stores_query.filter(Store.city.ilike(f"%{city}%"))
    
    stores = stores_query.all()
    cities = [c[0] for c in db.session.query(Store.city).distinct().all() if c[0]]

    return render_template('customer/store_locator.html', stores=stores, cities=cities, selected_city=city)


@customer_bp.route('/reserve', methods=['POST'])
@login_required
def reserve_medicine():
    inventory_id = request.form.get('inventory_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    customer_notes = request.form.get('customer_notes', '').strip()

    inventory = db.get_or_404(StoreInventory, inventory_id)

    if inventory.stock_quantity < quantity:
        flash(f'Insufficient stock. Only {inventory.stock_quantity} units available at {inventory.store.store_name}.', 'danger')
        return redirect(request.referrer or url_for('customer.index'))

    # Deduct stock on reservation
    inventory.stock_quantity -= quantity
    total_price = round(inventory.selling_price * quantity, 2)
    code = generate_reservation_code()

    reservation = Reservation(
        customer_id=session['user_id'],
        store_id=inventory.store_id,
        medicine_id=inventory.medicine_id,
        quantity=quantity,
        unit_price=inventory.selling_price,
        total_price=total_price,
        reservation_code=code,
        status='Reserved',
        customer_notes=customer_notes
    )

    db.session.add(reservation)
    db.session.commit()

    flash(f'Success! Medicine reserved at {inventory.store.store_name}. Your Booking Token is {code}.', 'success')
    return redirect(url_for('customer.my_reservations'))


@customer_bp.route('/my-reservations')
@login_required
def my_reservations():
    reservations = Reservation.query.filter_by(
        customer_id=session['user_id']
    ).order_by(Reservation.created_at.desc()).all()

    return render_template('customer/my_reservations.html', reservations=reservations)
