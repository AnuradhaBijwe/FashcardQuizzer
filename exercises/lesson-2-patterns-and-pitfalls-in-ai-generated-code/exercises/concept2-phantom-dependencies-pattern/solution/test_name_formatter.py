import pytest

from name_formatter import format_user_name, format_names_list, validate_name_format, format_apostrophes

class TestNameFormatterSolution:
    """Test suite for name formatter using real dependencies only"""
    
    def test_basic_name_formatting(self):
        """Test basic name formatting works correctly"""
        assert format_user_name("john", "doe") == "John Doe"
        assert format_user_name("jane", "smith") == "Jane Smith"
        assert format_user_name("", "wilson") == "Wilson"
        assert format_user_name("alice", "") == "Alice"
        assert format_user_name("", "") == "Unknown User"
    
    def test_apostrophe_handling(self):
        """Test apostrophe handling using real string operations"""
        result = format_apostrophes("o'connor")
        assert result == "O'Connor"
        
        result = format_apostrophes("d'angelo")  
        assert result == "D'Angelo"
        
        # Test without apostrophes
        result = format_apostrophes("smith")
        assert result == "smith"
    
    def test_list_formatting(self):
        """Test list formatting functionality"""
        users = [
            {"first_name": "alice", "last_name": "jones"},
            {"first_name": "bob", "last_name": "o'connor"},
            {"first_name": "", "last_name": "smith"},
            "invalid_entry"  # Should be skipped gracefully
        ]
        
        result = format_names_list(users)
        expected = ["Alice Jones", "Bob O'Connor", "Smith"]
        assert result == expected
    
    def test_name_validation(self):
        """Test name validation using real string operations"""
        assert validate_name_format("John Doe") == True
        assert validate_name_format("Mary O'Connor") == True
        assert validate_name_format("Jean-Luc") == True
        assert validate_name_format("") == False
        assert validate_name_format("123Invalid") == False
        assert validate_name_format(None) == False
    
    def test_uses_only_real_libraries(self):
        """Verify solution uses only real Python capabilities"""
        
        with open("name_formatter.py", "r") as f:
            solution_code = f.read()
        
        # Should use real standard library
        assert "import string" in solution_code, "Should use real string module"
        assert "from typing import" in solution_code, "Should use real typing module"
        
        # Should NOT contain any phantom libraries
        phantom_libraries = [
            "name_formatter_pro",
            "string_utils_plus", 
            "text_optimizer"
        ]
        
        for phantom in phantom_libraries:
            assert phantom not in solution_code, f"Should not use phantom: {phantom}"
    
    def test_no_phantom_methods_used(self):
        """Verify solution doesn't use phantom methods"""
        
        with open("name_formatter.py", "r") as f:
            solution_code = f.read()
        
        # Should use real string methods
        real_methods = [".strip()", ".title()", ".capitalize()"]
        methods_found = sum(1 for method in real_methods if method in solution_code)
        assert methods_found >= 1, "Should use real string methods"
        
        # Should NOT use phantom methods
        phantom_methods = ["super_clean", "smart_title_case", "process_batch"]
        for phantom_method in phantom_methods:
            assert phantom_method not in solution_code, f"Should not use phantom method: {phantom_method}"