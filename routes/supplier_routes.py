from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Medicine, Supplier, SupplierCatalog, RestockOrder, StoreInventory
from routes.auth_routes import login_required, role_required

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')

def get_current_supplier():
    supplier_id = session.get('supplier_id')
    if not supplier_id:
        supplier = Supplier.query.filter_by(user_id=session.get('user_id')).first()
        if supplier:
            session['supplier_id'] = supplier.id
            session['supplier_name'] = supplier.company_name
            return supplier
    else:
        return db.session.get(Supplier, supplier_id)
    return None


@supplier_bp.route('/dashboard')
@login_required
@role_required('supplier')
def dashboard():
    supplier = get_current_supplier()
    if not supplier:
        flash('Supplier profile not found.', 'danger')
        return redirect(url_for('customer.index'))

    catalog_items = SupplierCatalog.query.filter_by(supplier_id=supplier.id).all()
    total_items = len(catalog_items)
    total_stock_units = sum(item.stock_units for item in catalog_items)

    pending_orders = RestockOrder.query.filter_by(
        supplier_id=supplier.id, status='Pending'
    ).count()

    active_orders = RestockOrder.query.filter(
        RestockOrder.supplier_id == supplier.id,
        RestockOrder.status.in_(['Accepted', 'Dispatched'])
    ).count()

    recent_orders = RestockOrder.query.filter_by(supplier_id=supplier.id)\
        .order_by(RestockOrder.created_at.desc()).limit(6).all()

    return render_template(
        'supplier/dashboard.html',
        supplier=supplier,
        total_items=total_items,
        total_stock_units=total_stock_units,
        pending_orders=pending_orders,
        active_orders=active_orders,
        recent_orders=recent_orders
    )


@supplier_bp.route('/catalog', methods=['GET', 'POST'])
@login_required
@role_required('supplier')
def catalog():
    supplier = get_current_supplier()
    if not supplier:
        return redirect(url_for('customer.index'))

    if request.method == 'POST':
        medicine_id = request.form.get('medicine_id', type=int)
        wholesale_rate = request.form.get('wholesale_rate', type=float)
        min_order_qty = request.form.get('min_order_qty', 50, type=int)
        stock_units = request.form.get('stock_units', 500, type=int)
        batch_no = request.form.get('batch_no', '').strip()

        existing = SupplierCatalog.query.filter_by(
            supplier_id=supplier.id, medicine_id=medicine_id
        ).first()

        if existing:
            existing.wholesale_rate = wholesale_rate
            existing.min_order_qty = min_order_qty
            existing.stock_units += stock_units
            if batch_no:
                existing.batch_no = batch_no
            flash('Catalog item updated.', 'success')
        else:
            new_item = SupplierCatalog(
                supplier_id=supplier.id,
                medicine_id=medicine_id,
                wholesale_rate=wholesale_rate,
                min_order_qty=min_order_qty,
                stock_units=stock_units,
                batch_no=batch_no
            )
            db.session.add(new_item)
            flash('Medicine added to wholesale catalog.', 'success')

        db.session.commit()
        return redirect(url_for('supplier.catalog'))

    catalog_items = SupplierCatalog.query.filter_by(supplier_id=supplier.id).all()
    all_medicines = Medicine.query.order_by(Medicine.name).all()

    return render_template(
        'supplier/catalog.html',
        supplier=supplier,
        catalog_items=catalog_items,
        all_medicines=all_medicines
    )


@supplier_bp.route('/catalog/edit/<int:item_id>', methods=['POST'])
@login_required
@role_required('supplier')
def edit_catalog(item_id):
    supplier = get_current_supplier()
    item = SupplierCatalog.query.filter_by(id=item_id, supplier_id=supplier.id).first_or_404()

    item.wholesale_rate = request.form.get('wholesale_rate', item.wholesale_rate, type=float)
    item.min_order_qty = request.form.get('min_order_qty', item.min_order_qty, type=int)
    item.stock_units = request.form.get('stock_units', item.stock_units, type=int)
    item.batch_no = request.form.get('batch_no', item.batch_no).strip()

    db.session.commit()
    flash(f'Updated {item.medicine.name} in wholesale catalog.', 'success')
    return redirect(url_for('supplier.catalog'))


@supplier_bp.route('/orders')
@login_required
@role_required('supplier')
def orders():
    supplier = get_current_supplier()
    if not supplier:
        return redirect(url_for('customer.index'))

    status_filter = request.args.get('status', 'all')
    orders_query = RestockOrder.query.filter_by(supplier_id=supplier.id)

    if status_filter != 'all':
        orders_query = orders_query.filter_by(status=status_filter)

    orders_list = orders_query.order_by(RestockOrder.created_at.desc()).all()

    return render_template('supplier/orders.html', supplier=supplier, orders=orders_list, status_filter=status_filter)


@supplier_bp.route('/orders/update/<int:order_id>', methods=['POST'])
@login_required
@role_required('supplier')
def update_order_status(order_id):
    supplier = get_current_supplier()
    order = RestockOrder.query.filter_by(id=order_id, supplier_id=supplier.id).first_or_404()
    new_status = request.form.get('status')

    valid_statuses = ['Accepted', 'Dispatched', 'Delivered', 'Cancelled']
    if new_status in valid_statuses:
        order.status = new_status

        # If Delivered, automatically credit the store inventory!
        if new_status == 'Delivered':
            store_inv = StoreInventory.query.filter_by(
                store_id=order.store_id, medicine_id=order.medicine_id
            ).first()

            if store_inv:
                store_inv.stock_quantity += order.quantity
            else:
                # Add as new item to store inventory with standard markup
                new_inv = StoreInventory(
                    store_id=order.store_id,
                    medicine_id=order.medicine_id,
                    selling_price=round(order.unit_price * 1.25, 2), # 25% margin
                    stock_quantity=order.quantity,
                    min_threshold=10
                )
                db.session.add(new_inv)

        db.session.commit()
        flash(f'Order #{order.id} updated to "{new_status}".', 'success')

    return redirect(url_for('supplier.orders'))
