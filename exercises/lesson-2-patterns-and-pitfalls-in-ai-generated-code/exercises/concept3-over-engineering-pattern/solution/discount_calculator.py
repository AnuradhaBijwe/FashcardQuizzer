import logging

logger = logging.getLogger(__name__)

def calculate_discount(price: float, customer_type: str) -> float:
    """Calculate discount based on customer type with logging.
    
    Simple, direct implementation that meets the original requirements
    without unnecessary complexity.
    """
    
    logger.info(f"Calculating discount for {customer_type}, price: ${price}")
    
    # Simple discount logic - no need for strategy pattern
    discount_rates = {
        'premium': 0.15,
        'regular': 0.05,
        'vip': 0.25,
        'student': 0.10
    }
    
    # Get discount rate, defaulting to regular customer rate
    rate = discount_rates.get(customer_type, 0.05)
    discount = price * rate
    
    logger.info(f"Discount calculated: ${discount:.2f} ({rate*100}% rate)")
    
    return discount

def calculate_final_price(price: float, customer_type: str) -> dict:
    """Calculate final price after discount with detailed breakdown."""
    
    discount = calculate_discount(price, customer_type)
    final_price = price - discount
    
    return {
        'original_price': price,
        'discount_amount': discount,
        'final_price': final_price,
        'customer_type': customer_type,
        'discount_rate': discount / price if price > 0 else 0
    }

# If you need multiple discount calculations, you can batch them simply:
def calculate_bulk_discounts(price_customer_pairs: list) -> list:
    """Calculate discounts for multiple customers efficiently."""
    
    results = []
    for price, customer_type in price_customer_pairs:
        result = calculate_final_price(price, customer_type)
        results.append(result)
    
    logger.info(f"Processed bulk discount calculations for {len(results)} customers")
    return results