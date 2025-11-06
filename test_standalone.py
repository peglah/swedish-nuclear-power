#!/usr/bin/env python3
"""
Standalone test for Swedish Nuclear Power data fetching
"""

import sys
import os
import json
import requests
import re
from datetime import datetime

# Plant configurations
PLANTS = {
    "ringhals": {
        "name": "Ringhals",
        "url": "https://karnkraft.vattenfall.se/ringhals/produktion",
        "reactors": ["R3", "R4"],
        "max_capacity": {"R3": 1074, "R4": 1130},  # Maximum capacity in MW from technical data
    },
    "forsmark": {
        "name": "Forsmark", 
        "url": "https://karnkraft.vattenfall.se/forsmark/produktion",
        "reactors": ["F1", "F2", "F3"],
        "max_capacity": {"F1": 1014, "F2": 1121, "F3": 1172},  # Maximum capacity in MW from technical data
    },
    "okg": {
        "name": "Oskarshamn",
        "url": "https://okg.se/.netlify/functions/getReactorOutput",
        "reactors": ["O3"],
        "api": True,
        "max_capacity": {"O3": 1450},  # Maximum capacity in MW for percentage calculation
    },
}

class NuclearDataFetcher:
    """Standalone nuclear data fetcher for testing."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_all_plants(self):
        """Fetch data from all nuclear plants."""
        all_data = {}
        
        for plant_key, plant_config in PLANTS.items():
            try:
                if plant_config.get("api", False):
                    # O3 API call
                    data = self.fetch_okg_data(plant_config)
                else:
                    # Vattenfall scraping
                    data = self.fetch_vattenfall_data(plant_key, plant_config)
                
                if data:
                    all_data[plant_key] = data
                    
            except Exception as e:
                print(f"❌ Failed to fetch data from {plant_config['name']}: {e}")
                continue
        
        return all_data
    
    def fetch_vattenfall_data(self, plant_key, plant_config):
        """Fetch data from Vattenfall plants."""
        try:
            url = plant_config["url"]
            print(f"📡 Fetching data from {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = self.extract_production_data(response.text, plant_key)
            if data:
                print(f"✅ Successfully extracted data for {plant_key}")
                return data
            else:
                print(f"❌ Failed to extract data from {plant_key}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ Request error for {plant_key}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error for {plant_key}: {e}")
            return None
    
    def extract_production_data(self, html_content, plant_name):
        """Extract production data from JSON embedded in HTML."""
        try:
            # Look for JSON data in script tags
            pattern = r'<script[^>]*type="application/json"[^>]*>(.*?)</script>'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            for match in matches:
                try:
                    json_data = json.loads(match.strip())
                    if 'powerPlant' in json_data and 'blockProductionDataList' in json_data:
                        if json_data['powerPlant'].lower() == plant_name.lower():
                            return {
                                'timestamp': json_data.get('timestamp'),
                                'power_plant': json_data['powerPlant'],
                                'data': json_data['blockProductionDataList']
                            }
                except json.JSONDecodeError:
                    continue
            
            print(f"⚠️ No valid JSON data found for {plant_name}")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting data for {plant_name}: {e}")
            return None
    
    def fetch_okg_data(self, plant_config):
        """Fetch data from OKG O3 API."""
        try:
            url = plant_config["url"]
            print(f"📡 Fetching data from {url}")
            
            # OKG API requires format parameter
            response = self.session.get(f"{url}?format=json", timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Calculate percentage for O3 using max capacity
            max_capacity = plant_config.get("max_capacity", {}).get("O3", 1450)
            current_power = data.get('value', 0)
            percentage = (current_power / max_capacity * 100) if max_capacity > 0 else 0
            
            # OKG returns single reactor data
            return {
                'timestamp': data.get('timestamp'),
                'power_plant': plant_config['name'],
                'data': [{
                    'name': 'O3',
                    'production': current_power,
                    'percent': round(percentage, 1),
                    'unit': 'MW',
                    'valueDate': data.get('valueDate')
                }]
            }
            
        except requests.RequestException as e:
            print(f"❌ Request error for OKG: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error for OKG: {e}")
            return None

def test_integration():
    """Test integration data fetching."""
    print("🚀 Swedish Nuclear Power Integration Test")
    print("=" * 50)
    
    fetcher = NuclearDataFetcher()
    
    print("📊 Plant Details:")
    for plant_key, plant_config in PLANTS.items():
        print(f"  • {plant_config['name']} ({plant_key})")
        print(f"    Reactors: {plant_config['reactors']}")
        print(f"    API: {plant_config.get('api', False)}")
    
    print("\n🔄 Fetching data from all plants...")
    data = fetcher.fetch_all_plants()
    
    if data:
        print(f"✅ Successfully fetched data from {len(data)} plants")
        
        total_power = 0
        reactor_count = 0
        active_reactors = 0
        
        for plant_key, plant_data in data.items():
            plant_name = plant_data.get('power_plant', plant_key)
            timestamp = plant_data.get('timestamp', 'N/A')
            reactors = plant_data.get('data', [])
            
            print(f"\n🏭 {plant_name}:")
            print(f"   Timestamp: {timestamp}")
            print(f"   Reactors: {len(reactors)}")
            
            for reactor in reactors:
                name = reactor.get('name', 'Unknown')
                power = reactor.get('production', 0)
                percent = reactor.get('percent')
                
                if percent is not None:
                    print(f"     • {name}: {power} MW ({percent:.1f}%)")
                else:
                    print(f"     • {name}: {power} MW")
                total_power += power
                reactor_count += 1
                if power > 0:
                    active_reactors += 1
        
        print(f"\n⚡ Total Swedish Nuclear Power: {total_power:.2f} MW")
        print(f"📊 Reactor Status: {active_reactors}/{reactor_count} active")
        print("✅ Integration test completed successfully!")
        
        # Generate sensor list
        print(f"\n🏠 Home Assistant Sensors that will be created:")
        for plant_key, plant_config in PLANTS.items():
            for reactor in plant_config['reactors']:
                print(f"  • sensor.{plant_key}_{reactor.lower()}_power")
            print(f"  • sensor.{plant_key}_last_update")
        print(f"  • sensor.swedish_nuclear_power_total_power")
        
    else:
        print("❌ No data fetched from any plant")

def test_file_structure():
    """Test if all required files exist."""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'custom_components/swedish_nuclear_power/__init__.py',
        'custom_components/swedish_nuclear_power/manifest.json',
        'custom_components/swedish_nuclear_power/const.py',
        'custom_components/swedish_nuclear_power/config_flow.py',
        'custom_components/swedish_nuclear_power/coordinator.py',
        'custom_components/swedish_nuclear_power/sensor.py',
        'custom_components/swedish_nuclear_power/options.py',
        'custom_components/swedish_nuclear_power/translations/en.json',
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files")
        return False
    else:
        print("\n✅ All required files present")
        return True

def test_manifest():
    """Test manifest.json validity."""
    print("\n📋 Testing manifest.json...")
    
    try:
        with open('custom_components/swedish_nuclear_power/manifest.json', 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['domain', 'name', 'version', 'integration_type', 'iot_class']
        missing_fields = []
        
        for field in required_fields:
            if field in manifest:
                print(f"✅ {field}: {manifest[field]}")
            else:
                print(f"❌ {field}: missing")
                missing_fields.append(field)
        
        if not missing_fields:
            print("✅ Manifest is valid")
            return True
        else:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in manifest.json: {e}")
        return False
    except FileNotFoundError:
        print("❌ manifest.json not found")
        return False

if __name__ == "__main__":
    print("🔬 Swedish Nuclear Power Integration Test Suite")
    print("=" * 60)
    
    # Test file structure
    structure_ok = test_file_structure()
    
    # Test manifest
    manifest_ok = test_manifest()
    
    if structure_ok and manifest_ok:
        # Run integration test
        test_integration()
    else:
        print("\n❌ Basic tests failed, skipping integration test")
        sys.exit(1)