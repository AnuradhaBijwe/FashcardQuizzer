"""
Code Review Solution 1: Fixed Data Processing Function

Key Issues Fixed:
1. Magic numbers (1.2, 100) -> named constants
2. Poor variable naming ('temp') -> descriptive names  
3. Missing error handling -> basic input validation
4. Hard-coded values -> configurable constants
"""

# Constants - eliminates magic numbers and makes values configurable
MULTIPLIER = 1.2
MAX_VALUE = 100

def process_data(data):
    """
    Process active items by applying multiplier and capping values.
    
    Args:
        data: List of dictionaries with 'status', 'value', and 'id' keys
    
    Returns:
        List of processed items with 'id' and 'processed_value'
    """
    # Basic input validation
    if not isinstance(data, list):
        raise ValueError("Input data must be a list")
    
    result = []
    
    for item in data:
        try:
            # Check required fields exist
            if 'status' not in item or 'value' not in item or 'id' not in item:
                print(f"Warning: Skipping item missing required fields: {item}")
                continue
            
            # Only process active items
            if item['status'] == 'active':
                # Use descriptive variable name instead of 'temp'
                processed_value = item['value'] * MULTIPLIER
                
                # Cap the value at maximum
                if processed_value > MAX_VALUE:
                    processed_value = MAX_VALUE
                
                result.append({
                    'id': item['id'], 
                    'processed_value': processed_value
                })
                
        except (KeyError, TypeError) as e:
            print(f"Warning: Error processing item {item}: {e}")
            continue
    
    return result


# Example usage showing the improvements
if __name__ == "__main__":
    test_data = [
        {'id': 1, 'status': 'active', 'value': 50},
        {'id': 2, 'status': 'inactive', 'value': 75},
        {'id': 3, 'status': 'active', 'value': 120},
        {'id': 4, 'status': 'active'},  # Missing 'value' - will be handled gracefully
    ]
    
    result = process_data(test_data)
    print("Processed results:", result)
    # Output: [{'id': 1, 'processed_value': 60.0}, {'id': 3, 'processed_value': 100}]