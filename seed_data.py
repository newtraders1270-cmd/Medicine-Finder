import os
from datetime import datetime
from app import create_app
from models import db, User, Store, StoreInventory, Supplier, SupplierCatalog, Medicine, RestockOrder, Reservation

app = create_app()

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("[*] Database tables created cleanly.")

        # ==========================================
        # 1. CREATE USERS
        # ==========================================
        # Admin
        admin = User(full_name="System Administrator", email="admin@demo.com", role="admin", phone="9900000001")
        admin.set_password("password123")

        # Customers
        cust1 = User(full_name="Rahul Sharma", email="customer@demo.com", role="customer", phone="9820011223")
        cust1.set_password("password123")

        cust2 = User(full_name="Priya Nair", email="priya@demo.com", role="customer", phone="9833445566")
        cust2.set_password("password123")

        # Store Owners
        store_user1 = User(full_name="Rajesh Gupta", email="apollo@demo.com", role="store", phone="022-26281122")
        store_user1.set_password("password123")

        store_user2 = User(full_name="Kunal Mehra", email="wellness@demo.com", role="store", phone="022-26402233")
        store_user2.set_password("password123")

        store_user3 = User(full_name="Dr. Suresh Patil", email="sanjivani@demo.com", role="store", phone="022-24123344")
        store_user3.set_password("password123")

        store_user4 = User(full_name="Amit Varma", email="medplus@demo.com", role="store", phone="022-28914455")
        store_user4.set_password("password123")

        # Suppliers
        sup_user1 = User(full_name="Vikas Malhotra", email="metro@demo.com", role="supplier", phone="022-66991100")
        sup_user1.set_password("password123")

        sup_user2 = User(full_name="Ramesh Jain", email="bharat@demo.com", role="supplier", phone="022-66992200")
        sup_user2.set_password("password123")

        db.session.add_all([admin, cust1, cust2, store_user1, store_user2, store_user3, store_user4, sup_user1, sup_user2])
        db.session.commit()
        print("[*] Users created.")

        # ==========================================
        # 2. CREATE STORES & SUPPLIERS
        # ==========================================
        store1 = Store(
            user_id=store_user1.id,
            store_name="Apollo Pharmacy - Andheri West",
            license_no="MH-TZ4-2024-8841",
            address="Shop 4, Crystal Point Mall, Link Road, Andheri West",
            city="Mumbai",
            area="Andheri West",
            latitude=19.1352,
            longitude=72.8315,
            phone="022-26281122",
            opening_hours="24 Hours Open",
            is_verified=True
        )

        store2 = Store(
            user_id=store_user2.id,
            store_name="Wellness Forever - Bandra",
            license_no="MH-TZ4-2023-7712",
            address="Ground Floor, Hill Road, Near Mehboob Studio, Bandra West",
            city="Mumbai",
            area="Bandra West",
            latitude=19.0544,
            longitude=72.8282,
            phone="022-26402233",
            opening_hours="24 Hours Open",
            is_verified=True
        )

        store3 = Store(
            user_id=store_user3.id,
            store_name="Sanjivani Chemist & Druggist",
            license_no="MH-TZ1-2022-5509",
            address="14 Swami Samarth Complex, Tilak Bridge, Dadar East",
            city="Mumbai",
            area="Dadar East",
            latitude=19.0178,
            longitude=72.8478,
            phone="022-24123344",
            opening_hours="8:00 AM - 11:30 PM",
            is_verified=True
        )

        store4 = Store(
            user_id=store_user4.id,
            store_name="MedPlus Pharmacy - Borivali",
            license_no="MH-TZ7-2024-9123",
            address="Shop 1, Sai Heritage, Chandavarkar Road, Borivali West",
            city="Mumbai",
            area="Borivali West",
            latitude=19.2307,
            longitude=72.8567,
            phone="022-28914455",
            opening_hours="8:30 AM - 11:00 PM",
            is_verified=True
        )

        supplier1 = Supplier(
            user_id=sup_user1.id,
            company_name="Metro Pharma Wholesalers",
            license_no="WDL-MH-2021-0045",
            warehouse_address="Warehouse 4B, Akruti Trade Centre, MIDC, Andheri East",
            city="Mumbai",
            phone="022-66991100",
            is_verified=True
        )

        supplier2 = Supplier(
            user_id=sup_user2.id,
            company_name="Bharat Wholesale Drug Distributors",
            license_no="WDL-MH-2020-0089",
            warehouse_address="Logistics Park B-7, Mumbai-Nashik Highway, Bhiwandi",
            city="Mumbai",
            phone="022-66992200",
            is_verified=True
        )

        db.session.add_all([store1, store2, store3, store4, supplier1, supplier2])
        db.session.commit()
        print("[*] Stores and Suppliers created.")

        # ==========================================
        # 3. CREATE MASTER MEDICINE DIRECTORY
        # ==========================================
        medicines = [
            # 1. Paracetamol 650 Brand vs Generic
            Medicine(
                name="Dolo 650",
                generic_name="Paracetamol",
                strength="650 mg",
                category="Tablet",
                manufacturer="Micro Labs",
                default_mrp=33.50,
                uses="Fever relief, Mild to moderate body pain, Headache, Viral infections",
                dosage_info="1 tablet every 6 hours after food (Max 4 tabs/day)",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Paracetamol 650mg Generic",
                generic_name="Paracetamol",
                strength="650 mg",
                category="Tablet",
                manufacturer="Jan Aushadhi / Cipla Generic",
                default_mrp=11.50,
                uses="Fever relief, Mild to moderate body pain, Headache (Cheaper Bioequivalent Generic)",
                dosage_info="1 tablet every 6 hours after food (Max 4 tabs/day)",
                prescription_required=False,
                is_generic=True
            ),

            # 2. Paracetamol 500 Brand vs Generic
            Medicine(
                name="Crocin Advance",
                generic_name="Paracetamol",
                strength="500 mg",
                category="Tablet",
                manufacturer="GSK Consumer Healthcare",
                default_mrp=24.00,
                uses="Fast fever relief, Headaches, Toothache, Muscle aches",
                dosage_info="1-2 tablets every 4-6 hours",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Paracetamol 500mg Generic",
                generic_name="Paracetamol",
                strength="500 mg",
                category="Tablet",
                manufacturer="Generic Pharma India",
                default_mrp=8.00,
                uses="Fever relief and headache management",
                dosage_info="1 tablet every 6 hours",
                prescription_required=False,
                is_generic=True
            ),

            # 3. Amoxicillin + Clavulanate Brand vs Generic
            Medicine(
                name="Augmentin 625 Duo",
                generic_name="Amoxicillin + Potassium Clavulanate",
                strength="625 mg",
                category="Tablet",
                manufacturer="GSK Pharmaceuticals",
                default_mrp=223.00,
                uses="Broad-spectrum antibiotic for Respiratory, Dental, ENT & Skin infections",
                dosage_info="1 tablet twice daily after meals as prescribed by doctor",
                prescription_required=True,
                is_generic=False
            ),
            Medicine(
                name="Amoxyclav 625 Generic",
                generic_name="Amoxicillin + Potassium Clavulanate",
                strength="625 mg",
                category="Tablet",
                manufacturer="Jan Aushadhi",
                default_mrp=72.00,
                uses="Broad-spectrum antibiotic for severe bacterial infections (Generic Equivalent)",
                dosage_info="1 tablet twice daily with food",
                prescription_required=True,
                is_generic=True
            ),

            # 4. Pantoprazole Brand vs Generic
            Medicine(
                name="Pantocid 40",
                generic_name="Pantoprazole",
                strength="40 mg",
                category="Tablet",
                manufacturer="Sun Pharma",
                default_mrp=168.00,
                uses="Acidity, Gastroesophageal reflux disease (GERD), Heartburn, Stomach ulcers",
                dosage_info="1 tablet in the morning empty stomach 30 mins before food",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Pantoprazole 40mg Generic",
                generic_name="Pantoprazole",
                strength="40 mg",
                category="Tablet",
                manufacturer="Zydus Generics",
                default_mrp=42.00,
                uses="Acidity, Heartburn, Acid Reflux reduction (Generic Equivalent)",
                dosage_info="1 tablet morning empty stomach",
                prescription_required=False,
                is_generic=True
            ),

            # 5. Azithromycin Brand vs Generic
            Medicine(
                name="Azithral 500",
                generic_name="Azithromycin",
                strength="500 mg",
                category="Tablet",
                manufacturer="Alembic Pharmaceuticals",
                default_mrp=132.50,
                uses="Throat infections, Tonsillitis, Sinusitis, Chest infections, Typhoid",
                dosage_info="1 tablet once daily 1 hour before or 2 hours after meal",
                prescription_required=True,
                is_generic=False
            ),
            Medicine(
                name="Azithromycin 500mg Generic",
                generic_name="Azithromycin",
                strength="500 mg",
                category="Tablet",
                manufacturer="Cipla Generics",
                default_mrp=49.00,
                uses="Antibiotic for bacterial infections (Generic Equivalent)",
                dosage_info="1 tablet once daily for 3 to 5 days",
                prescription_required=True,
                is_generic=True
            ),

            # 6. Metformin Brand vs Generic
            Medicine(
                name="Glycomet 500 SR",
                generic_name="Metformin Hydrochloride",
                strength="500 mg",
                category="Tablet",
                manufacturer="USV Ltd",
                default_mrp=49.50,
                uses="Type 2 Diabetes Mellitus, Blood sugar regulation",
                dosage_info="1 tablet with or immediately after lunch/dinner",
                prescription_required=True,
                is_generic=False
            ),
            Medicine(
                name="Metformin 500mg Generic",
                generic_name="Metformin Hydrochloride",
                strength="500 mg",
                category="Tablet",
                manufacturer="Jan Aushadhi",
                default_mrp=16.00,
                uses="Type 2 Diabetes glucose control (Generic Equivalent)",
                dosage_info="1 tablet with food",
                prescription_required=True,
                is_generic=True
            ),

            # 7. Telmisartan Brand vs Generic
            Medicine(
                name="Telma 40",
                generic_name="Telmisartan",
                strength="40 mg",
                category="Tablet",
                manufacturer="Glenmark Pharmaceuticals",
                default_mrp=128.00,
                uses="High blood pressure (Hypertension), Prevention of heart attack and stroke",
                dosage_info="1 tablet once daily morning with or without food",
                prescription_required=True,
                is_generic=False
            ),
            Medicine(
                name="Telmisartan 40mg Generic",
                generic_name="Telmisartan",
                strength="40 mg",
                category="Tablet",
                manufacturer="Sun Generic",
                default_mrp=36.00,
                uses="Hypertension blood pressure control (Generic Equivalent)",
                dosage_info="1 tablet once daily",
                prescription_required=True,
                is_generic=True
            ),

            # 8. Montelukast + Levocetirizine Brand vs Generic
            Medicine(
                name="Montair LC",
                generic_name="Montelukast + Levocetirizine",
                strength="10mg + 5mg",
                category="Tablet",
                manufacturer="Cipla",
                default_mrp=215.00,
                uses="Allergic rhinitis, Hay fever, Sneezing, Runny itchy nose, Mild asthma symptoms",
                dosage_info="1 tablet at bedtime",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Montelukast + Levocetirizine Generic",
                generic_name="Montelukast + Levocetirizine",
                strength="10mg + 5mg",
                category="Tablet",
                manufacturer="Mankind Generics",
                default_mrp=65.00,
                uses="Allergy relief, Cold and Sneezing (Generic Equivalent)",
                dosage_info="1 tablet at night",
                prescription_required=False,
                is_generic=True
            ),

            # 9. Other Popular Medicines
            Medicine(
                name="Pan-D Capsule",
                generic_name="Pantoprazole + Domperidone",
                strength="40mg + 30mg",
                category="Capsule",
                manufacturer="Alkem Laboratories",
                default_mrp=199.00,
                uses="Gastroesophageal reflux with nausea, Acid indigestion, Gas and bloating",
                dosage_info="1 capsule in the morning before food",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Combiflam",
                generic_name="Ibuprofen + Paracetamol",
                strength="400mg + 325mg",
                category="Tablet",
                manufacturer="Sanofi India",
                default_mrp=47.50,
                uses="Joint inflammation, Dental toothache, Sprains, Muscular fever pain",
                dosage_info="1 tablet with food when pain occurs",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Becosules Z",
                generic_name="Vitamin B-Complex + Zinc + Vitamin C",
                strength="Capsule",
                category="Capsule",
                manufacturer="Pfizer India",
                default_mrp=56.00,
                uses="Mouth ulcers, Vitamin B deficiency, Fatigue, Immune support",
                dosage_info="1 capsule daily after breakfast",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Cipcal 500",
                generic_name="Calcium + Vitamin D3",
                strength="500mg + 250IU",
                category="Tablet",
                manufacturer="Cipla",
                default_mrp=98.00,
                uses="Calcium deficiency, Bone weakness, Osteoporosis prevention",
                dosage_info="1 tablet daily after food",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Volini Pain Relief Gel",
                generic_name="Diclofenac Diethylamine + Methyl Salicylate",
                strength="50g Tube",
                category="Ointment",
                manufacturer="Sun Pharma",
                default_mrp=155.00,
                uses="Backache, Neck pain, Joint sprains, Muscle stiffness",
                dosage_info="Apply gently on affected area 3-4 times daily",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Benadryl Cough Syrup",
                generic_name="Diphenhydramine + Ammonium Chloride",
                strength="100 ml",
                category="Syrup",
                manufacturer="Johnson & Johnson",
                default_mrp=125.00,
                uses="Dry cough, Throat tickle, Allergic cough relief",
                dosage_info="10 ml (2 teaspoons) every 6 hours",
                prescription_required=False,
                is_generic=False
            ),
            Medicine(
                name="Ascoril LS Syrup",
                generic_name="Levosalbutamol + Ambroxol + Guaiphenesin",
                strength="100 ml",
                category="Syrup",
                manufacturer="Glenmark",
                default_mrp=142.00,
                uses="Productive wet cough, Chest congestion, Mucus breakdown in lungs",
                dosage_info="5-10 ml three times a day",
                prescription_required=True,
                is_generic=False
            ),
            Medicine(
                name="Ecosprin 75",
                generic_name="Aspirin (Acetylsalicylic Acid)",
                strength="75 mg",
                category="Tablet",
                manufacturer="USV Ltd",
                default_mrp=12.80,
                uses="Blood thinner, Heart attack prevention, Stroke prevention",
                dosage_info="1 tablet daily with lunch",
                prescription_required=True,
                is_generic=False
            )
        ]

        db.session.add_all(medicines)
        db.session.commit()
        print(f"[*] {len(medicines)} Medicines added to database.")

        # ==========================================
        # 4. CREATE PHARMACY INVENTORIES (With Price Differences & Low Stock Alerts)
        # ==========================================
        # Helper to find med
        def get_med(name):
            return Medicine.query.filter(Medicine.name.ilike(name)).first()

        dolo = get_med("Dolo 650")
        dolo_gen = get_med("Paracetamol 650mg Generic")
        crocin = get_med("Crocin Advance")
        crocin_gen = get_med("Paracetamol 500mg Generic")
        augmentin = get_med("Augmentin 625 Duo")
        amoxyclav_gen = get_med("Amoxyclav 625 Generic")
        pantocid = get_med("Pantocid 40")
        pantoprazole_gen = get_med("Pantoprazole 40mg Generic")
        azithral = get_med("Azithral 500")
        azithro_gen = get_med("Azithromycin 500mg Generic")
        glycomet = get_med("Glycomet 500 SR")
        telma = get_med("Telma 40")
        montair = get_med("Montair LC")
        combiflam = get_med("Combiflam")
        becosules = get_med("Becosules Z")
        volini = get_med("Volini Pain Relief Gel")
        benadryl = get_med("Benadryl Cough Syrup")

        inventories = [
            # Store 1: Apollo Pharmacy (Andheri)
            StoreInventory(store_id=store1.id, medicine_id=dolo.id, selling_price=32.00, stock_quantity=45, min_threshold=10, batch_no="AP-D6-101", expiry_date="2027-08"),
            StoreInventory(store_id=store1.id, medicine_id=dolo_gen.id, selling_price=11.00, stock_quantity=30, min_threshold=10, batch_no="AP-PG-202", expiry_date="2027-11"),
            StoreInventory(store_id=store1.id, medicine_id=crocin.id, selling_price=23.00, stock_quantity=50, min_threshold=10, batch_no="AP-CR-303", expiry_date="2027-05"),
            StoreInventory(store_id=store1.id, medicine_id=augmentin.id, selling_price=215.00, stock_quantity=18, min_threshold=10, batch_no="AP-AG-404", expiry_date="2027-02"),
            StoreInventory(store_id=store1.id, medicine_id=pantocid.id, selling_price=160.00, stock_quantity=4, min_threshold=10, batch_no="AP-PT-505", expiry_date="2026-12"), # LOW STOCK!
            StoreInventory(store_id=store1.id, medicine_id=azithral.id, selling_price=128.00, stock_quantity=3, min_threshold=10, batch_no="AP-AZ-606", expiry_date="2027-04"), # LOW STOCK!
            StoreInventory(store_id=store1.id, medicine_id=volini.id, selling_price=145.00, stock_quantity=22, min_threshold=10, batch_no="AP-VL-707", expiry_date="2028-01"),

            # Store 2: Wellness Forever (Bandra)
            StoreInventory(store_id=store2.id, medicine_id=dolo.id, selling_price=31.00, stock_quantity=60, min_threshold=10, batch_no="WF-D6-11", expiry_date="2027-09"),
            StoreInventory(store_id=store2.id, medicine_id=dolo_gen.id, selling_price=10.50, stock_quantity=25, min_threshold=10, batch_no="WF-PG-22", expiry_date="2027-10"),
            StoreInventory(store_id=store2.id, medicine_id=crocin.id, selling_price=22.50, stock_quantity=40, min_threshold=10, batch_no="WF-CR-33", expiry_date="2027-07"),
            StoreInventory(store_id=store2.id, medicine_id=augmentin.id, selling_price=210.00, stock_quantity=20, min_threshold=10, batch_no="WF-AG-44", expiry_date="2027-03"),
            StoreInventory(store_id=store2.id, medicine_id=amoxyclav_gen.id, selling_price=68.00, stock_quantity=35, min_threshold=10, batch_no="WF-AM-55", expiry_date="2027-06"),
            StoreInventory(store_id=store2.id, medicine_id=pantocid.id, selling_price=158.00, stock_quantity=28, min_threshold=10, batch_no="WF-PT-66", expiry_date="2027-04"),
            StoreInventory(store_id=store2.id, medicine_id=pantoprazole_gen.id, selling_price=39.00, stock_quantity=45, min_threshold=10, batch_no="WF-PGEN-77", expiry_date="2027-12"),
            StoreInventory(store_id=store2.id, medicine_id=becosules.id, selling_price=52.00, stock_quantity=5, min_threshold=10, batch_no="WF-BC-88", expiry_date="2027-08"), # LOW STOCK!

            # Store 3: Sanjivani Chemist (Dadar) - BEST DISCOUNT STORE
            StoreInventory(store_id=store3.id, medicine_id=dolo.id, selling_price=29.50, stock_quantity=80, min_threshold=10, batch_no="SJ-D6-90", expiry_date="2027-12"), # Lowest Price!
            StoreInventory(store_id=store3.id, medicine_id=dolo_gen.id, selling_price=9.50, stock_quantity=100, min_threshold=10, batch_no="SJ-PG-91", expiry_date="2028-02"), # Super Low!
            StoreInventory(store_id=store3.id, medicine_id=crocin.id, selling_price=21.00, stock_quantity=30, min_threshold=10, batch_no="SJ-CR-92", expiry_date="2027-04"),
            StoreInventory(store_id=store3.id, medicine_id=crocin_gen.id, selling_price=7.00, stock_quantity=50, min_threshold=10, batch_no="SJ-CG-93", expiry_date="2027-09"),
            StoreInventory(store_id=store3.id, medicine_id=augmentin.id, selling_price=205.00, stock_quantity=15, min_threshold=10, batch_no="SJ-AG-94", expiry_date="2027-01"),
            StoreInventory(store_id=store3.id, medicine_id=amoxyclav_gen.id, selling_price=65.00, stock_quantity=40, min_threshold=10, batch_no="SJ-AMG-95", expiry_date="2027-08"),
            StoreInventory(store_id=store3.id, medicine_id=azithral.id, selling_price=122.00, stock_quantity=20, min_threshold=10, batch_no="SJ-AZ-96", expiry_date="2027-05"),
            StoreInventory(store_id=store3.id, medicine_id=azithro_gen.id, selling_price=44.00, stock_quantity=60, min_threshold=10, batch_no="SJ-AZG-97", expiry_date="2027-10"),
            StoreInventory(store_id=store3.id, medicine_id=glycomet.id, selling_price=45.00, stock_quantity=6, min_threshold=10, batch_no="SJ-GL-98", expiry_date="2026-11"), # LOW STOCK!

            # Store 4: MedPlus Pharmacy (Borivali)
            StoreInventory(store_id=store4.id, medicine_id=dolo.id, selling_price=33.00, stock_quantity=50, min_threshold=10, batch_no="MP-D6-01", expiry_date="2027-07"),
            StoreInventory(store_id=store4.id, medicine_id=pantocid.id, selling_price=162.00, stock_quantity=30, min_threshold=10, batch_no="MP-PT-02", expiry_date="2027-09"),
            StoreInventory(store_id=store4.id, medicine_id=telma.id, selling_price=120.00, stock_quantity=25, min_threshold=10, batch_no="MP-TL-03", expiry_date="2027-06"),
            StoreInventory(store_id=store4.id, medicine_id=montair.id, selling_price=200.00, stock_quantity=14, min_threshold=10, batch_no="MP-MN-04", expiry_date="2027-04"),
            StoreInventory(store_id=store4.id, medicine_id=combiflam.id, selling_price=44.00, stock_quantity=35, min_threshold=10, batch_no="MP-CB-05", expiry_date="2027-11"),
            StoreInventory(store_id=store4.id, medicine_id=benadryl.id, selling_price=120.00, stock_quantity=2, min_threshold=10, batch_no="MP-BD-06", expiry_date="2026-10") # LOW STOCK!
        ]

        db.session.add_all(inventories)
        db.session.commit()
        print("[*] Store inventories populated.")

        # ==========================================
        # 5. CREATE SUPPLIER WHOLESALE CATALOGS
        # ==========================================
        supplier_catalogs = [
            # Supplier 1: Metro Pharma Wholesalers
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=dolo.id, wholesale_rate=22.00, min_order_qty=50, stock_units=2000, batch_no="METRO-DOLO-88"),
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=crocin.id, wholesale_rate=16.50, min_order_qty=50, stock_units=1500, batch_no="METRO-CROC-77"),
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=augmentin.id, wholesale_rate=165.00, min_order_qty=20, stock_units=800, batch_no="METRO-AUG-66"),
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=pantocid.id, wholesale_rate=120.00, min_order_qty=30, stock_units=1200, batch_no="METRO-PAN-55"),
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=azithral.id, wholesale_rate=95.00, min_order_qty=25, stock_units=900, batch_no="METRO-AZI-44"),
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=glycomet.id, wholesale_rate=35.00, min_order_qty=40, stock_units=1100, batch_no="METRO-GLY-33"),
            SupplierCatalog(supplier_id=supplier1.id, medicine_id=volini.id, wholesale_rate=115.00, min_order_qty=20, stock_units=600, batch_no="METRO-VOL-22"),

            # Supplier 2: Bharat Wholesale Drug Distributors (Generics & Bulk Specialist)
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=dolo_gen.id, wholesale_rate=6.50, min_order_qty=100, stock_units=5000, batch_no="BHRT-PARA-10"),
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=crocin_gen.id, wholesale_rate=4.80, min_order_qty=100, stock_units=4000, batch_no="BHRT-P500-11"),
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=amoxyclav_gen.id, wholesale_rate=48.00, min_order_qty=30, stock_units=1500, batch_no="BHRT-AMXG-12"),
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=pantoprazole_gen.id, wholesale_rate=24.00, min_order_qty=50, stock_units=2500, batch_no="BHRT-PNTG-13"),
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=azithro_gen.id, wholesale_rate=32.00, min_order_qty=40, stock_units=1800, batch_no="BHRT-AZTG-14"),
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=telma.id, wholesale_rate=88.00, min_order_qty=30, stock_units=1200, batch_no="BHRT-TLM-15"),
            SupplierCatalog(supplier_id=supplier2.id, medicine_id=montair.id, wholesale_rate=145.00, min_order_qty=20, stock_units=800, batch_no="BHRT-MON-16")
        ]

        db.session.add_all(supplier_catalogs)
        db.session.commit()
        print("[*] Supplier wholesale catalogs created.")

        # ==========================================
        # 6. SAMPLE RESERVATIONS & RESTOCK ORDERS
        # ==========================================
        # Sample customer reservation
        res1 = Reservation(
            customer_id=cust1.id,
            store_id=store1.id,
            medicine_id=dolo.id,
            quantity=2,
            unit_price=32.00,
            total_price=64.00,
            reservation_code="MED-884920",
            status="Ready for Pickup",
            customer_notes="Will pick up by 6 PM today"
        )

        res2 = Reservation(
            customer_id=cust2.id,
            store_id=store3.id,
            medicine_id=dolo_gen.id,
            quantity=3,
            unit_price=9.50,
            total_price=28.50,
            reservation_code="MED-194022",
            status="Reserved",
            customer_notes="Please keep generic strips packed"
        )

        # Sample restock orders
        ro1 = RestockOrder(
            store_id=store1.id,
            supplier_id=supplier1.id,
            medicine_id=pantocid.id,
            quantity=50,
            unit_price=120.00,
            total_amount=6000.00,
            status="Dispatched",
            notes="Urgent replenishment needed due to low stock"
        )

        ro2 = RestockOrder(
            store_id=store3.id,
            supplier_id=supplier2.id,
            medicine_id=dolo_gen.id,
            quantity=100,
            unit_price=6.50,
            total_amount=650.00,
            status="Accepted",
            notes="Regular monthly bulk generic refill"
        )

        db.session.add_all([res1, res2, ro1, ro2])
        db.session.commit()
        print("[*] Sample reservations and restock orders populated.")

        print("=" * 60)
        print("SEEDING COMPLETED SUCCESSFULLY!")
        print("Demo Logins (Password for all: password123):")
        print("  - Customer: customer@demo.com")
        print("  - Medical Store: apollo@demo.com / wellness@demo.com / sanjivani@demo.com")
        print("  - Supplier: metro@demo.com / bharat@demo.com")
        print("  - Admin: admin@demo.com")
        print("=" * 60)

if __name__ == '__main__':
    seed_database()

