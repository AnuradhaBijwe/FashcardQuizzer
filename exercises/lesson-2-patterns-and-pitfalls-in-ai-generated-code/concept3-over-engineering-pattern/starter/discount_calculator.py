import logging

logger = logging.getLogger(__name__)

def calculate_discount(price: float, customer_type: str) -> float:
    """Calculate discount based on customer type.

    Args:
        price: The base price to calculate discount from
        customer_type: Type of customer ('premium', 'vip', 'student', 'regular')

    Returns:
        The discount amount

    Raises:
        ValueError: If customer_type is not recognized or price is negative
    """
    if price < 0:
        raise ValueError("Price cannot be negative")

    # Normalize customer type to lowercase for comparison
    customer_type = customer_type.lower()

    # Define discount rates
    discount_rates = {
        'premium': 0.15,
        'vip': 0.25,
        'student': 0.10,
        'regular': 0.05
    }

    # Validate customer type
    if customer_type not in discount_rates:
        logger.error(f"Invalid customer type: {customer_type}")
        raise ValueError(f"Invalid customer type: {customer_type}. "
                       f"Must be one of: {', '.join(discount_rates.keys())}")

    # Calculate discount
    discount_rate = discount_rates[customer_type]
    discount = price * discount_rate

    logger.info(f"Calculated {customer_type} discount: ${discount:.2f} "
               f"({discount_rate*100}% of ${price:.2f})")

    return discount


if __name__ == "__main__":
    # Configure logging for demo
    logging.basicConfig(level=logging.INFO,
                       format='%(levelname)s: %(message)s')

    # Usage examples
    print(f"Premium discount on $100: ${calculate_discount(100.0, 'premium'):.2f}")
    print(f"VIP discount on $100: ${calculate_discount(100.0, 'vip'):.2f}")
    print(f"Student discount on $100: ${calculate_discount(100.0, 'student'):.2f}")
    print(f"Regular discount on $100: ${calculate_discount(100.0, 'regular'):.2f}")

    # Test error handling
    try:
        calculate_discount(100.0, 'invalid')
    except ValueError as e:
        print(f"\nError handling demo: {e}")