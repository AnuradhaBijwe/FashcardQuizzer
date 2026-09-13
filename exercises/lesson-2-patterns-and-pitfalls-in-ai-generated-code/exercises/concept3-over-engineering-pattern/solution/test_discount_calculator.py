import pytest
from unittest.mock import patch
from discount_calculator import calculate_discount, calculate_final_price, calculate_bulk_discounts

class TestDiscountCalculator:
    """Test suite for simple, maintainable discount calculation"""
    
    def test_premium_discount_calculation(self):
        """Test premium customer discount"""
        discount = calculate_discount(100.0, "premium")
        assert discount == 15.0  # 15% of 100
    
    def test_regular_discount_calculation(self):
        """Test regular customer discount"""
        discount = calculate_discount(100.0, "regular")
        assert discount == 5.0  # 5% of 100
    
    def test_vip_discount_calculation(self):
        """Test VIP customer discount"""
        discount = calculate_discount(100.0, "vip")
        assert discount == 25.0  # 25% of 100
    
    def test_student_discount_calculation(self):
        """Test student customer discount"""
        discount = calculate_discount(100.0, "student")
        assert discount == 10.0  # 10% of 100
    
    def test_unknown_customer_type_defaults(self):
        """Test unknown customer type gets regular discount"""
        discount = calculate_discount(100.0, "unknown")
        assert discount == 5.0  # Defaults to regular (5%)
    
    def test_final_price_calculation(self):
        """Test complete price calculation with breakdown"""
        result = calculate_final_price(100.0, "premium")
        
        assert result['original_price'] == 100.0
        assert result['discount_amount'] == 15.0
        assert result['final_price'] == 85.0
        assert result['customer_type'] == "premium"
        assert result['discount_rate'] == 0.15
    
    def test_bulk_discount_calculations(self):
        """Test bulk processing functionality"""
        price_customer_pairs = [
            (100.0, "premium"),
            (50.0, "regular"),
            (200.0, "vip")
        ]
        
        results = calculate_bulk_discounts(price_customer_pairs)
        
        assert len(results) == 3
        assert results[0]['discount_amount'] == 15.0  # Premium
        assert results[1]['discount_amount'] == 2.5   # Regular
        assert results[2]['discount_amount'] == 50.0  # VIP
    
    @patch('discount_calculator.logger')
    def test_logging_functionality(self, mock_logger):
        """Test that logging works as requested in original requirement"""
        
        calculate_discount(100.0, "premium")
        
        # Verify logging was called
        assert mock_logger.info.call_count >= 2
        
        # Check log messages contain relevant information
        call_args = [call[0][0] for call in mock_logger.info.call_args_list]
        log_content = " ".join(call_args).lower()
        
        assert "calculating discount" in log_content
        assert "premium" in log_content
        assert "100" in log_content
    
    def test_edge_cases_handled_simply(self):
        """Test edge cases are handled without complex error hierarchies"""
        
        # Zero price
        discount = calculate_discount(0.0, "premium")
        assert discount == 0.0
        
        # Large price
        discount = calculate_discount(10000.0, "regular") 
        assert discount == 500.0  # 5% of 10000
        
        # Edge case customer types
        discount = calculate_discount(100.0, "")
        assert discount == 5.0  # Defaults to regular

class TestSimplicityComparison:
    """Tests that highlight how simple code achieves the same goals"""
    
    def test_equivalent_functionality_simple_vs_complex(self):
        """Demonstrate that simple code produces identical results"""
        
        # Simple implementation (what probably should have been written)
        def simple_discount(price, customer_type):
            rates = {'premium': 0.15, 'regular': 0.05, 'vip': 0.25, 'student': 0.10}
            return price * rates.get(customer_type, 0.05)
        
        # Test cases
        test_cases = [
            (100.0, "premium"),
            (50.0, "regular"), 
            (200.0, "vip"),
            (75.0, "student"),
            (100.0, "unknown")
        ]
        
        for price, customer_type in test_cases:
            simple_result = simple_discount(price, customer_type)
            complex_result = calculate_discount(price, customer_type)
            
            assert simple_result == complex_result, \
                f"Results differ for {customer_type}: simple={simple_result}, complex={complex_result}"
    
    def test_complexity_metrics(self):
        """Show how simple implementation achieves the same functionality"""
        
        # Count lines of code in the simple version
        with open("discount_calculator.py", "r") as f:
            simple_code = f.read()
        
        simple_lines = len([line for line in simple_code.split('\n') if line.strip()])
        
        # The simple version is much more concise 
        assert simple_lines < 50, f"Simple version has {simple_lines} lines (much less than complex 200+ line version)"
        
        # Count number of classes (should be minimal for this simple problem)
        class_count = simple_code.count("class ")
        assert class_count == 0, f"Simple version uses {class_count} classes (vs 9 in complex version)"
    
    def test_original_requirement_analysis(self):
        """Analyze what the original request probably was"""
        
        # The user likely asked: "Add logging to the discount calculation function"
        # But AI created an entire enterprise architecture
        
        # The simple requirement was probably:
        # 1. Calculate discount based on customer type
        # 2. Add logging to see what's happening
        
        # Everything else (enums, strategies, factories, caching, statistics) 
        # was likely unnecessary for the actual business requirement
        
        # Test that the simple approach meets the core requirement
        with patch('discount_calculator.logger') as mock_logger:
            calculate_discount(100.0, "premium")
            
            # Logging requirement met with simple approach
            assert mock_logger.info.called
            
        # Discount calculation requirement met
        assert calculate_discount(100.0, "premium") == 15.0