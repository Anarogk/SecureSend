import unittest
from sftp_project.client.sftp_client import SFTPClient

class TestSFTPClient(unittest.TestCase):
    def setUp(self):
        self.client = SFTPClient("localhost", 2222, "testuser", "testpassword")

    def test_connection(self):
        # This test assumes a running SFTP server on localhost:2222
        # with the specified credentials
        try:
            self.client.connect()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Connection failed: {str(e)}")

    def tearDown(self):
        if self.client:
            self.client.disconnect()

if __name__ == '__main__':
    unittest.main()