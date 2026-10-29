from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Medicine, Store, StoreInventory, Reservation, Supplier, SupplierCatalog, RestockOrder
from routes.auth_routes import login_required, role_required

store_bp = Blueprint('store', __name__, url_prefix='/store')

def get_current_store():
    store_id = session.get('store_id')
    if not store_id:
        store = Store.query.filter_by(user_id=session.get('user_id')).first()
        if store:
            session['store_id'] = store.id
            session['store_name'] = store.store_name
            return store
    else:
        return db.session.get(Store, store_id)
    return None


@store_bp.route('/dashboard')
@login_required
@role_required('store')
def dashboard():
    store = get_current_store()
    if not store:
        flash('Store profile not found. Please register your store.', 'danger')
        return redirect(url_for('customer.index'))

    # Stats
    inventory_items = StoreInventory.query.filter_by(store_id=store.id).all()
    total_medicines = len(inventory_items)
    total_units = sum(item.stock_quantity for item in inventory_items)
    
    # Low stock items (< threshold)
    low_stock_items = [item for item in inventory_items if item.is_low_stock]

    # Customer reservations
    pending_reservations = Reservation.query.filter_by(
        store_id=store.id, status='Reserved'
    ).count()

    # Restock orders
    active_restocks = RestockOrder.query.filter(
        RestockOrder.store_id == store.id,
        RestockOrder.status.in_(['Pending', 'Accepted', 'Dispatched'])
    ).count()

    recent_reservations = Reservation.query.filter_by(store_id=store.id)\
        .order_by(Reservation.created_at.desc()).limit(5).all()

    return render_template(
        'store/dashboard.html',
        store=store,
        total_medicines=total_medicines,
        total_units=total_units,
        low_stock_count=len(low_stock_items),
        low_stock_items=low_stock_items,
        pending_reservations=pending_reservations,
        active_restocks=active_restocks,
        recent_reservations=recent_reservations
    )


@store_bp.route('/inventory', methods=['GET', 'POST'])
@login_required
@role_required('store')
def inventory():
    store = get_current_store()
    if not store:
        return redirect(url_for('customer.index'))

    if request.method == 'POST':
        # Add new item to inventory
        medicine_id = request.form.get('medicine_id', type=int)
        selling_price = request.form.get('selling_price', type=float)
        stock_quantity = request.form.get('stock_quantity', 0, type=int)
        min_threshold = request.form.get('min_threshold', 10, type=int)
        batch_no = request.form.get('batch_no', '').strip()
        expiry_date = request.form.get('expiry_date', '').strip()

        # Check if already in inventory
        existing = StoreInventory.query.filter_by(
            store_id=store.id, medicine_id=medicine_id
        ).first()

        if existing:
            existing.stock_quantity += stock_quantity
            existing.selling_price = selling_price
            if batch_no:
                existing.batch_no = batch_no
            if expiry_date:
                existing.expiry_date = expiry_date
            flash('Inventory item updated successfully.', 'success')
        else:
            new_item = StoreInventory(
                store_id=store.id,
                medicine_id=medicine_id,
                selling_price=selling_price,
                stock_quantity=stock_quantity,
                min_threshold=min_threshold,
                batch_no=batch_no,
                expiry_date=expiry_date
            )
            db.session.add(new_item)
            flash('Medicine added to your store inventory.', 'success')

        db.session.commit()
        return redirect(url_for('store.inventory'))

    # GET inventory
    filter_type = request.args.get('filter', 'all')
    search_q = request.args.get('q', '').strip()

    inv_query = StoreInventory.query.join(Medicine).filter(StoreInventory.store_id == store.id)

    if search_q:
        inv_query = inv_query.filter(
            (Medicine.name.ilike(f"%{search_q}%")) |
            (Medicine.generic_name.ilike(f"%{search_q}%"))
        )

    all_items = inv_query.all()
    if filter_type == 'low_stock':
        all_items = [item for item in all_items if item.is_low_stock]

    # All medicines for add modal dropdown
    all_medicines = Medicine.query.order_by(Medicine.name).all()

    return render_template(
        'store/inventory.html',
        store=store,
        inventory_items=all_items,
        all_medicines=all_medicines,
        filter_type=filter_type,
        search_q=search_q
    )


