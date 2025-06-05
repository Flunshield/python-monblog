#!/usr/bin/env python3
"""
Test script to verify the Gemini generator functionality
"""

import requests
import json
import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_gemini_generator():
    """Test the Gemini generator endpoint"""
    
    # First, get the CSRF token
    session = requests.Session()
    
    print("🧪 Testing Gemini Generator...")
    
    # Get the generator page to obtain CSRF token
    try:
        response = session.get('http://localhost:8000/fr/gemini-generator/')
        if response.status_code == 200:
            print("✅ Generator page loads successfully")
            
            # Extract CSRF token (simple approach)
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
                
                # Test the API endpoint
                test_data = {
                    'resume': 'Write a short article about artificial intelligence in healthcare',
                    'langue': 'en'
                }
                
                headers = {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': 'application/json',
                    'Referer': 'http://localhost:8000/fr/gemini-generator/'
                }
                
                # Add cookies from the session
                api_response = session.post(
                    'http://localhost:8000/generate-article-ai/',
                    json=test_data,
                    headers=headers
                )
                
                print(f"📡 API Response Status: {api_response.status_code}")
                
                if api_response.status_code == 200:
                    result = api_response.json()
                    if result.get('success'):
                        print("✅ Article generated successfully!")
                        print(f"📝 Title: {result.get('titre', 'N/A')}")
                        print(f"📄 Content length: {len(result.get('contenu', ''))} characters")
                        return True
                    else:
                        print(f"❌ API returned error: {result.get('error', 'Unknown error')}")
                else:
                    print(f"❌ API request failed with status {api_response.status_code}")
                    print(f"Response: {api_response.text}")
            else:
                print("❌ Could not extract CSRF token")
        else:
            print(f"❌ Failed to load generator page: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 Starting Gemini Generator Test")
    print("=" * 50)
    
    success = test_gemini_generator()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Your Gemini generator is working perfectly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
