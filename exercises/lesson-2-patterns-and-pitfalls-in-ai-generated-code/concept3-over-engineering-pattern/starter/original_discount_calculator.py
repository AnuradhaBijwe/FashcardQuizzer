import logging

logger = logging.getLogger(__name__)

def calculate_discount(price: float, customer_type: str) -> float:
    """Calculate discount based on customer type.
    
    ORIGINAL VERSION - Simple, working discount calculation.
    This was the working code before AI was asked to "add logging".
    """
    
    # Simple discount logic
    if customer_type == 'premium':
        discount = price * 0.15
    elif customer_type == 'vip':
        discount = price * 0.25
    elif customer_type == 'student':
        discount = price * 0.10
    else:
        discount = price * 0.05  # regular customer
    
    return discount

# Simple usage example
if __name__ == "__main__":
    # This simple function worked perfectly for business needs
    premium_discount = calculate_discount(100.0, "premium")
    regular_discount = calculate_discount(100.0, "regular")
    
    print(f"Premium customer discount: ${premium_discount}")
    print(f"Regular customer discount: ${regular_discount}")