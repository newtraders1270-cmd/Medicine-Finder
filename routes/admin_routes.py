from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Medicine, Store, Supplier, User, Reservation, RestockOrder
from routes.auth_routes import login_required, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    total_users = User.query.count()
    total_stores = Store.query.count()
    total_suppliers = Supplier.query.count()
    total_medicines = Medicine.query.count()
    total_reservations = Reservation.query.count()
    total_restocks = RestockOrder.query.count()

    # Verification requests
    pending_stores = Store.query.filter_by(is_verified=False).all()
    pending_suppliers = Supplier.query.filter_by(is_verified=False).all()

    verified_stores = Store.query.filter_by(is_verified=True).all()
    verified_suppliers = Supplier.query.filter_by(is_verified=True).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_stores=total_stores,
        total_suppliers=total_suppliers,
        total_medicines=total_medicines,
        total_reservations=total_reservations,
        total_restocks=total_restocks,
        pending_stores=pending_stores,
        pending_suppliers=pending_suppliers,
        verified_stores=verified_stores,
        verified_suppliers=verified_suppliers
    )


@admin_bp.route('/verify/<target_type>/<int:target_id>', methods=['POST'])
@login_required
@role_required('admin')
def verify_entity(target_type, target_id):
    action = request.form.get('action') # 'approve' or 'reject'
    status_value = (action == 'approve')

    if target_type == 'store':
        store = db.get_or_404(Store, target_id)
        store.is_verified = status_value
        db.session.commit()
        msg = f'Store "{store.store_name}" {"approved" if status_value else "rejected"}.'
    elif target_type == 'supplier':
        supplier = db.get_or_404(Supplier, target_id)
        supplier.is_verified = status_value
        db.session.commit()
        msg = f'Supplier "{supplier.company_name}" {"approved" if status_value else "rejected"}.'
    else:
        flash('Invalid target type.', 'danger')
        return redirect(url_for('admin.dashboard'))

    flash(msg, 'success' if status_value else 'warning')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/medicines', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def medicines():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        generic_name = request.form.get('generic_name', '').strip()
        strength = request.form.get('strength', '').strip()
        category = request.form.get('category', 'Tablet').strip()
        manufacturer = request.form.get('manufacturer', '').strip()
        default_mrp = request.form.get('default_mrp', 0.0, type=float)
        uses = request.form.get('uses', '').strip()
        dosage_info = request.form.get('dosage_info', '').strip()
        prescription_required = bool(request.form.get('prescription_required'))
        is_generic = bool(request.form.get('is_generic'))

        new_med = Medicine(
            name=name,
            generic_name=generic_name,
            strength=strength,
            category=category,
            manufacturer=manufacturer,
            default_mrp=default_mrp,
            uses=uses,
            dosage_info=dosage_info,
            prescription_required=prescription_required,
            is_generic=is_generic
        )
        db.session.add(new_med)
        db.session.commit()

        flash(f'Medicine "{name}" added to master database.', 'success')
        return redirect(url_for('admin.medicines'))

    search_q = request.args.get('q', '').strip()
    med_query = Medicine.query

    if search_q:
        med_query = med_query.filter(
            (Medicine.name.ilike(f"%{search_q}%")) |
            (Medicine.generic_name.ilike(f"%{search_q}%"))
        )

    all_medicines = med_query.order_by(Medicine.name).all()

    return render_template('admin/medicines.html', medicines=all_medicines, search_q=search_q)


@admin_bp.route('/medicines/edit/<int:med_id>', methods=['POST'])
@login_required
@role_required('admin')
def edit_medicine(med_id):
    med = db.get_or_404(Medicine, med_id)

    med.name = request.form.get('name', med.name).strip()
    med.generic_name = request.form.get('generic_name', med.generic_name).strip()
    med.strength = request.form.get('strength', med.strength).strip()
    med.category = request.form.get('category', med.category).strip()
    med.manufacturer = request.form.get('manufacturer', med.manufacturer).strip()
    med.default_mrp = request.form.get('default_mrp', med.default_mrp, type=float)
    med.uses = request.form.get('uses', med.uses).strip()
    med.dosage_info = request.form.get('dosage_info', med.dosage_info).strip()
    med.prescription_required = bool(request.form.get('prescription_required'))
    med.is_generic = bool(request.form.get('is_generic'))

    db.session.commit()
    flash(f'Medicine "{med.name}" updated.', 'success')
    return redirect(url_for('admin.medicines'))


@admin_bp.route('/medicines/delete/<int:med_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_medicine(med_id):
    med = db.get_or_404(Medicine, med_id)
    name = med.name
    db.session.delete(med)
    db.session.commit()
    flash(f'Medicine "{name}" deleted from master catalog.', 'info')
    return redirect(url_for('admin.medicines'))
