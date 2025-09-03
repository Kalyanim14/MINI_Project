import unittest
from app import app

class FlaskStegoIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test if the home page loads."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Encrypt', response.data)

    def test_encrypt_page_get(self):
        """Test GET request to /encrypt."""
        response = self.app.get('/encrypt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Encrypt', response.data)

    def test_encrypt_post_missing_fields(self):
        """Test POST to /encrypt with missing fields."""
        response = self.app.post('/encrypt', data={})
        self.assertIn(b'All fields are required.', response.data)

    def test_decrypt_page_get(self):
        """Test GET request to /decrypt."""
        response = self.app.get('/decrypt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Decrypt', response.data)

    def test_decrypt_post_missing_fields(self):
        """Test POST to /decrypt with missing fields."""
        response = self.app.post('/decrypt', data={})
        self.assertEqual(response.status_code, 200)  # Should return 200, not 400
        self.assertIn(b'All fields are required.', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)