import unittest
from app import create_app
from models import db, Medicine, Store, StoreInventory, User

class MediCompareTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Medi', response.data)
        self.assertIn(b'Compare', response.data)

    def test_search_branded_medicine(self):
        response = self.client.get('/search?q=Dolo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dolo 650', response.data)
        # Verify Generic Advice box is triggered
        self.assertIn(b'Generic Alternative', response.data)

    def test_medicine_detail_route(self):
        with self.app.app_context():
            med = Medicine.query.first()
            self.assertIsNotNone(med)
            med_id = med.id

        response = self.client.get(f'/medicine/{med_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nearby Store Availability', response.data)

    def test_store_locator(self):
        response = self.client.get('/store-locator')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Medical Store Locator', response.data)

    def test_api_suggestions(self):
        response = self.client.get('/api/search-suggestions?q=paracetamol')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertGreater(len(data), 0)

    def test_api_stores(self):
        response = self.client.get('/api/stores')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertGreater(len(data), 0)

    def test_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quick-Fill Logins', response.data)

if __name__ == '__main__':
    unittest.main()

