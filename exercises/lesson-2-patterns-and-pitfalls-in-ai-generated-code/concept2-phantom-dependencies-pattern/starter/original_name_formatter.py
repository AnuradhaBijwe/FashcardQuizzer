def format_user_name(first_name: str, last_name: str) -> str:
    """Format user names in a consistent way.
    
    ORIGINAL VERSION - Simple, working function using only built-in Python.
    """
    
    # Handle empty/None inputs
    if not first_name:
        first_name = ""
    if not last_name:
        last_name = ""
    
    # Basic formatting
    first_clean = first_name.strip().title()
    last_clean = last_name.strip().title()
    
    # Format full name
    if first_clean and last_clean:
        return f"{first_clean} {last_clean}"
    elif first_clean:
        return first_clean
    elif last_clean:
        return last_clean
    else:
        return "Unknown User"

def format_names_list(users: list) -> list:
    """Format a list of user names"""
    
    formatted_names = []
    for user in users:
        if isinstance(user, dict):
            formatted_name = format_user_name(
                user.get('first_name', ''),
                user.get('last_name', '')
            )
            formatted_names.append(formatted_name)
    
    return formatted_names

if __name__ == "__main__":
    # Simple usage with built-in functions
    name = format_user_name("john", "doe")
    print(f"Formatted name: {name}")
    
    users = [
        {"first_name": "jane", "last_name": "smith"},
        {"first_name": "bob", "last_name": "johnson"}
    ]
    
    formatted_list = format_names_list(users)
    print(f"Formatted list: {formatted_list}")