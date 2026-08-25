import unittest
import json
import os
import hashlib
from bs4 import BeautifulSoup
from parse_nobroker_complete import (
    make_hash,
    is_sobha_neopolis,
    is_project_match,
    get_facing,
    verify_listing_alive,
    parse_mb_price,
    normalize_property_area,
    _parse_mb_card,
    PROJECTS
)

class TestSobhaCrawler(unittest.TestCase):
    
    def test_make_hash(self):
        """Test SHA-256 hash generation for property IDs."""
        pid = "8aa99ecc98f9c9a10198f9fa7dae223a"
        expected_hash = hashlib.sha256(pid.encode()).hexdigest()[:8]
        self.assertEqual(make_hash(pid), expected_hash)
        self.assertEqual(len(make_hash(pid)), 8)

    def test_parse_mb_price(self):
        """Test MagicBricks price string conversion to integer."""
        self.assertEqual(parse_mb_price("₹3.67 Cr"), 36700000)
        self.assertEqual(parse_mb_price("₹ 2.45 Cr"), 24500000)
        self.assertEqual(parse_mb_price("₹ 85 Lac"), 8500000)
        self.assertEqual(parse_mb_price("₹ 95 Lakhs"), 9500000)
        self.assertEqual(parse_mb_price("₹ 50 k"), 50000)
        self.assertEqual(parse_mb_price(""), 0)

    def test_normalize_property_area_sba_passthrough(self):
        """Known SBA values (from the whitelist) are returned unchanged."""
        self.assertEqual(normalize_property_area("Any Flat", 1611), 1611)
        self.assertEqual(normalize_property_area("Any Flat", 2481), 2481)
        self.assertEqual(normalize_property_area("Any Flat", 1915), 1915)
        self.assertEqual(normalize_property_area("Any Flat", 2150), 2150)

    def test_normalize_property_area_carpet_to_sba_4bhk(self):
        """4 BHK with carpet area < 2000 must be converted to SBA 2481.

        Root cause of the reported bug: MagicBricks shows 1617 sqft as
        Carpet Area for Sobha Neopolis 4 BHK; the actual SBA is 2481.
        """
        # Typical Sobha Neopolis 4BHK: ~1617 sqft carpet → 2481 sqft SBA
        self.assertEqual(normalize_property_area("4 BHK Flat for Sale in Panathur, Bangalore", 1617), 2481)
        # Any other 4BHK carpet area below 2000
        self.assertEqual(normalize_property_area("4 BHK Flat", 1800), 2481)
        # Actual SBA value for 4BHK is preserved
        self.assertEqual(normalize_property_area("4 BHK Flat", 2481), 2481)

    def test_normalize_property_area_carpet_to_sba_3bhk(self):
        """3 BHK carpet area ranges (~0.65 carpet-to-SBA ratio) map to the correct SBA tier."""
        # 1040 sqft carpet area (~1040 / 0.65 = 1600) -> Neopolis 3BHK Standard SBA (1611)
        self.assertEqual(normalize_property_area("3 BHK Flat for Sale in Panathur, Bangalore", 1040), 1611)
        self.assertEqual(normalize_property_area("3 BHK Flat", 1100), 1611)

        # 1240 sqft carpet area (~1240 / 0.65 = 1907) -> Neopolis 3BHK Luxury SBA (1915)
        self.assertEqual(normalize_property_area("3 BHK Flat for Sale in Panathur, Bangalore", 1240), 1915)

        # 1400 sqft carpet area (~1400 / 0.65 = 2153) -> Neopolis 3BHK Large SBA (2150)
        self.assertEqual(normalize_property_area("3 BHK Flat for Sale in Panathur, Bangalore", 1400), 2150)

        # Known SBA values pass through unchanged
        self.assertEqual(normalize_property_area("3 BHK Flat", 1611), 1611)
        self.assertEqual(normalize_property_area("3 BHK Flat", 1915), 1915)
        self.assertEqual(normalize_property_area("3 BHK Flat", 2150), 2150)

    def test_parse_mb_card_super_area_no_conversion(self):
        """Card labelled 'Super Area' should store the value as-is (no carpet conversion)."""
        html = '''
        <div class="mb-srp__card">
          <h2 class="mb-srp__card--title">4 BHK Flat for Sale in Panathur, Bangalore</h2>
          <div class="mb-srp__card__summary__list--item">
            <span class="mb-srp__card__summary--label">Super Area</span>
            <span class="mb-srp__card__summary--value">2481 sqft</span>
          </div>
          <span class="mb-srp__card__price--amount">₹4.10 Cr</span>
          <a href="https://www.magicbricks.com/propertyDetails/test&id=abc123">Link</a>
        </div>'''
        c = BeautifulSoup(html, 'html.parser').select_one('.mb-srp__card')
        result = _parse_mb_card(c, PROJECTS['sobha-neopolis'], 'https://www.magicbricks.com')
        self.assertEqual(result['area'], 2481, "Super Area 2481 should be stored as-is")
        self.assertEqual(result['source'], 'MagicBricks')
        self.assertEqual(result['price_raw'], 41000000)

    def test_parse_mb_card_carpet_area_converted(self):
        """Card labelled 'Carpet Area' with 1617 sqft must convert to 2481 SBA for 4 BHK."""
        html = '''
        <div class="mb-srp__card">
          <h2 class="mb-srp__card--title">4 BHK Flat for Sale in Panathur, Bangalore</h2>
          <div class="mb-srp__card__summary__list--item">
            <span class="mb-srp__card__summary--label">Carpet Area</span>
            <span class="mb-srp__card__summary--value">1617 sqft</span>
          </div>
          <span class="mb-srp__card__price--amount">₹4.10 Cr</span>
          <a href="https://www.magicbricks.com/propertyDetails/test&id=abc456">Link</a>
        </div>'''
        c = BeautifulSoup(html, 'html.parser').select_one('.mb-srp__card')
        result = _parse_mb_card(c, PROJECTS['sobha-neopolis'], 'https://www.magicbricks.com')
        self.assertEqual(result['area'], 2481,
            "Carpet Area 1617 sqft for 4 BHK must be converted to SBA 2481")
        self.assertEqual(result['source'], 'MagicBricks')

    def test_project_matchers(self):
        """Test project filter matchers for Sobha Neopolis."""
        self.assertTrue(is_project_match({"society": "Sobha Neopolis"}, PROJECTS["sobha-neopolis"]))
        self.assertFalse(is_project_match({"society": "Prestige Lavender Fields"}, PROJECTS["sobha-neopolis"]))

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

    def test_verify_listing_alive_inactive_nobroker(self):
        """Verify that NoBroker inactive/sold listings (with -Inactive title or overlay-rented-out class) are detected as dead."""
        # The user's provided inactive URL must return False (delisted/inactive)
        self.assertFalse(verify_listing_alive("https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-sobha-neopolis-bangalore/8aa9b3249cf506e8019cf52284310a54/detail"))

    def test_all_multi_project_data_files(self):
        """Validate schema integrity & multi-source support for all 4 project JSON files."""
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
                self.assertIn(item["source"], ["NoBroker", "MagicBricks"], f"Invalid source '{item['source']}' in {pkey} item {item['hash']}")
                self.assertGreater(item["price_raw"], 0, f"price_raw should be > 0 in {pkey} item {item['hash']}")
                self.assertGreater(item["area"], 0, f"area should be > 0 in {pkey} item {item['hash']}")
                # A 4 BHK must never be stored with Neopolis 3BHK area (1611) — catches carpet/SBA mismatch
                if "4 bhk" in item["title"].lower() or "4bhk" in item["title"].lower():
                    self.assertGreaterEqual(item["area"], 2000,
                        f"4 BHK area {item['area']} sqft is suspiciously small (carpet area bug?) in {pkey} item {item['hash']}")

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
