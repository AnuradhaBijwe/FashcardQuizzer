"""
CLI Interface Module - Version 1

Displays reports in terminal with formatting and color.
This version works but has areas for improvement.
"""


class CLIInterface:
    """Terminal interface for displaying expense reports."""
    
    def display_report(self, report_data):
        """Display formatted report to terminal."""
        mode = report_data.get('mode', 'unknown')
        
        if mode == 'summary':
            print("\n" + "=" * 50)
            print("  EXPENSE SUMMARY BY CATEGORY")
            print("=" * 50)
            
            data = report_data.get('data', {})
            for category, amount in sorted(data.items()):
                print(f"  {category:20s} ${amount:>10.2f}")
            
            print("-" * 50)
            total = report_data.get('total', 0.0)
            print(f"  {'TOTAL':20s} ${total:>10.2f}")
            print("=" * 50 + "\n")
            
        elif mode == 'monthly':
            print("\n" + "=" * 50)
            print("  MONTHLY EXPENSE TOTALS")
            print("=" * 50)
            
            data = report_data.get('data', {})
            for month, amount in sorted(data.items()):
                print(f"  {month:20s} ${amount:>10.2f}")
            
            print("-" * 50)
            total = report_data.get('total', 0.0)
            print(f"  {'TOTAL':20s} ${total:>10.2f}")
            print("=" * 50 + "\n")
        else:
            print(f"\nError: Unknown report mode '{mode}'\n")
    
    def display_error(self, error):
        """Display error message to terminal."""
        error_str = str(error)
        
        if 'file' in error_str.lower() or 'not found' in error_str.lower():
            print("\n" + "!" * 50)
            print("  ERROR: File Not Found")
            print("  " + error_str)
            print("!" * 50 + "\n")
        elif 'invalid' in error_str.lower() or 'value' in error_str.lower():
            print("\n" + "!" * 50)
            print("  ERROR: Invalid Data")
            print("  " + error_str)
            print("!" * 50 + "\n")
        else:
            print("\n" + "!" * 50)
            print("  ERROR")
            print("  " + error_str)
            print("!" * 50 + "\n")
