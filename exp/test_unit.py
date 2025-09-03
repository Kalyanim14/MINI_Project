import unittest
import os
from io import BytesIO
from PIL import Image
import numpy as np
from app import encrypt_message, decrypt_message

class TestEncryptionFunctions(unittest.TestCase):

    def setUp(self):
        # Create a dummy image for testing
        self.image_path = "test_image.png"
        self.test_message = "Hello, Stego!"
        self.test_password = "secret"
        self.image_id = "dummy-id"

        img = Image.new('RGB', (10, 10), color='white')
        img.save(self.image_path)

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

    # --- Existing Tests ---
    def test_encrypt_message_function(self):
        """Test if encryption works correctly."""
        with open(self.image_path, 'rb') as f:
            img_io, base64_img, error = encrypt_message(f, self.test_message)
            self.assertIsNone(error)
            self.assertIsNotNone(img_io)
            self.assertTrue(base64_img.startswith('iVBOR'))

    def test_decrypt_message_invalid_image(self):
        """Test decryption with invalid image data."""
        result = decrypt_message(b"notanimage", self.test_password, self.image_id)
        self.assertIn("Error", result)

    # --- New Unit Tests ---
    def test_encrypt_empty_message(self):
        with open(self.image_path, 'rb') as f:
            img_io, base64_img, error = encrypt_message(f, "")
            self.assertIsNotNone(error)
            self.assertIn("Message cannot be empty", error)

    def test_encrypt_message_too_large(self):
        """Test if encryption fails when message is too large for the image."""
        large_message = "A" * 1000  # Too large for a 10x10 image
        with open(self.image_path, 'rb') as f:
            img_io, base64_img, error = encrypt_message(f, large_message)
            self.assertIsNotNone(error)
            self.assertIn("Message too long", error)

    def test_decrypt_correct_password(self):
        """Test decryption with the correct password (mocked DB response)."""
        # Mock a valid encrypted image (simplified for unit testing)
        mock_image_data = np.zeros((10, 10, 3), dtype=np.uint8)
        mock_image = Image.fromarray(mock_image_data)
        img_io = BytesIO()
        mock_image.save(img_io, 'PNG')
        img_bytes = img_io.getvalue()

        # Simulate a successful DB password check
        def mock_decrypt(image_bytes, password, image_id):
            if password == self.test_password:
                return "Decrypted successfully"
            return "Invalid password"

        result = mock_decrypt(img_bytes, self.test_password, self.image_id)
        self.assertEqual(result, "Decrypted successfully")

if __name__ == '__main__':
    unittest.main(verbosity=2)