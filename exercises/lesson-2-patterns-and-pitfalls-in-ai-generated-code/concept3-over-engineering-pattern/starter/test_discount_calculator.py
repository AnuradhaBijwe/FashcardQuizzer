import pytest
from unittest.mock import patch

# Import both versions to compare them
import original_discount_calculator as original
import discount_calculator as ai_modified

class TestOriginalDiscountCalculator:
    """Test the original simple discount calculator"""
    
    def test_original_basic_functionality(self):
        """Test that original simple version works"""
        assert original.calculate_discount(100.0, "premium") == 15.0
        assert original.calculate_discount(100.0, "regular") == 5.0
        assert original.calculate_discount(100.0, "vip") == 25.0
        assert original.calculate_discount(100.0, "student") == 10.0
    
    def test_original_handles_unknown_types(self):
        """Test original handles edge cases simply"""
        # Unknown types default to regular
        assert original.calculate_discount(100.0, "unknown") == 5.0
        assert original.calculate_discount(100.0, "") == 5.0
    
    def test_original_simplicity_metrics(self):
        """Measure the simplicity of original version"""
        with open("original_discount_calculator.py", "r") as f:
            original_code = f.read()
        
        original_lines = len([line for line in original_code.split('\n') if line.strip()])
        class_count = original_code.count("class ")
        
        # Original should be simple
        assert original_lines < 30, f"Original is simple: {original_lines} lines"
        assert class_count == 0, f"Original uses no classes: {class_count}"

class TestAIModifiedDiscountCalculator:
    """Test the AI over-engineered discount calculator"""
    
    def test_ai_version_basic_functionality_works(self):
        """Test that AI version produces correct results despite complexity"""
        # AI version should still work, just with unnecessary complexity
        assert ai_modified.calculate_discount(100.0, "premium") == 15.0
        assert ai_modified.calculate_discount(100.0, "regular") == 5.0
    
    def test_ai_version_over_engineering_metrics(self):
        """Measure the complexity AI introduced"""
        with open("discount_calculator.py", "r") as f:
            ai_code = f.read()
        
        ai_lines = len([line for line in ai_code.split('\n') if line.strip()])
        class_count = ai_code.count("class ")
        
        # AI version should be overly complex
        assert ai_lines > 100, f"AI version is complex: {ai_lines} lines"
        assert class_count >= 5, f"AI version uses many classes: {class_count}"
    
    def test_ai_added_unnecessary_patterns(self):
        """Test that AI added patterns that weren't requested"""
        with open("discount_calculator.py", "r") as f:
            ai_code = f.read()
        
        # Check for over-engineering indicators
        over_engineering_patterns = [
            "Strategy",        # Strategy pattern
            "Factory",         # Factory pattern  
            "Enum",           # Enum for simple strings
            "dataclass",      # Data classes for simple data
            "ABC",            # Abstract base classes
            "cache"           # Caching for simple calculations
        ]
        
        found_patterns = []
        for pattern in over_engineering_patterns:
            if pattern in ai_code:
                found_patterns.append(pattern)
        
        assert len(found_patterns) >= 4, f"AI should introduce multiple unnecessary patterns: {found_patterns}"

class TestOverEngineeringComparison:
    """Tests that directly compare simple original vs complex AI versions"""
    
    def test_both_versions_produce_identical_results(self):
        """Both versions should calculate discounts identically"""
        test_cases = [
            (100.0, "premium"),
            (50.0, "regular"), 
            (200.0, "vip"),
            (75.0, "student"),
            (100.0, "unknown")
        ]
        
        for price, customer_type in test_cases:
            original_result = original.calculate_discount(price, customer_type)
            ai_result = ai_modified.calculate_discount(price, customer_type)
            
            assert original_result == ai_result, \
                f"Results should be identical for {customer_type}: original={original_result}, ai={ai_result}"
    
    def test_complexity_explosion_for_simple_request(self):
        """MAIN TEST: Shows how AI over-engineered a simple request"""
        
        # Compare code complexity
        with open("original_discount_calculator.py", "r") as f:
            original_code = f.read()
        
        with open("discount_calculator.py", "r") as f:
            ai_code = f.read()
        
        original_lines = len([line for line in original_code.split('\n') if line.strip()])
        ai_lines = len([line for line in ai_code.split('\n') if line.strip()])
        
        # AI should have exploded the complexity
        complexity_ratio = ai_lines / original_lines
        assert complexity_ratio > 5, f"AI version {complexity_ratio:.1f}x more complex than needed"
    
    @patch('original_discount_calculator.logger')
    @patch('discount_calculator.logger')  
    def test_logging_requirement_analysis(self, ai_mock_logger, orig_mock_logger):
        """Analyze what the original request was probably about"""
        
        # Original version had no logging
        original.calculate_discount(100.0, "premium")
        orig_mock_logger.info.assert_not_called()
        
        # AI version has logging (the actual requirement)
        ai_modified.calculate_discount(100.0, "premium")
        ai_mock_logger.info.assert_called()
        
        # But AI also added tons of unnecessary complexity beyond just logging