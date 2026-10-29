# Project Synopsis: Medicine Availability Finder
**Academic Level**: T.Y.C.S. (Third Year Computer Science)  
**Student Name**: Kaustubh Naresh Mhatre (Roll No. 66)  
**Project Guide**: Prof. Zeba Kuwari  

---

## 1. Project Title
**Medicine Availability Finder: Real-Time Pharmacy Stock Locator, Multi-Store Price Comparison & Pharmaceutical Supply Chain Portal**

## 2. Abstract
Finding vital prescribed medicines during emergencies or chronic treatments often results in patients visiting multiple local pharmacies due to unpredictable stockouts and price disparities. Furthermore, patients often overpay by 50% to 70% for branded pharmaceuticals simply because they are unaware of chemically identical, bioequivalent generic substitutes. At the retail tier, chemist shops rely on manual, ad-hoc telephone calls to order inventory from wholesale distributors.

**MediCompare** is an integrated web-based platform that unifies Patients, Retail Medical Stores (Chemists), and Wholesale Drug Suppliers. It empowers patients to search medications by brand or active chemical salt, compare prices across local pharmacies in real-time, view store locations on an interactive geospatial map, and receive automated recommendations for cheaper generic substitutes. For chemists, the platform delivers digital stock tracking, automated low-stock warnings, and direct one-click wholesale replenishment from registered distributors.

---

## 3. Objectives
1. Provide a transparent medicine price and availability comparison engine across retail pharmacies.
2. Promote affordable healthcare through a **Generic Bioequivalent Advisory Engine** that calculates patient cost savings.
3. Eliminate stockouts through automated chemist inventory alerts ($\le 10$ units) linked to wholesale replenishment.
4. Digitize counter reservations with alphanumeric booking tokens to reduce waiting times.
5. Provide a verification gate for system administrators to validate pharmacy and wholesale drug licenses.

---

## 4. Hardware & Software Requirements

### Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Hard Disk**: 500 MB free storage
- **Input / Output**: Keyboard, Mouse, Standard Display Monitor (1366x768 or higher)

### Software Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **Programming Language**: Python 3.10+ (Tested on Python 3.14)
- **Web Framework**: Flask 3.1+ (Python)
- **Database**: SQLite 3 with SQLAlchemy ORM
- **Frontend Technologies**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6
- **Mapping API**: Leaflet.js with OpenStreetMap (Free, open-source geospatial tiles)
- **Web Browser**: Google Chrome, Mozilla Firefox, or Microsoft Edge

---

## 5. Modules Description

### Module 1: Authentication & Role-Based Access Control (RBAC)
- Supports four user personas: Customer, Medical Store Owner, Wholesale Supplier, and Administrator.
- Implements secure PBKDF2/SHA-256 salted password hashing via Werkzeug.
- Session authorization decorators protect sensitive operational routes.

### Module 2: Customer Search & Generic Advisory Engine
- Live autocomplete search matching drug brand name, active chemical salt, or therapeutic indications.
- Side-by-side price comparison matrix sorted by price, distance, or stock.
- Automated generic substitution calculation showing percentage savings.
- One-click medicine counter reservation with printable vouchers.

### Module 3: Medical Store (Chemist) Management
- Real-time inventory CRUD operations (selling prices, stock units, batches, expiry dates).
- Automated Low-Stock Alert detection when quantity drops below threshold.
- Counter reservation pickup queue management.
- B2B Restock purchase order creation to registered wholesale distributors.

### Module 4: Wholesale Supplier Hub
- Wholesale bulk catalog management (bulk rates, MOQ, warehouse stock).
- Restock order fulfillment lifecycle (`Pending -> Accepted -> Dispatched -> Delivered`).
- Automated stock synchronization: marking an order as delivered automatically increments the chemist's inventory.

### Module 5: Administrator Console
- Pharmacy and distributor drug license verification gate.
- Master pharmaceutical drug database editor.
- System metrics and analytical dashboards.

---

## 6. Architecture & Data Flow

```
[ Customer / Patient ]  <-- Search & Compare -->  [ Web Application ]
                                                          |
                                                 [ Flask Controller ]
                                                          |
[ Retail Chemist Store ] <-- Re-order Stock -->  [ SQLAlchemy ORM ]
                                                          |
[ Wholesale Supplier  ]  <-- Fulfill Orders -->  [ SQLite Database ]
```

