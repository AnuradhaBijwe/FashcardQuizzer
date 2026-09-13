import pytest
from unittest.mock import patch

# Import both versions to compare them
import original_log_formatter as original
import log_formatter as ai_modified

class TestOriginalLogFormatter:
    """Test the original working log formatter"""
    
    def test_original_basic_functionality(self):
        """Test that original version works correctly"""
        result = original.format_log_entry("INFO", "User logged in")
        
        assert "[INFO]" in result
        assert "User logged in" in result
    
    def test_original_handles_user_context(self):
        """Test original includes user information"""
        result = original.format_log_entry("ERROR", "Failed login", "user123")
        
        assert "[ERROR]" in result
        assert "Failed login" in result  
        assert "(User: user123)" in result
    
    def test_original_validates_log_levels(self):
        """Test original validates and defaults invalid log levels"""
        result = original.format_log_entry("INVALID", "test message")
        
        assert "[INFO]" in result  # Should default to INFO
        assert "test message" in result
    
    @patch('original_log_formatter.write_to_log_file')
    @patch('original_log_formatter.send_to_monitoring')
    @patch('original_log_formatter.update_log_statistics')
    def test_original_complete_workflow(self, mock_stats, mock_monitoring, mock_file):
        """Test that original version includes all workflow steps"""
        result = original.format_log_entry("ERROR", "Database error", "user456")
        
        # Original should call all these functions
        mock_file.assert_called_once()
        mock_monitoring.assert_called_once()
        mock_stats.assert_called_once()

class TestAIModifiedLogFormatter:
    """Test the AI-modified log formatter - reveals context gap"""
    
    def test_ai_version_timestamp_formatting_works(self):
        """Test that AI successfully added timestamp formatting"""
        result = ai_modified.format_log_entry("INFO", "User logged in")
        
        # Should contain timestamp (the requested feature)
        assert "202" in result  # Year should be in timestamp
        assert ":" in result     # Time separator should be present
        assert "[INFO]" in result
        assert "User logged in" in result
    
    def test_ai_version_basic_functionality_preserved(self):
        """Test that basic formatting still works"""
        result = ai_modified.format_log_entry("WARNING", "Low disk space", "admin")
        
        assert "[WARNING]" in result
        assert "Low disk space" in result
        assert "(User: admin)" in result
    
    @patch('log_formatter.write_to_log_file')
    def test_ai_version_missing_file_logging(self, mock_file):
        """CONTEXT GAP: AI removed file logging functionality"""
        ai_modified.format_log_entry("ERROR", "Database error")
        
        # This should be called but won't be - CONTEXT GAP!
        mock_file.assert_not_called()
    
    @patch('log_formatter.send_to_monitoring')
    def test_ai_version_missing_monitoring(self, mock_monitoring):
        """CONTEXT GAP: AI removed monitoring integration"""
        ai_modified.format_log_entry("CRITICAL", "System failure", "user123")
        
        # This should be called but won't be - CONTEXT GAP!
        mock_monitoring.assert_not_called()
    
    @patch('log_formatter.update_log_statistics')
    def test_ai_version_missing_statistics(self, mock_stats):
        """CONTEXT GAP: AI removed statistics tracking"""
        ai_modified.format_log_entry("INFO", "User action")
        
        # This should be called but won't be - CONTEXT GAP!
        mock_stats.assert_not_called()

class TestContextGapComparison:
    """Tests that directly compare original vs AI-modified versions"""
    
    def test_both_versions_format_messages_correctly(self):
        """Both versions should format basic messages"""
        original_result = original.format_log_entry("INFO", "Test message", "user123")
        ai_result = ai_modified.format_log_entry("INFO", "Test message", "user123")
        
        # Both should contain the core information
        assert "[INFO]" in original_result and "[INFO]" in ai_result
        assert "Test message" in original_result and "Test message" in ai_result
        assert "(User: user123)" in original_result and "(User: user123)" in ai_result
    
    def test_only_ai_version_has_timestamps(self):
        """AI version adds timestamps, original doesn't"""
        
        original_result = original.format_log_entry("INFO", "Test message")
        ai_result = ai_modified.format_log_entry("INFO", "Test message")
        
        # Original doesn't have timestamps
        assert "202" not in original_result  # No year
        assert not any(c == ":" for c in original_result[:10])  # No time separators at start
        
        # AI version has timestamps
        assert "202" in ai_result  # Has year
        assert ":" in ai_result[:20]  # Has time separator in timestamp
    
    @patch('original_log_formatter.write_to_log_file')
    @patch('log_formatter.write_to_log_file')
    def test_context_gap_in_file_logging(self, ai_mock_file, orig_mock_file):
        """MAIN TEST: Shows the context gap in file logging"""
        
        # Original version logs to file
        original.format_log_entry("INFO", "Test message")
        orig_mock_file.assert_called_once()
        
        # AI version doesn't log to file - CONTEXT GAP!
        ai_modified.format_log_entry("INFO", "Test message")  
        ai_mock_file.assert_not_called()
    
    @patch('original_log_formatter.send_to_monitoring')
    @patch('log_formatter.send_to_monitoring')
    def test_context_gap_in_monitoring(self, ai_mock_monitor, orig_mock_monitor):
        """MAIN TEST: Shows the context gap in monitoring integration"""
        
        # Original version sends to monitoring  
        original.format_log_entry("ERROR", "Critical issue")
        orig_mock_monitor.assert_called_once()
        
        # AI version doesn't send to monitoring - CONTEXT GAP!
        ai_modified.format_log_entry("ERROR", "Critical issue")
        ai_mock_monitor.assert_not_called()