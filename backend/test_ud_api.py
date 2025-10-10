#!/usr/bin/env python3
"""
Test that UD rules are available via API
"""

import requests
import json

def test_ud_api():
    """
    Test the API endpoints for UD rules
    """
    base_url = "http://localhost:8000"
    
    print("🧪 Testing UD Rules API Integration")
    print("=" * 50)
    
    # Test 1: Get all grammar rules
    try:
        response = requests.get(f"{base_url}/grammar/rules")
        if response.status_code == 200:
            rules = response.json()
            ud_rules = [r for r in rules if r.get('usage_context') in ['universal_dependencies', 'enhanced_ud']]
            print(f"✅ Found {len(ud_rules)} UD-based rules via API")
            
            # Show some UD rules
            if ud_rules:
                print(f"\n📝 Sample UD Rules:")
                for rule in ud_rules[:3]:
                    print(f"  - {rule['language_id']}: {rule['rule_name']}")
        else:
            print(f"❌ API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    # Test 2: Get rules for specific languages with UD data
    languages = ['zh', 'de', 'ja', 'ru']
    for lang in languages:
        try:
            response = requests.get(f"{base_url}/grammar/rules/{lang}")
            if response.status_code == 200:
                rules = response.json()
                ud_rules = [r for r in rules if r.get('usage_context') in ['universal_dependencies', 'enhanced_ud']]
                print(f"  {lang}: {len(ud_rules)} UD rules")
            else:
                print(f"  {lang}: API error {response.status_code}")
        except Exception as e:
            print(f"  {lang}: Failed - {e}")
    
    # Test 3: Check if examples are included
    try:
        response = requests.get(f"{base_url}/grammar/rules/zh")
        if response.status_code == 200:
            rules = response.json()
            if rules:
                first_rule = rules[0]
                if 'examples' in first_rule and first_rule['examples']:
                    print(f"✅ Examples are included in API responses")
                    print(f"   Sample: {first_rule['examples'][0]['example_sentence'][:50]}...")
                else:
                    print(f"❌ No examples found in API response")
        else:
            print(f"❌ API test failed")
    except Exception as e:
        print(f"❌ Example test failed: {e}")

if __name__ == '__main__':
    test_ud_api()