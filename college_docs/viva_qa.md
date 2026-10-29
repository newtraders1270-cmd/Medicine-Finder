# Medicine Availability Finder - College Project Viva Questions & Answers
**Academic Year**: T.Y.C.S. (Third Year Computer Science)  
**Student Name**: Kaustubh Naresh Mhatre (Roll No. 66)  
**Project Guide**: Prof. Zeba Kuwari  
**Project Title**: Medicine Availability Finder (Stock Locator & Price Comparison)  
**Domain**: Web Technologies, Healthcare Informatics, Supply Chain Management, Database Engineering

---

### Q1: What is the main objective of this project?
**Answer**:  
The primary objective of MediCompare is to address real-world drug accessibility, transparency, and distribution challenges by connecting three key stakeholders:
1. **Customers (Patients)**: Who struggle to locate nearby pharmacies with prescribed medicines in stock, face price disparities, and overpay for branded medicines due to lack of generic awareness.
2. **Medical Store Owners (Retail Chemists)**: Who need digital inventory tracking, automated low-stock re-order alerts, and pre-booking pickup management.
3. **Wholesale Suppliers (Distributors)**: Who require a digital B2B channel to receive bulk replenishment orders from retail chemists.

---

### Q2: What technology stack is used and why was it chosen?
**Answer**:
- **Frontend**: **HTML5, CSS3, JavaScript** styled with **Bootstrap 5** and enhanced with **Leaflet.js** for interactive map visualization. It ensures high responsiveness, fast client-side autocomplete, and zero frontend build overhead.
- **Backend**: **Python (Flask)**. Flask follows the WSGI standard and micro-framework philosophy, giving clean route modularization (Blueprints), high extensibility, and simple MVC separation.
- **Database**: **SQLite with SQLAlchemy ORM**. SQLite is zero-configuration, ACID-compliant, serverless, and stores the entire database within a single portable file (`medicompare.db`). SQLAlchemy provides robust ORM mapping and eliminates SQL injection risks.

---

### Q3: How does the "Smart Advice / Generic Substitution" feature work?
**Answer**:  
When a user searches for a branded medicine (e.g., *Dolo 650*), the system:
1. Identifies the active pharmaceutical salt (`generic_name` = *Paracetamol*) and dosage strength (*650 mg*).
2. Queries the database for bioequivalent generic medicines sharing that exact salt formulation.
3. Locates nearby verified pharmacies stocking the generic equivalent.
4. Calculates the price difference and exact savings percentage:
   $$\text{Savings \%} = \frac{\text{Brand MRP} - \text{Generic Price}}{\text{Brand MRP}} \times 100$$
5. Renders a prominent **Smart Savings Advisory Banner** displaying both price options, promoting affordable healthcare.

---

### Q4: How is security handled in this web application?
**Answer**:
1. **Password Hashing**: Passwords are never stored in plain text. We utilize `werkzeug.security` with PBKDF2/SHA-256 and salted hashes (`generate_password_hash` and `check_password_hash`).
2. **SQL Injection Prevention**: All database operations use SQLAlchemy ORM with parameterized queries, preventing SQL injection attacks.
3. **Session Management & RBAC (Role-Based Access Control)**: Secure HTTP session cookies manage user identities. Custom Python decorators (`@login_required`, `@role_required`) enforce permission barriers so customers cannot access pharmacy stock, and chemists cannot access admin routes.
4. **Verification Gate**: Only verified stores and suppliers can list medicines or accept bulk orders, preventing counterfeit sellers.

---

### Q5: What database normalization level does your schema follow?
**Answer**:  
The schema conforms to **Third Normal Form (3NF)**:
- **1NF**: Every table column holds atomic values; no repeating groups.
- **2NF**: All non-key attributes are fully functionally dependent on the primary key (composite tables like `StoreInventory` separate store and medicine attributes cleanly).
- **3NF**: There are no transitive dependencies; non-key attributes depend only on the primary key (e.g., store addresses belong to `Store`, not repeated in `StoreInventory` or `Reservations`).

---

### Q6: How does the Restock / Supply Chain replenishment workflow operate?
**Answer**:
1. When a pharmacy's medicine stock falls to or below `min_threshold` (e.g., $\le 10$ units), the system raises a **Low-Stock Alert** on the chemist's dashboard.
2. The chemist clicks **"Order from Wholesaler"**, which queries `SupplierCatalog` filtered for that drug.
3. The chemist creates a `RestockOrder` respecting the supplier's Minimum Order Quantity (MOQ).
4. The supplier sees the order in their dashboard and advances the lifecycle: `Pending -> Accepted -> Dispatched -> Delivered`.
5. Upon marking as **Delivered**, the backend automatically increments the receiving pharmacy's inventory quantity in `StoreInventory`.

---

### Q7: How are pharmacy locations rendered on the map without Google Maps billing?
**Answer**:  
We integrated **Leaflet.js** with open-source **OpenStreetMap** tile layers. Each registered pharmacy holds latitude and longitude coordinates. Our backend provides a JSON API endpoint (`/api/stores`), and client-side JavaScript dynamically plots custom map pins with clickable popup info cards, opening hours, and one-click Google Maps driving direction routing.

---

### Q8: What design pattern is used in the backend architecture?
**Answer**:  
The application uses the **MVC (Model-View-Controller)** pattern with Flask Blueprints:
- **Model**: SQLAlchemy entities (`User`, `Medicine`, `Store`, `StoreInventory`, `Supplier`, `RestockOrder`, `Reservation`) in `models.py`.
- **View**: Jinja2 HTML templates in `templates/` styled with Bootstrap 5 and CSS.
- **Controller**: Route blueprints in `routes/` handling request validation, business logic, session checks, and database transactions.

---

### Q9: What happens when a customer reserves a medicine?
**Answer**:  
1. The customer selects a verified pharmacy with stock and clicks "Reserve".
2. The system checks stock availability and temporarily decrements the count to prevent over-allocation.
3. A unique 6-digit alphanumeric reservation token (e.g., `MED-884920`) is generated.
4. A reservation record is saved with status `Reserved`.
5. The customer can view and print a counter pickup voucher. If the chemist or customer cancels, the reserved stock is automatically returned to the inventory.

---

### Q10: What are future enhancements for this project?
**Answer**:
1. Integration of OCR (Optical Character Recognition) to automatically scan handwritten doctor prescriptions and match medicines.
2. Live GPS geolocation tracking of delivery vehicles for wholesale supply dispatches.
3. Automated WhatsApp/SMS booking notifications via Twilio or Gupshup API.
4. Machine Learning predictive forecasting of seasonal drug shortages based on historical purchase trends.

