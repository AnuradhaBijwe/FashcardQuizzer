"""Tests for data processing function."""

import pytest
from data_processor import process_data, MULTIPLIER, MAX_VALUE


class TestDataProcessorBasic:
    """Tests for basic functionality."""
    
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
        assert result[0]['processed_value'] == 50 * MULTIPLIER  # Now using constants
        assert result[1]['id'] == 3
        assert result[1]['processed_value'] == MAX_VALUE  # Capped at max value
    
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
    """Tests that show improved error handling."""
    
    def test_missing_required_fields_handled_gracefully(self):
        """Missing fields are now handled gracefully."""
        problematic_data = [
            {'id': 1, 'status': 'active', 'value': 50},  # Good item
            {'id': 5, 'status': 'active'},               # Missing 'value'
            {'id': 6, 'value': 30},                      # Missing 'status'
        ]
        
        # Should process the good item and skip the bad ones
        result = process_data(problematic_data)
        assert len(result) == 1
        assert result[0]['id'] == 1
    
    def test_invalid_input_type_raises_clear_error(self):
        """Non-list input now raises a clear error."""
        with pytest.raises(ValueError, match="Input data must be a list"):
            process_data("not a list")
    
    def test_none_input_raises_clear_error(self):
        """None input raises a clear error."""
        with pytest.raises(ValueError, match="Input data must be a list"):
            process_data(None)


class TestDataProcessorConstants:
    """Tests that show how constants improve testability."""
    
    def test_multiplier_constant_makes_tests_clear(self):
        """Using constants makes tests more readable and maintainable."""
        test_data = [{'id': 1, 'status': 'active', 'value': 10}]
        result = process_data(test_data)
        
        # Now we can use the named constant in our test
        expected_value = 10 * MULTIPLIER
        assert result[0]['processed_value'] == expected_value
    
    def test_max_value_constant_makes_capping_testable(self):
        """Using constants makes the capping logic testable."""
        test_data = [{'id': 1, 'status': 'active', 'value': 200}]
        result = process_data(test_data)
        
        # Clear test using the named constant
        assert result[0]['processed_value'] == MAX_VALUE
    
    def test_edge_case_exactly_at_max_after_processing(self):
        """Test edge case where processed value equals max value."""
        # Calculate input that will result in exactly MAX_VALUE after processing
        input_value = MAX_VALUE / MULTIPLIER
        test_data = [{'id': 1, 'status': 'active', 'value': input_value}]
        result = process_data(test_data)
        
        assert result[0]['processed_value'] == MAX_VALUE


class TestDataProcessorRobustness:
    """Tests for robustness and edge cases."""
    
    def test_zero_value_handled(self):
        """Zero values are handled correctly."""
        test_data = [{'id': 1, 'status': 'active', 'value': 0}]
        result = process_data(test_data)
        
        assert len(result) == 1
        assert result[0]['processed_value'] == 0.0
    
    def test_negative_value_handled(self):
        """Negative values are handled correctly."""
        test_data = [{'id': 1, 'status': 'active', 'value': -10}]
        result = process_data(test_data)
        
        assert len(result) == 1
        assert result[0]['processed_value'] == -10 * MULTIPLIER
    
    def test_mixed_valid_and_invalid_data(self):
        """Mix of valid and invalid data is handled correctly."""
        mixed_data = [
            {'id': 1, 'status': 'active', 'value': 50},     # Valid
            {'id': 2, 'status': 'active'},                  # Missing value
            {'id': 3, 'status': 'active', 'value': 30},     # Valid
            None,                                            # Invalid item
            {'id': 4, 'value': 40},                         # Missing status
        ]
        
        result = process_data(mixed_data)
        
        # Should only process the 2 valid items
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['id'] == 3