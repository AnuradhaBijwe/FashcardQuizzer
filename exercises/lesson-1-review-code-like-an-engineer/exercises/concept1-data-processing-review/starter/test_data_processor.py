"""Tests for data processing function."""

import pytest
from data_processor import process_data


class TestDataProcessorBasic:
    """Tests for basic functionality - these should work."""
    
    def test_processes_active_items(self):
        """Test basic functionality with clean data."""
        test_data = [
            {'id': 1, 'status': 'active', 'value': 50},
            {'id': 2, 'status': 'inactive', 'value': 75},
            {'id': 3, 'status': 'active', 'value': 120},
        ]
        
        result = process_data(test_data)
        
        # Should only process active items
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['processed_value'] == 60.0
        assert result[1]['id'] == 3
        assert result[1]['processed_value'] == 100
    
    def test_empty_list_returns_empty(self):
        """Test with empty input."""
        result = process_data([])
        assert result == []
    
    def test_no_active_items_returns_empty(self):
        """Test when no items are active."""
        test_data = [
            {'id': 1, 'status': 'inactive', 'value': 50},
            {'id': 2, 'status': 'pending', 'value': 75},
        ]
        
        result = process_data(test_data)
        assert result == []


class TestDataProcessorErrorHandling:
    """Tests that should pass but will fail - showing missing error handling."""
    
    def test_missing_required_fields_handled_gracefully(self):
        """This test fails - shows missing error handling."""
        problematic_data = [
            {'id': 1, 'status': 'active', 'value': 50},  # Good item
            {'id': 5, 'status': 'active'},               # Missing 'value' - will crash
            {'id': 6, 'value': 30},                      # Missing 'status' - will crash
        ]
        
        # This should process the good item and skip bad ones, but it will crash instead
        with pytest.raises(KeyError):
            result = process_data(problematic_data)
            # If this didn't crash, we'd expect:
            # assert len(result) == 1
            # assert result[0]['id'] == 1
    
    def test_invalid_input_type_raises_clear_error(self):
        """This test fails - shows missing input validation."""
        # Should validate input type, but it doesn't
        with pytest.raises(TypeError):
            process_data("not a list")  # Will crash with unhelpful error
    
    def test_none_input_raises_clear_error(self):
        """This test fails - shows missing input validation."""
        # Should handle None gracefully, but it doesn't
        with pytest.raises(TypeError):
            process_data(None)  # Will crash


class TestDataProcessorConstants:
    """Tests that show how magic numbers make code hard to test and understand."""
    
    def test_multiplier_constant_makes_tests_hard(self):
        """Magic numbers make tests unclear - what is 1.2?"""
        test_data = [{'id': 1, 'status': 'active', 'value': 10}]
        result = process_data(test_data)
        
        # We have to use the magic number in our test - bad practice
        expected_value = 10 * 1.2  # What is 1.2? Why 1.2?
        assert result[0]['processed_value'] == expected_value
    
    def test_max_value_constant_makes_capping_unclear(self):
        """Magic numbers make the capping logic unclear - what is 100?"""
        test_data = [{'id': 1, 'status': 'active', 'value': 200}]
        result = process_data(test_data)
        
        # We have to use the magic number - unclear why it's 100
        assert result[0]['processed_value'] == 100  # Why 100? Where does this come from?
    
    def test_edge_case_hard_to_test_with_magic_numbers(self):
        """Testing edge cases is hard when values are magic numbers."""
        # What input value results in exactly the max after processing?
        # With magic numbers, this calculation is unclear:
        input_value = 100 / 1.2  # Magic numbers make this confusing
        test_data = [{'id': 1, 'status': 'active', 'value': input_value}]
        result = process_data(test_data)
        
        assert result[0]['processed_value'] == 100


class TestDataProcessorRobustness:
    """Tests for edge cases - some will work, others will fail."""
    
    def test_zero_value_handled(self):
        """Zero values should work fine."""
        test_data = [{'id': 1, 'status': 'active', 'value': 0}]
        result = process_data(test_data)
        
        assert len(result) == 1
        assert result[0]['processed_value'] == 0.0
    
    def test_negative_value_handled(self):
        """Negative values should work (no validation prevents them)."""
        test_data = [{'id': 1, 'status': 'active', 'value': -10}]
        result = process_data(test_data)
        
        assert len(result) == 1
        assert result[0]['processed_value'] == -12.0  # -10 * 1.2
    
    def test_mixed_valid_and_invalid_data(self):
        """This test fails - shows how bad data crashes everything."""
        mixed_data = [
            {'id': 1, 'status': 'active', 'value': 50},     # Valid
            {'id': 2, 'status': 'active'},                  # Missing value - will crash
            {'id': 3, 'status': 'active', 'value': 30},     # Valid
            None,                                            # Invalid item - will crash
            {'id': 4, 'value': 40},                         # Missing status - will crash
        ]
        
        # This will crash on the first bad item, instead of processing the good ones
        with pytest.raises((KeyError, TypeError)):
            result = process_data(mixed_data)
            # If it worked properly, we'd expect:
            # assert len(result) == 2  # Only the 2 valid items
            # assert result[0]['id'] == 1
            # assert result[1]['id'] == 3