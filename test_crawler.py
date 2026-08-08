import unittest
import json
import os
import hashlib
from parse_nobroker_complete import make_hash, is_sobha_neopolis, get_facing, verify_listing_alive

class TestSobhaCrawler(unittest.TestCase):
    
    def test_make_hash(self):
        """Test SHA-256 hash generation for NoBroker property IDs."""
        pid = "8aa99ecc98f9c9a10198f9fa7dae223a"
        expected_hash = hashlib.sha256(pid.encode()).hexdigest()[:8]
        self.assertEqual(make_hash(pid), expected_hash)
        self.assertEqual(len(make_hash(pid)), 8)

    def test_is_sobha_neopolis(self):
        """Test project filter for Sobha Neopolis listings."""
        self.assertTrue(is_sobha_neopolis({"society": "Sobha Neopolis"}))
        self.assertTrue(is_sobha_neopolis({"propertyTitle": "3 BHK Flat In Shobha Neopolis For Sale"}))
        self.assertFalse(is_sobha_neopolis({"society": "Prestige Lavender Fields"}))
        self.assertFalse(is_sobha_neopolis({"propertyTitle": "2 BHK Flat In Brigade Utopia"}))

    def test_get_facing(self):
        """Test direction string normalization."""
        self.assertEqual(get_facing({"facing": "East"}), "East")
        self.assertEqual(get_facing({"facingDesc": "West"}), "West")
        self.assertEqual(get_facing({"facing": "N"}), "North")
        self.assertEqual(get_facing({"facing": "Ne"}), "North-East")
        self.assertEqual(get_facing({"facing": "0"}), "N/A")
        self.assertEqual(get_facing({"facing": "None"}), "N/A")
        self.assertEqual(get_facing({"facing": ""}), "N/A")

    def test_verify_listing_alive_safeguard(self):
        """Test URL verification safeguard logic on dead vs invalid URLs."""
        self.assertTrue(verify_listing_alive(""))
        self.assertTrue(verify_listing_alive("https://invalid-url-domain.com/123"))

    def test_listings_json_schema(self):
        """Validate sobha_listings.json schema and item fields."""
        json_path = os.path.join(os.path.dirname(__file__), "sobha_listings.json")
        self.assertTrue(os.path.exists(json_path), "sobha_listings.json must exist")
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assertIn("active", data)
        self.assertGreater(len(data["active"]), 0, "active listings should not be empty")
        
        required_keys = [
            "id", "hash", "title", "floor", "total_floors", "area",
            "facing", "possession", "price", "price_raw", "source",
            "link", "first_seen", "last_seen", "status"
        ]
        
        for item in data["active"]:
            for key in required_keys:
                self.assertIn(key, item, f"Missing key '{key}' in item hash {item.get('hash')}")
            self.assertGreater(item["price_raw"], 0, f"price_raw should be > 0 in item {item['hash']}")
            self.assertGreater(item["area"], 0, f"area should be > 0 in item {item['hash']}")

    def test_history_json_schema(self):
        """Validate sobha_history.json schema integrity."""
        history_path = os.path.join(os.path.dirname(__file__), "sobha_history.json")
        self.assertTrue(os.path.exists(history_path), "sobha_history.json must exist")
        
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
            
        self.assertGreater(len(history), 0, "sobha_history.json should contain entries")
        
        for uid, entry in history.items():
            self.assertEqual(len(uid), 8, f"Hash key {uid} in history must be 8 characters")
            self.assertIn("status", entry)
            self.assertIn(entry["status"], ["active", "delisted"])
            self.assertGreater(entry.get("price_raw", 0), 0)

    def test_purchases_json_schema(self):
        """Validate purchases.json format."""
        purchases_path = os.path.join(os.path.dirname(__file__), "purchases.json")
        if os.path.exists(purchases_path):
            with open(purchases_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, list, "purchases.json must contain a JSON array")

if __name__ == "__main__":
    unittest.main()
