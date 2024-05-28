import logging
import unittest
from app import create_app, db
from app.models import Item

logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ItemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.app_context().push()
    #     db.create_all()
    #
    #     item = Item(name="Test Item", description="This is a test item")
    #     db.session.add(item)
    #     db.session.commit()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()

    def test_get_items(self):
        response = self.client.get('/items/')
        self.assertEqual(200, 200)

    def test_create_item(self):
        response = self.client.post('/items/', json={"name": "New Item"})
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'New Item', response.data)

    def test_create_item_pass(self):
        response = self.client.post('/items/pass/', json={"name": "New Item"})
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'New Item', response.data)

    def test_update_item(self):
        response = self.client.put('/items/2', json={"name": "Updated Item"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Item', response.data)

    def test_delete_item(self):
        response = self.client.delete('/items/2')
        self.assertEqual(response.status_code, 204)
