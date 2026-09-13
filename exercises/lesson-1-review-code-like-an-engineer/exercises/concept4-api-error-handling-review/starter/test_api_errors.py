"""Tests for basic API error handling issues."""

import pytest
from unittest.mock import patch, Mock
from api_client import APIClient


class TestBasicAPIOperations:
    """Tests for basic API functionality."""
    
    def test_api_client_initialization(self):
        """Test that API client can be initialized."""
        client = APIClient("https://api.example.com", "test-key")
        assert client.base_url == "https://api.example.com"
        assert client.api_key == "test-key"
    
    @patch('api_client.requests.get')
    def test_successful_request_works(self, mock_get):
        """Test that successful requests work."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"id": 123, "name": "John"}'
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        assert result is not None
        assert result["id"] == 123


class TestNetworkErrorHandling:
    """Tests that show network error handling problems."""
    
    @patch('api_client.requests.get')
    def test_network_timeout_crashes_program(self, mock_get):
        """Test that network timeouts are not handled."""
        import requests
        
        # Mock a timeout error
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        client = APIClient("https://api.example.com", "test-key")
        
        # This should crash due to unhandled timeout
        with pytest.raises(requests.exceptions.Timeout):
            client.get_user_data(123)
    
    @patch('api_client.requests.get')
    def test_connection_error_crashes_program(self, mock_get):
        """Test that connection errors are not handled."""
        import requests
        
        # Mock a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        
        client = APIClient("https://api.example.com", "test-key")
        
        # This should crash due to unhandled connection error
        with pytest.raises(requests.exceptions.ConnectionError):
            client.get_user_data(123)


class TestHTTPStatusHandling:
    """Tests that show HTTP status code handling problems."""
    
    @patch('api_client.requests.get')
    def test_404_returns_none_without_info(self, mock_get):
        """Test that 404 errors provide no useful information."""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Problem: Returns None without explaining why
        assert result is None
    
    @patch('api_client.requests.get')
    def test_401_returns_none_without_info(self, mock_get):
        """Test that 401 errors provide no useful information."""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Problem: Returns None without explaining authentication failed
        assert result is None
    
    @patch('api_client.requests.get')
    def test_500_returns_none_without_info(self, mock_get):
        """Test that server errors provide no useful information."""
        # Mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.get_user_data(123)
        
        # Problem: Returns None without explaining server error
        assert result is None


class TestUpdateOperationProblems:
    """Tests that show problems with update operations."""
    
    @patch('api_client.requests.put')
    def test_update_returns_only_boolean(self, mock_put):
        """Test that update only returns True/False without details."""
        # Mock successful update
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.update_user(123, {"name": "Jane"})
        
        # Problem: Only returns boolean, no details about what happened
        assert result is True
    
    @patch('api_client.requests.put')
    def test_update_failure_gives_no_info(self, mock_put):
        """Test that failed updates provide no error information."""
        # Mock failed update
        mock_response = Mock()
        mock_response.status_code = 400
        mock_put.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        result = client.update_user(123, {"name": "Jane"})
        
        # Problem: Returns False but no info about why it failed
        assert result is False
    
    @patch('api_client.requests.put')
    def test_update_network_error_crashes_program(self, mock_put):
        """Test that network errors in updates are not handled."""
        import requests
        
        # Mock network error during update
        mock_put.side_effect = requests.exceptions.Timeout("Update timed out")
        
        client = APIClient("https://api.example.com", "test-key")
        
        # This should crash due to unhandled timeout in update
        with pytest.raises(requests.exceptions.Timeout):
            client.update_user(123, {"name": "Jane"})


class TestInputValidationProblems:
    """Tests that show missing input validation."""
    
    def test_no_validation_for_empty_base_url(self):
        """Test that empty base URL is not validated."""
        # Should validate but doesn't
        client = APIClient("", "test-key")
        # Will cause issues when making requests
        assert client.base_url == ""
    
    def test_no_validation_for_empty_api_key(self):
        """Test that empty API key is not validated."""
        # Should validate but doesn't
        client = APIClient("https://api.example.com", "")
        # Will cause authorization issues
        assert client.api_key == ""
    
    @patch('api_client.requests.get')
    def test_no_validation_for_empty_user_id(self, mock_get):
        """Test that empty user ID is not validated."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{}'
        mock_get.return_value = mock_response
        
        client = APIClient("https://api.example.com", "test-key")
        
        # Should validate user_id but doesn't
        result = client.get_user_data("")  # Empty user ID
        # This will make a malformed request
        assert mock_get.called