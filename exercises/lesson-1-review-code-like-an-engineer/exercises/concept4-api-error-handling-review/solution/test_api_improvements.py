"""Tests for improved API error handling."""

import pytest
from unittest.mock import patch, Mock
from api_client import APIClient


class TestImprovedAPIInitialization:
    """Tests for improved API client initialization."""
    
    def test_api_client_validates_base_url(self):
        """Test that API client validates base URL."""
        with pytest.raises(ValueError, match="Base URL cannot be empty"):
            APIClient("", "test-key")
        
        with pytest.raises(ValueError, match="Base URL cannot be empty"):
            APIClient(None, "test-key")
    
    def test_api_client_validates_api_key(self):
        """Test that API client validates API key."""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            APIClient("https://api.example.com", "")
        
        with pytest.raises(ValueError, match="API key cannot be empty"):
            APIClient("https://api.example.com", None)
    
    def test_api_client_accepts_valid_parameters(self):
        """Test that valid parameters are accepted."""
        client = APIClient("https://api.example.com", "test-key")
        assert client.base_url == "https://api.example.com"
        assert client.api_key == "test-key"


class TestImprovedNetworkErrorHandling:
    """Tests for improved network error handling."""
    
    @patch('api_client.requests.get')
    def test_timeout_error_handled_gracefully(self, mock_get):
        """Test that timeout errors are handled gracefully."""
        import requests
        
        # Mock a timeout error
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return error info instead of crashing
        assert "error" in result
        assert "timed out" in result["error"]
    
    @patch('api_client.requests.get')
    def test_connection_error_handled_gracefully(self, mock_get):
        """Test that connection errors are handled gracefully."""
        import requests
        
        # Mock a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return error info instead of crashing
        assert "error" in result
        assert "connect" in result["error"]
    
    @patch('api_client.requests.get')
    def test_general_request_error_handled(self, mock_get):
        """Test that general request errors are handled."""
        import requests
        
        # Mock a general request error
        mock_get.side_effect = requests.exceptions.RequestException("Something went wrong")
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return error info instead of crashing
        assert "error" in result
        assert "Request failed" in result["error"]


class TestImprovedHTTPStatusHandling:
    """Tests for improved HTTP status code handling."""
    
    @patch('api_client.requests.get')
    def test_200_returns_json_data(self, mock_get):
        """Test that successful requests return proper JSON data."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 123, "name": "John"}
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return JSON data directly
        assert result["id"] == 123
        assert result["name"] == "John"
    
    @patch('api_client.requests.get')
    def test_404_returns_helpful_error_message(self, mock_get):
        """Test that 404 errors return helpful error messages."""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return helpful error message
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    @patch('api_client.requests.get')
    def test_401_returns_helpful_error_message(self, mock_get):
        """Test that 401 errors return helpful error messages."""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return helpful error message about authentication
        assert "error" in result
        assert "unauthorized" in result["error"].lower()
        assert "api key" in result["error"].lower()
    
    @patch('api_client.requests.get')
    def test_500_returns_helpful_error_message(self, mock_get):
        """Test that server errors return helpful error messages."""
        # Mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return helpful error message about server issues
        assert "error" in result
        assert "server error" in result["error"].lower()
    
    @patch('api_client.requests.get')
    def test_unknown_status_code_handled(self, mock_get):
        """Test that unknown status codes are handled."""
        # Mock unknown status code
        mock_response = Mock()
        mock_response.status_code = 418  # I'm a teapot
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Should return error with status code information
        assert "error" in result
        assert "418" in result["error"]


class TestImprovedUpdateOperations:
    """Tests for improved update operations."""
    
    @patch('api_client.requests.put')
    def test_successful_update_returns_detailed_result(self, mock_put):
        """Test that successful updates return detailed results."""
        # Mock successful update
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.update_user(123, {"name": "Jane"})
        
        # Should return structured result with success info
        assert result["success"] is True
        assert "message" in result
        assert "updated" in result["message"].lower()
    
    @patch('api_client.requests.put')
    def test_failed_update_returns_error_details(self, mock_put):
        """Test that failed updates return error details."""
        # Mock failed update
        mock_response = Mock()
        mock_response.status_code = 404
        mock_put.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.update_user(123, {"name": "Jane"})
        
        # Should return structured result with error details
        assert result["success"] is False
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    @patch('api_client.requests.put')
    def test_update_network_error_handled_gracefully(self, mock_put):
        """Test that network errors in updates are handled gracefully."""
        import requests
        
        # Mock network error during update
        mock_put.side_effect = requests.exceptions.Timeout("Update timed out")
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.update_user(123, {"name": "Jane"})
        
        # Should return error info instead of crashing
        assert result["success"] is False
        assert "error" in result
        assert "timed out" in result["error"]


class TestImprovedInputValidation:
    """Tests for improved input validation."""
    
    def test_get_user_data_validates_user_id(self):
        """Test that get_user_data validates user_id parameter."""
        client = APIClient("https://api.example.com", "test-key")
        
        # Should reject empty user_id
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            client.get_user_data("")
        
        # Should reject None user_id
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            client.get_user_data(None)
    
    def test_update_user_validates_user_id(self):
        """Test that update_user validates user_id parameter."""
        client = APIClient("https://api.example.com", "test-key")
        
        # Should reject empty user_id
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            client.update_user("", {"name": "Jane"})
        
        # Should reject None user_id
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            client.update_user(None, {"name": "Jane"})
    
    def test_update_user_validates_data_parameter(self):
        """Test that update_user validates data parameter."""
        client = APIClient("https://api.example.com", "test-key")
        
        # Should reject None data
        with pytest.raises(ValueError, match="Data must be a non-empty dictionary"):
            client.update_user(123, None)
        
        # Should reject empty data
        with pytest.raises(ValueError, match="Data must be a non-empty dictionary"):
            client.update_user(123, {})
        
        # Should reject non-dictionary data
        with pytest.raises(ValueError, match="Data must be a non-empty dictionary"):
            client.update_user(123, "not a dict")


class TestImprovedContentHandling:
    """Tests for improved content handling."""
    
    @patch('api_client.requests.put')
    def test_update_sends_proper_json_content_type(self, mock_put):
        """Test that updates send proper JSON content type."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        client.update_user(123, {"name": "Jane"})
        
        # Should have called with proper headers
        mock_put.assert_called_once()
        call_args = mock_put.call_args
        headers = call_args[1]["headers"]
        assert headers["Content-Type"] == "application/json"
    
    @patch('api_client.requests.put')
    def test_update_sends_json_data_properly(self, mock_put):
        """Test that updates send data as JSON properly."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        test_data = {"name": "Jane", "email": "jane@example.com"}
        client.update_user(123, test_data)
        
        # Should have used json parameter instead of data parameter
        mock_put.assert_called_once()
        call_args = mock_put.call_args
        assert "json" in call_args[1]
        assert call_args[1]["json"] == test_data