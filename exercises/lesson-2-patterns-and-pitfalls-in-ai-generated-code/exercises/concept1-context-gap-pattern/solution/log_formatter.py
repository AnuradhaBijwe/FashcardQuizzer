from datetime import datetime

def format_log_entry(level: str, message: str, user_id: str = None) -> str:
    """Format a log entry with timestamps while preserving all original functionality.
    
    SOLUTION VERSION - Properly integrates timestamp formatting without losing
    the critical functionality that was in the original version.
    """
    
    # Validate log level (PRESERVED from original)
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level.upper() not in valid_levels:
        level = 'INFO'  # Default to INFO for invalid levels
    
    # Add timestamp formatting (NEW feature requested by user)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_entry = f"{timestamp} [{level.upper()}] {message}"
    
    # Add user context if provided (PRESERVED from original)
    if user_id:
        formatted_entry += f" (User: {user_id})"
    
    # Add to system log file for persistence (PRESERVED from original)
    write_to_log_file(formatted_entry)
    
    # Send to monitoring system for alerts (PRESERVED from original)
    send_to_monitoring(level, message, user_id)
    
    # Update log statistics for dashboard (PRESERVED from original)
    update_log_statistics(level)
    
    return formatted_entry

def write_to_log_file(entry: str) -> None:
    """Write log entry to persistent file"""
    print(f"FILE LOG: {entry}")

def send_to_monitoring(level: str, message: str, user_id: str) -> None:
    """Send log to monitoring system for alerts"""
    if level.upper() in ['ERROR', 'CRITICAL']:
        print(f"MONITORING ALERT: {level} - {message} - User: {user_id}")
    else:
        print(f"MONITORING: {level} - {message}")

def update_log_statistics(level: str) -> None:
    """Update log level statistics for dashboard"""
    print(f"STATS: Incremented {level} count")