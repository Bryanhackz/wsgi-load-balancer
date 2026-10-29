import unittest
import tempfile
from pathlib import Path
import db
import balancer

class BalancerTests(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        
        self.original_db_path = db.DB_PATH
        db.DB_PATH = Path(self.temp_db.name)
        db.init_db()
        
        # Reset round robin counter for clean tests
        balancer._current_index = 0

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        for suffix in ["", "-wal", "-shm"]:
            path = Path(self.temp_db.name + suffix)
            if path.exists():
                try:
                    path.unlink()
                except PermissionError:
                    pass

    def test_round_robin(self):
        # We registered 3 default backends in init_db
        b1 = balancer.get_next_backend()
        b2 = balancer.get_next_backend()
        b3 = balancer.get_next_backend()
        b4 = balancer.get_next_backend()

        self.assertEqual(b1, "http://127.0.0.1:8001")
        self.assertEqual(b2, "http://127.0.0.1:8002")
        self.assertEqual(b3, "http://127.0.0.1:8003")
        self.assertEqual(b4, "http://127.0.0.1:8001") # Wraps around

    def test_health_check_removes_backend(self):
        # Mark 8001 as dead
        db.update_health("http://127.0.0.1:8001", False)
        
        b1 = balancer.get_next_backend()
        b2 = balancer.get_next_backend()
        b3 = balancer.get_next_backend()

        # 8001 should be skipped
        self.assertEqual(b1, "http://127.0.0.1:8002")
        self.assertEqual(b2, "http://127.0.0.1:8003")
        self.assertEqual(b3, "http://127.0.0.1:8002")

    def test_no_healthy_backends(self):
        db.update_health("http://127.0.0.1:8001", False)
        db.update_health("http://127.0.0.1:8002", False)
        db.update_health("http://127.0.0.1:8003", False)
        
        self.assertIsNone(balancer.get_next_backend())

if __name__ == "__main__":
    unittest.main()