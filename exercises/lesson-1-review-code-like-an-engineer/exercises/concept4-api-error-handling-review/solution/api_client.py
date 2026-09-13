"""
Code Review Solution 4: Fixed API Client

Key Issues Fixed:
1. Network error handling -> try/catch for timeouts and connection errors
2. HTTP status code handling -> check for common error codes
3. Error information -> return error details instead of just None
4. Input validation -> basic parameter validation
"""

import requests
import json

class APIClient:
    def __init__(self, base_url, api_key):
        # Basic input validation
        if not base_url:
            raise ValueError("Base URL cannot be empty")
        if not api_key:
            raise ValueError("API key cannot be empty")
        
        self.base_url = base_url.rstrip('/')  # Remove trailing slash
        self.api_key = api_key

    def get_user_data(self, user_id):
        """Get user data with proper error handling."""
        # Basic input validation
        if not user_id:
            raise ValueError("User ID cannot be empty")
        
        url = f"{self.base_url}/users/{user_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            # FIXED: Handle network errors with try/catch
            response = requests.get(url, headers=headers, timeout=5)
            
            # FIXED: Check different HTTP status codes
            if response.status_code == 200:
                return response.json()  # FIXED: Use response.json() instead of json.loads()
            elif response.status_code == 404:
                return {"error": "User not found"}
            elif response.status_code == 401:
                return {"error": "Unauthorized - check API key"}
            elif response.status_code >= 500:
                return {"error": "Server error - try again later"}
            else:
                return {"error": f"Request failed with status {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            return {"error": "Failed to connect to server"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def update_user(self, user_id, data):
        """Update user with proper error handling."""
        # Basic input validation
        if not user_id:
            raise ValueError("User ID cannot be empty")
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary")
        
        url = f"{self.base_url}/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"  # FIXED: Add proper content type
        }
        
        try:
            # FIXED: Handle network errors with try/catch
            response = requests.put(url, headers=headers, json=data, timeout=5)  # FIXED: Use json parameter
            
            # FIXED: Return detailed results instead of just True/False
            if response.status_code == 200:
                return {"success": True, "message": "User updated successfully"}
            elif response.status_code == 404:
                return {"success": False, "error": "User not found"}
            elif response.status_code == 401:
                return {"success": False, "error": "Unauthorized - check API key"}
            elif response.status_code >= 500:
                return {"success": False, "error": "Server error - try again later"}
            else:
                return {"success": False, "error": f"Update failed with status {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Failed to connect to server"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}


# Test the improved API client
if __name__ == "__main__":
    print("=== Testing Improved API Client ===")
    print("This version handles errors gracefully!\n")
    
    try:
        # Test initialization validation
        client = APIClient("https://httpbin.org", "test-key")
        print("✓ Client created successfully")
        
        print("\n1. Testing successful request...")
        result = client.get_user_data("get")
        if "error" in result:
            print(f"✗ Error: {result['error']}")
        else:
            print("✓ Success: Got user data")
        
        print("\n2. Testing 404 error handling...")
        result = client.get_user_data("nonexistent")
        if "error" in result:
            print(f"✓ Handled 404 gracefully: {result['error']}")
        else:
            print("Got unexpected success")
        
        print("\n3. Testing network error handling...")
        bad_client = APIClient("https://nonexistent-domain-12345.com", "key")
        result = bad_client.get_user_data(123)
        if "error" in result:
            print(f"✓ Handled network error gracefully: {result['error']}")
        else:
            print("Got unexpected success")
        
        print("\n4. Testing input validation...")
        try:
            client.get_user_data("")  # Empty user ID
        except ValueError as e:
            print(f"✓ Input validation works: {e}")
        
        print("\n=== Key Improvements ===")
        print("✓ Network errors are caught and handled")
        print("✓ HTTP status codes are checked and explained")
        print("✓ Users get helpful error messages")
        print("✓ Input validation prevents bad requests")
        print("✓ Functions return structured results")
        
    except Exception as e:
        print(f"Unexpected error: {e}")