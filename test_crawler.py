import unittest
import json
import os
import hashlib
from parse_nobroker_complete import (
    make_hash,
    is_sobha_neopolis,
    is_project_match,
    get_facing,
    verify_listing_alive,
    PROJECTS
)

class TestSobhaCrawler(unittest.TestCase):
    
    def test_make_hash(self):
        """Test SHA-256 hash generation for NoBroker property IDs."""
        pid = "8aa99ecc98f9c9a10198f9fa7dae223a"
        expected_hash = hashlib.sha256(pid.encode()).hexdigest()[:8]
        self.assertEqual(make_hash(pid), expected_hash)
        self.assertEqual(len(make_hash(pid)), 8)

    def test_project_matchers(self):
        """Test project filter matchers for all 4 Sobha projects."""
        self.assertTrue(is_project_match({"society": "Sobha Neopolis"}, PROJECTS["sobha-neopolis"]))
        self.assertTrue(is_project_match({"propertyTitle": "3 BHK In Sobha Royal Pavilion"}, PROJECTS["sobha-royal-pavilion"]))
        self.assertTrue(is_project_match({"society": "Sobha Windsor"}, PROJECTS["sobha-windsor"]))
        self.assertTrue(is_project_match({"propertyTitle": "2 BHK Flat In Sobha Sentosa"}, PROJECTS["sobha-sentosa"]))
        
        self.assertFalse(is_project_match({"society": "Prestige Lavender Fields"}, PROJECTS["sobha-neopolis"]))
        self.assertFalse(is_project_match({"propertyTitle": "Brigade Utopia"}, PROJECTS["sobha-royal-pavilion"]))

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

    def test_all_multi_project_data_files(self):
        """Validate schema integrity for all 4 Sobha project JSON files in data/."""
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "data")
        self.assertTrue(os.path.exists(data_dir), "data/ directory must exist")
        
        required_keys = [
            "id", "hash", "title", "floor", "total_floors", "area",
            "facing", "possession", "price", "price_raw", "source",
            "link", "first_seen", "last_seen", "status"
        ]
        
        for pkey, pconfig in PROJECTS.items():
            safe_key = pkey.replace("-", "_")
            json_path = os.path.join(data_dir, f"{safe_key}_listings.json")
            self.assertTrue(os.path.exists(json_path), f"JSON for {pkey} must exist at {json_path}")
            
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.assertIn("active", data)
            self.assertIn("delisted", data)
            self.assertEqual(data.get("project_key"), pkey)
            self.assertGreaterEqual(len(data["active"]), 0)
            
            for item in data["active"]:
                for key in required_keys:
                    self.assertIn(key, item, f"Missing key '{key}' in {pkey} item {item.get('hash')}")
                self.assertGreater(item["price_raw"], 0, f"price_raw should be > 0 in {pkey} item {item['hash']}")
                self.assertGreater(item["area"], 0, f"area should be > 0 in {pkey} item {item['hash']}")

    def test_summary_json_file(self):
        """Validate all_projects_summary.json contains all 4 projects."""
        summary_path = os.path.join(os.path.dirname(__file__), "data", "all_projects_summary.json")
        self.assertTrue(os.path.exists(summary_path), "all_projects_summary.json must exist")
        
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
            
        for pkey in PROJECTS:
            self.assertIn(pkey, summary, f"{pkey} missing from all_projects_summary.json")
            self.assertIn("active_count", summary[pkey])

if __name__ == "__main__":
    unittest.main()
