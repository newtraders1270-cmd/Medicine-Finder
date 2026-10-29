import os
from flask import Flask, session
from config import Config
from models import db, User, Store, Supplier

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.customer_routes import customer_bp
    from routes.store_routes import store_bp
    from routes.supplier_routes import supplier_bp
    from routes.admin_routes import admin_bp
    from routes.api_routes import api_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Template Context Processors
    @app.context_processor
    def inject_user_context():
        user = None
        store = None
        supplier = None
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user:
                if user.role == 'store':
                    store = Store.query.filter_by(user_id=user.id).first()
                elif user.role == 'supplier':
                    supplier = Supplier.query.filter_by(user_id=user.id).first()

        return dict(
            current_user=user,
            current_store=store,
            current_supplier=supplier,
            user_role=session.get('user_role'),
            is_logged_in=('user_id' in session)
        )

    # Jinja Filters
    @app.template_filter('currency')
    def currency_filter(value):
        try:
            return f"₹{float(value):,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print(" MediCompare - Medicine Locator & Price Comparison Web Portal")
    print(" College Project - TY CS")
    print(" Server running on: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
