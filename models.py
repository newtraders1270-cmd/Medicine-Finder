from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer') # customer, store, supplier, admin
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    store_profile = db.relationship('Store', backref='owner', uselist=False, cascade='all, delete-orphan')
    supplier_profile = db.relationship('Supplier', backref='owner', uselist=False, cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Medicine(db.Model):
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True) # e.g. Dolo 650, Crocin Advance
    generic_name = db.Column(db.String(150), nullable=False, index=True) # e.g. Paracetamol
    strength = db.Column(db.String(50), nullable=False) # e.g. 650 mg, 500 mg
    category = db.Column(db.String(50), nullable=False, default='Tablet') # Tablet, Syrup, Capsule, Drops, Ointment
    manufacturer = db.Column(db.String(120), nullable=True) # e.g. Micro Labs, GSK, Cipla
    default_mrp = db.Column(db.Float, nullable=False, default=0.0)
    uses = db.Column(db.Text, nullable=True) # Medical indications / symptoms
    dosage_info = db.Column(db.String(250), nullable=True) # Dosage advice
    prescription_required = db.Column(db.Boolean, default=False)
    is_generic = db.Column(db.Boolean, default=False) # True if sold under pure generic name

    # Relationships
    inventory_entries = db.relationship('StoreInventory', backref='medicine', lazy='dynamic', cascade='all, delete-orphan')
    supplier_listings = db.relationship('SupplierCatalog', backref='medicine', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Medicine {self.name} ({self.generic_name})>'


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    store_name = db.Column(db.String(150), nullable=False)
    license_no = db.Column(db.String(100), nullable=False) # Pharmacy Drug License
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(80), nullable=False, default='Mumbai')
    area = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False, default=19.0760)
    longitude = db.Column(db.Float, nullable=False, default=72.8777)
    phone = db.Column(db.String(20), nullable=False)
    opening_hours = db.Column(db.String(100), default='8:00 AM - 11:00 PM')
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    inventory = db.relationship('StoreInventory', backref='store', lazy='dynamic', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', backref='store', lazy='dynamic')
    restock_orders = db.relationship('RestockOrder', backref='store', lazy='dynamic')

    def __repr__(self):
        return f'<Store {self.store_name} ({self.city})>'


class StoreInventory(db.Model):
    __tablename__ = 'store_inventory'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    selling_price = db.Column(db.Float, nullable=False) # Discounted or retail price
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    min_threshold = db.Column(db.Integer, nullable=False, default=10) # Alert if <= threshold
    batch_no = db.Column(db.String(50), nullable=True)
    expiry_date = db.Column(db.String(20), nullable=True) # YYYY-MM or YYYY-MM-DD
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_threshold

    @property
    def discount_percent(self):
        if self.medicine and self.medicine.default_mrp > 0:
            diff = self.medicine.default_mrp - self.selling_price
            if diff > 0:
                return round((diff / self.medicine.default_mrp) * 100, 1)
        return 0.0

    def __repr__(self):
        return f'<StoreInventory Store:{self.store_id} Med:{self.medicine_id} Qty:{self.stock_quantity}>'


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    license_no = db.Column(db.String(100), nullable=False) # Wholesale Drug License
    warehouse_address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(80), nullable=False, default='Mumbai')
    phone = db.Column(db.String(20), nullable=False)
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    catalog_items = db.relationship('SupplierCatalog', backref='supplier', lazy='dynamic', cascade='all, delete-orphan')
    restock_orders = db.relationship('RestockOrder', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return f'<Supplier {self.company_name}>'


class SupplierCatalog(db.Model):
    __tablename__ = 'supplier_catalog'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    wholesale_rate = db.Column(db.Float, nullable=False) # Bulk price per unit
    min_order_qty = db.Column(db.Integer, nullable=False, default=50) # Minimum units per order
    stock_units = db.Column(db.Integer, nullable=False, default=1000)
    batch_no = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<SupplierCatalog Supplier:{self.supplier_id} Med:{self.medicine_id} Rate:{self.wholesale_rate}>'


class RestockOrder(db.Model):
    __tablename__ = 'restock_orders'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Pending') # Pending, Accepted, Dispatched, Delivered, Cancelled
    notes = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    medicine = db.relationship('Medicine')

    def __repr__(self):
        return f'<RestockOrder #{self.id} Store:{self.store_id} Status:{self.status}>'


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    reservation_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Reserved') # Reserved, Ready for Pickup, Completed, Cancelled
    customer_notes = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    medicine = db.relationship('Medicine')

    def __repr__(self):
        return f'<Reservation {self.reservation_code} Status:{self.status}>'

