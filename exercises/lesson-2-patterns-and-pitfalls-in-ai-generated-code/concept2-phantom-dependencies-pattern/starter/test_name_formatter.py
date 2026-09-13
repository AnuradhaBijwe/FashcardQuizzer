import pytest

# Test original version (should work)
try:
    import original_name_formatter as original
    ORIGINAL_IMPORTS_OK = True
except ImportError as e:
    ORIGINAL_IMPORTS_OK = False
    ORIGINAL_ERROR = str(e)

# Test AI version (should fail due to phantom dependencies)
try:
    import name_formatter as ai_modified
    AI_IMPORTS_OK = True  
except ImportError as e:
    AI_IMPORTS_OK = False
    AI_ERROR = str(e)

class TestOriginalNameFormatter:
    """Test the original working name formatter"""
    
    def test_original_imports_successfully(self):
        """Original version should import without issues"""
        assert ORIGINAL_IMPORTS_OK, f"Original failed: {ORIGINAL_ERROR if not ORIGINAL_IMPORTS_OK else 'N/A'}"
    
    @pytest.mark.skipif(not ORIGINAL_IMPORTS_OK, reason="Original import failed")
    def test_original_name_formatting_works(self):
        """Original version should format names correctly"""
        result = original.format_user_name("john", "doe")
        assert result == "John Doe"
        
        result = original.format_user_name("", "smith")
        assert result == "Smith"
        
        result = original.format_user_name("jane", "")
        assert result == "Jane"
    
    @pytest.mark.skipif(not ORIGINAL_IMPORTS_OK, reason="Original import failed")
    def test_original_list_formatting_works(self):
        """Original version should format name lists correctly"""
        users = [
            {"first_name": "alice", "last_name": "jones"},
            {"first_name": "bob", "last_name": "wilson"}
        ]
        
        result = original.format_names_list(users)
        assert result == ["Alice Jones", "Bob Wilson"]

class TestAIModifiedNameFormatter:
    """Test the AI-modified name formatter - reveals phantom dependencies"""
    
    def test_ai_version_import_fails(self):
        """PHANTOM DEPENDENCIES: AI version should fail to import"""
        assert not AI_IMPORTS_OK, "AI version should fail due to phantom dependencies"
        
        # Check that error mentions phantom libraries
        if not AI_IMPORTS_OK:
            phantom_names = [
                "name_formatter_pro",
                "string_utils_plus", 
                "text_optimizer"
            ]
            
            error_mentions_phantom = any(phantom in AI_ERROR for phantom in phantom_names)
            assert error_mentions_phantom, f"Error should mention phantoms: {AI_ERROR}"
    
    def test_phantom_library_patterns(self):
        """Identify phantom library naming patterns"""
        
        with open("name_formatter.py", "r") as f:
            ai_code = f.read()
        
        # Check for phantom libraries with suspicious naming
        phantom_indicators = [
            "name_formatter_pro",    # "pro" suffix
            "string_utils_plus",     # "plus" suffix
            "text_optimizer"         # sounds too comprehensive
        ]
        
        found_phantoms = 0
        for phantom in phantom_indicators:
            if phantom in ai_code:
                found_phantoms += 1
        
        assert found_phantoms >= 2, f"Should find phantom libraries in source code"
    
    def test_phantom_class_names(self):
        """Check for phantom classes that sound too convenient"""
        
        with open("name_formatter.py", "r") as f:
            ai_code = f.read()
        
        # Classes that sound suspiciously perfect
        phantom_classes = [
            "AdvancedNameProcessor",  # "Advanced" prefix
            "SmartCapitalizer",       # "Smart" prefix  
            "FastStringCleaner"       # "Fast" prefix
        ]
        
        found_classes = 0
        for phantom_class in phantom_classes:
            if phantom_class in ai_code:
                found_classes += 1
        
        assert found_classes >= 2, f"Should find phantom classes in source"
    
    def test_deprecated_import_usage(self):
        """Check for deprecated import patterns"""
        
        with open("name_formatter.py", "r") as f:
            ai_code = f.read()
        
        # Should contain deprecated String import (capital S)
        assert "import String" in ai_code, "Should contain deprecated String import"

class TestPhantomDependencyComparison:
    """Compare original (working) vs AI (phantom) versions"""
    
    def test_original_works_ai_fails(self):
        """Original uses real libraries, AI uses phantom ones"""
        
        assert ORIGINAL_IMPORTS_OK, "Original should work with built-in functions"
        assert not AI_IMPORTS_OK, "AI should fail with phantom dependencies"
    
    def test_what_ai_replaced_with_phantoms(self):
        """Show how AI replaced simple built-ins with phantom libraries"""
        
        with open("original_name_formatter.py", "r") as f:
            original_code = f.read()
        
        with open("name_formatter.py", "r") as f:
            ai_code = f.read()
        
        # Original should use simple built-in string methods
        assert ".strip()" in original_code, "Original should use built-in strip()"
        assert ".title()" in original_code, "Original should use built-in title()"
        
        # AI should have replaced these with phantom "advanced" versions
        assert "super_clean" in ai_code, "AI should use phantom super_clean method"
        assert "smart_title_case" in ai_code, "AI should use phantom smart_title_case method"