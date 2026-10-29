# MediCompare - Medicine Locator, Price Comparison & Supply Chain Portal

A comprehensive, full-stack web application designed for a **TY CS (Third Year Computer Science)** college project.

---

## 🌟 Key Features

1. **Intelligent Medicine Search & Autocomplete**:
   - Live autocomplete as you type by **Brand Name** (e.g. *Dolo 650*, *Augmentin 625*) or **Active Salt** (e.g. *Paracetamol*, *Azithromycin*).
2. **Multi-Store Price Comparison Matrix**:
   - Compare real prices side-by-side across nearby verified pharmacies.
   - Highlights the **Lowest Price Pharmacy** with a special badge.
   - Real-time stock counts: `In Stock`, `Low Stock Alert`, or `Out of Stock`.
3. **Smart Generic Drug Advisory Engine**:
   - Automatically detects cheaper bioequivalent generic medicines.
   - Shows patient savings (e.g. Save 65% by switching from *Dolo 650* at ₹33.50 to *Generic Paracetamol 650* at ₹11.50).
4. **Interactive Pharmacy Locator Map**:
   - Built with **Leaflet.js** and **OpenStreetMap** (100% free, no API billing required).
   - Plots pharmacies on the map with popup cards and Google Maps driving directions.
5. **Customer Counter Reservation Slip**:
   - Generate instant 6-digit booking tokens (e.g. `MED-884920`) with printable vouchers to collect medicine without waiting.
6. **Chemist Inventory & Automated Low-Stock Alert**:
   - Visual warnings when medicine units drop $\le 10$.
   - 1-click **"Order from Wholesaler"** button to replenish inventory directly from registered distributors.
7. **Wholesale Supplier Hub**:
   - Bulk medicine catalog with Minimum Order Quantities (MOQ).
   - Order fulfillment lifecycle (`Pending -> Accepted -> Dispatched -> Delivered`).
   - Automatically increments pharmacy stock upon delivery!
8. **Admin Panel**:
   - Verify drug licenses for pharmacies and wholesale distributors.
   - Manage master drug catalog.

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6, Leaflet.js
- **Backend**: Python (Flask 3.1)
- **Database**: SQLite with SQLAlchemy ORM (`medicompare.db`)
- **Authentication**: Role-based access control with Werkzeug salted password hashing

---

## 🚀 How to Run the Project (Windows)

### Method 1: Double-Click Startup
Simply double-click the **`run.bat`** file in the root directory!  
It will automatically verify Python, check dependencies, seed sample data, and open the server at `http://127.0.0.1:5000`.

### Method 2: Command Line
```powershell
# 1. Install dependencies
py -m pip install -r requirements.txt

# 2. Seed database with realistic demo data
py seed_data.py

# 3. Start the Flask application
py app.py
```
Then open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🔑 Demo Login Accounts

All accounts share the password: **`password123`**  
*(Note: You can also use the **1-Click Quick-Fill buttons** on the login page!)*

| Role | Email | Password | Details |
| :--- | :--- | :--- | :--- |
| **Customer** | `customer@demo.com` | `password123` | Patient Rahul Sharma |
| **Chemist 1** | `apollo@demo.com` | `password123` | Apollo Pharmacy (Andheri West) |
| **Chemist 2** | `wellness@demo.com` | `password123` | Wellness Forever (Bandra West) |
| **Chemist 3** | `sanjivani@demo.com` | `password123` | Sanjivani Chemist (Dadar East) - *Lowest Prices* |
| **Supplier** | `metro@demo.com` | `password123` | Metro Pharma Wholesalers |
| **Admin** | `admin@demo.com` | `password123` | System Administrator |

---

## 📁 Academic Submission Documents Included

- **`college_docs/viva_qa.md`**: Top 25+ expected Viva questions and detailed answers external examiners ask.
- **`college_docs/project_synopsis.md`**: Ready-to-submit project report summary with Abstract, Objectives, Requirements, and System Modules.

