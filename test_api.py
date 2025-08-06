#!/usr/bin/env python3
"""
Test script for YouTube Pro Backend API
Run this script to test all API endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_signup():
    """Test user signup"""
    print("\nTesting user signup...")
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/signup", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [201, 409]  # 201 for new user, 409 if already exists
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/login", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_users():
    """Test get all users"""
    print("\nTesting get all users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_user():
    """Test get specific user"""
    print("\nTesting get specific user...")
    try:
        response = requests.get(f"{BASE_URL}/users/1")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_user():
    """Test update user"""
    print("\nTesting update user...")
    data = {
        "name": "Updated Test User"
    }
    try:
        response = requests.put(f"{BASE_URL}/users/1", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_stats():
    """Test get statistics"""
    print("\nTesting get statistics...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_about():
    """Test about endpoint"""
    print("\nTesting about endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/about")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("YouTube Pro Backend API Test Suite")
    print("=" * 50)
    
    # Wait a moment for API to be ready
    print("Waiting for API to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health_check),
        ("Signup", test_signup),
        ("Login", test_login),
        ("Get All Users", test_get_users),
        ("Get Specific User", test_get_user),
        ("Update User", test_update_user),
        ("Statistics", test_stats),
        ("About", test_about)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API and database connection.")

if __name__ == "__main__":
    main() 