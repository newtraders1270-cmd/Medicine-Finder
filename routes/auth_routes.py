from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, User, Store, Supplier

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            user_role = session.get('user_role')
            if user_role not in allowed_roles:
                flash(f'Unauthorized access. This area is reserved for {", ".join(allowed_roles)}.', 'danger')
                return redirect(url_for('customer.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Set session
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['user_email'] = user.email
            session['user_role'] = user.role

            # If user has a store or supplier profile, store the ID
            if user.role == 'store' and user.store_profile:
                session['store_id'] = user.store_profile.id
                session['store_name'] = user.store_profile.store_name
            elif user.role == 'supplier' and user.supplier_profile:
                session['supplier_id'] = user.supplier_profile.id
                session['supplier_name'] = user.supplier_profile.company_name

            flash(f'Welcome back, {user.full_name}!', 'success')

            # Route by role or next parameter
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)

            if user.role == 'store':
                return redirect(url_for('store.dashboard'))
            elif user.role == 'supplier':
                return redirect(url_for('supplier.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('customer.index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'customer')
        phone = request.form.get('phone', '').strip()

        # Validation
        if not full_name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        # Create user
        user = User(full_name=full_name, email=email, role=role, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.flush() # Get user.id

        # If registering as store owner
        if role == 'store':
            store_name = request.form.get('store_name', '').strip() or f"{full_name}'s Pharmacy"
            license_no = request.form.get('license_no', '').strip() or 'DL-PENDING'
            address = request.form.get('address', '').strip() or 'Local Market'
            city = request.form.get('city', 'Mumbai').strip()
            area = request.form.get('area', '').strip() or 'Central'
            lat = float(request.form.get('latitude', 19.0760))
            lng = float(request.form.get('longitude', 72.8777))

            store = Store(
                user_id=user.id,
                store_name=store_name,
                license_no=license_no,
                address=address,
                city=city,
                area=area,
                latitude=lat,
                longitude=lng,
                phone=phone or '9876543210',
                is_verified=True # Auto-verified for demo convenience
            )
            db.session.add(store)

        # If registering as supplier
        elif role == 'supplier':
            company_name = request.form.get('company_name', '').strip() or f"{full_name} Wholesale"
            license_no = request.form.get('supplier_license', '').strip() or 'WDL-PENDING'
            warehouse_address = request.form.get('warehouse_address', '').strip() or 'Industrial Estate'
            city = request.form.get('city', 'Mumbai').strip()

            supplier = Supplier(
                user_id=user.id,
                company_name=company_name,
                license_no=license_no,
                warehouse_address=warehouse_address,
                city=city,
                phone=phone or '9876543210',
                is_verified=True
            )
            db.session.add(supplier)

        db.session.commit()
        flash('Registration successful! Please log in with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('customer.index'))

