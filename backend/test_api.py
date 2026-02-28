"""
Test script for authentication API endpoints
Run this after starting the Flask app: python app.py
Then in another terminal: python test_api.py
"""

import requests
import json
from datetime import datetime
from app import create_app

BASE_URL = 'http://localhost:5000/api'

# Test data
TEST_USER = {
    'username': f'testuser_{int(datetime.now().timestamp())}',
    'email': f'testuser_{int(datetime.now().timestamp())}@example.com',
    'password': 'TestPassword123'
}

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print()

def test_health():
    """Test health check endpoint"""
    response = requests.get(f'{BASE_URL}/health')
    print_response('Health Check', response)
    return response.status_code == 200

def test_signup():
    """Test user signup"""
    response = requests.post(
        f'{BASE_URL}/auth/signup',
        json=TEST_USER,
        headers={'Content-Type': 'application/json'}
    )
    print_response('User Signup', response)
    
    if response.status_code == 201:
        data = response.json()
        TEST_USER['token'] = data.get('token')
        return True
    return False

def test_duplicate_signup():
    """Test signup with duplicate username (should fail)"""
    response = requests.post(
        f'{BASE_URL}/auth/signup',
        json=TEST_USER,
        headers={'Content-Type': 'application/json'}
    )
    print_response('Duplicate Signup (Should Fail)', response)
    return response.status_code == 409

def test_invalid_signup():
    """Test signup with invalid data (should fail)"""
    invalid_data = {
        'username': 'ab',  # Too short
        'email': 'invalid@example.com',
        'password': '123'  # Too short
    }
    response = requests.post(
        f'{BASE_URL}/auth/signup',
        json=invalid_data,
        headers={'Content-Type': 'application/json'}
    )
    print_response('Invalid Signup (Should Fail)', response)
    return response.status_code == 400

def test_login():
    """Test user login"""
    response = requests.post(
        f'{BASE_URL}/auth/login',
        json={
            'username': TEST_USER['username'],
            'password': TEST_USER['password']
        },
        headers={'Content-Type': 'application/json'}
    )
    print_response('User Login', response)
    return response.status_code == 200

def test_login_invalid_password():
    """Test login with wrong password (should fail)"""
    response = requests.post(
        f'{BASE_URL}/auth/login',
        json={
            'username': TEST_USER['username'],
            'password': 'WrongPassword123'
        },
        headers={'Content-Type': 'application/json'}
    )
    print_response('Login with Invalid Password (Should Fail)', response)
    return response.status_code == 401

def test_get_profile():
    """Test getting user profile (protected endpoint)"""
    if 'token' not in TEST_USER:
        print("Skipping profile test - no token available")
        return False
    
    response = requests.get(
        f'{BASE_URL}/auth/profile',
        headers={
            'Authorization': f"Bearer {TEST_USER['token']}",
            'Content-Type': 'application/json'
        }
    )
    print_response('Get User Profile', response)
    return response.status_code == 200

def test_get_profile_no_token():
    """Test getting profile without token (should fail)"""
    response = requests.get(
        f'{BASE_URL}/auth/profile',
        headers={'Content-Type': 'application/json'}
    )
    print_response('Get Profile Without Token (Should Fail)', response)
    return response.status_code == 401

def test_logout():
    """Test logout endpoint"""
    if 'token' not in TEST_USER:
        print("Skipping logout test - no token available")
        return False
    
    response = requests.post(
        f'{BASE_URL}/auth/logout',
        headers={
            'Authorization': f"Bearer {TEST_USER['token']}",
            'Content-Type': 'application/json'
        }
    )
    print_response('User Logout', response)
    return response.status_code == 200

def test_verify_location():
    """Test location verification endpoint"""
    if 'token' not in TEST_USER:
        print("Skipping location verification test - no token available")
        return False
    
    # Test with Times Square, New York coordinates
    location_data = {
        'lat': 40.7580,  # Times Square latitude
        'lng': -73.9855,  # Times Square longitude
        'target_address': 'Times Square, New York, NY'
    }
    
    response = requests.post(
        f'{BASE_URL}/location/verify',
        json=location_data,
        headers={
            'Authorization': f"Bearer {TEST_USER['token']}",
            'Content-Type': 'application/json'
        }
    )
    print_response('Verify Location', response)
    return response.status_code == 200

def test_verify_location_invalid():
    """Test location verification with invalid address"""
    if 'token' not in TEST_USER:
        print("Skipping invalid location test - no token available")
        return False
    
    location_data = {
        'lat': 40.7580,
        'lng': -73.9855,
        'target_address': 'INVALID_ADDRESS_THAT_DOES_NOT_EXIST_123456789'
    }
    
    response = requests.post(
        f'{BASE_URL}/location/verify',
        json=location_data,
        headers={
            'Authorization': f"Bearer {TEST_USER['token']}",
            'Content-Type': 'application/json'
        }
    )
    print_response('Verify Location with Invalid Address (Should Fail)', response)
    return response.status_code == 404

def test_get_location_history():
    """Test getting user's location history"""
    if 'token' not in TEST_USER:
        print("Skipping location history test - no token available")
        return False
    
    response = requests.get(
        f'{BASE_URL}/location/history',
        headers={
            'Authorization': f"Bearer {TEST_USER['token']}",
            'Content-Type': 'application/json'
        }
    )
    print_response('Get Location History', response)
    return response.status_code == 200

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AUTHENTICATION API TEST SUITE")
    print("="*60)
    
    tests = [
        ('Health Check', test_health),
        ('User Signup', test_signup),
        ('Duplicate Signup', test_duplicate_signup),
        ('Invalid Signup', test_invalid_signup),
        ('User Login', test_login),
        ('Login Invalid Password', test_login_invalid_password),
        ('Get Profile Without Token', test_get_profile_no_token),
        ('Get User Profile', test_get_profile),
        ('Verify Location', test_verify_location),
        ('Verify Location Invalid Address', test_verify_location_invalid),
        ('Get Location History', test_get_location_history),
        ('User Logout', test_logout),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ERROR: Could not connect to server. Make sure app.py is running!")
            return
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTests Passed: {passed}/{total}")
    print()
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

if __name__ == '__main__':
    run_all_tests()