@store_bp.route('/inventory/edit/<int:item_id>', methods=['POST'])
@login_required
@role_required('store')
def edit_inventory(item_id):
    store = get_current_store()
    item = StoreInventory.query.filter_by(id=item_id, store_id=store.id).first_or_404()

    item.selling_price = request.form.get('selling_price', item.selling_price, type=float)
    item.stock_quantity = request.form.get('stock_quantity', item.stock_quantity, type=int)
    item.min_threshold = request.form.get('min_threshold', item.min_threshold, type=int)
    item.batch_no = request.form.get('batch_no', item.batch_no).strip()
    item.expiry_date = request.form.get('expiry_date', item.expiry_date).strip()

    db.session.commit()
    flash(f'Inventory updated for {item.medicine.name}.', 'success')
    return redirect(url_for('store.inventory'))


@store_bp.route('/inventory/delete/<int:item_id>', methods=['POST'])
@login_required
@role_required('store')
def delete_inventory(item_id):
    store = get_current_store()
    item = StoreInventory.query.filter_by(id=item_id, store_id=store.id).first_or_404()
    med_name = item.medicine.name

    db.session.delete(item)
    db.session.commit()
    flash(f'{med_name} removed from your inventory.', 'info')
    return redirect(url_for('store.inventory'))


@store_bp.route('/restock', methods=['GET', 'POST'])
@login_required
@role_required('store')
def restock():
    store = get_current_store()
    if not store:
        return redirect(url_for('customer.index'))

    if request.method == 'POST':
        supplier_id = request.form.get('supplier_id', type=int)
        medicine_id = request.form.get('medicine_id', type=int)
        quantity = request.form.get('quantity', type=int)
        unit_price = request.form.get('unit_price', type=float)
        notes = request.form.get('notes', '').strip()

        # Check wholesale catalog minimums
        listing = SupplierCatalog.query.filter_by(
            supplier_id=supplier_id, medicine_id=medicine_id
        ).first()

        if listing and quantity < listing.min_order_qty:
            flash(f'Minimum order quantity for this item is {listing.min_order_qty} units.', 'warning')
            return redirect(url_for('store.restock'))

        total_amount = round(quantity * unit_price, 2)

        order = RestockOrder(
            store_id=store.id,
            supplier_id=supplier_id,
            medicine_id=medicine_id,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            status='Pending',
            notes=notes
        )
        db.session.add(order)
        db.session.commit()

        flash(f'Restock order #{order.id} sent to supplier! Total: ₹{total_amount:.2f}', 'success')
        return redirect(url_for('store.restock'))

    # Pre-select medicine if coming from low-stock click
    preselected_med_id = request.args.get('med_id', type=int)

    # Wholesale catalog listings from verified suppliers
    catalog_query = SupplierCatalog.query.join(Supplier).filter(Supplier.is_verified == True)
    if preselected_med_id:
        catalog_query = catalog_query.filter(SupplierCatalog.medicine_id == preselected_med_id)

    available_supplies = catalog_query.all()

    # My restock order history
    orders = RestockOrder.query.filter_by(store_id=store.id)\
        .order_by(RestockOrder.created_at.desc()).all()

    return render_template(
        'store/restock.html',
        store=store,
        available_supplies=available_supplies,
        orders=orders,
        preselected_med_id=preselected_med_id
    )


@store_bp.route('/reservations')
@login_required
@role_required('store')
def reservations():
    store = get_current_store()
    if not store:
        return redirect(url_for('customer.index'))

    status_filter = request.args.get('status', 'all')
    res_query = Reservation.query.filter_by(store_id=store.id)

    if status_filter != 'all':
        res_query = res_query.filter_by(status=status_filter)

    reservations_list = res_query.order_by(Reservation.created_at.desc()).all()

    return render_template('store/reservations.html', store=store, reservations=reservations_list, status_filter=status_filter)


@store_bp.route('/reservations/update/<int:res_id>', methods=['POST'])
@login_required
@role_required('store')
def update_reservation_status(res_id):
    store = get_current_store()
    reservation = Reservation.query.filter_by(id=res_id, store_id=store.id).first_or_404()
    new_status = request.form.get('status')

    if new_status in ['Ready for Pickup', 'Completed', 'Cancelled']:
        # If cancelled, restore stock
        if new_status == 'Cancelled' and reservation.status != 'Cancelled':
            inv = StoreInventory.query.filter_by(
                store_id=store.id, medicine_id=reservation.medicine_id
            ).first()
            if inv:
                inv.stock_quantity += reservation.quantity

        reservation.status = new_status
        db.session.commit()
        flash(f'Reservation {reservation.reservation_code} updated to "{new_status}".', 'success')

    return redirect(url_for('store.reservations'))
