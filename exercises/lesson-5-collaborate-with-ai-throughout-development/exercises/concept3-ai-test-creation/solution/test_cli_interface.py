"""
Tests for CLIInterface - must pass for both v1 and v2.
These tests define the contract that refactoring must maintain.
"""
import pytest
from io import StringIO
import sys


def get_cli_interface():
    """Get the CLI interface class (v1 or v2)."""
    try:
        from cli_interface_v2 import CLIInterface
        return CLIInterface
    except ImportError:
        from cli_interface_v1 import CLIInterface
        return CLIInterface


@pytest.fixture
def cli():
    """Create CLI interface instance."""
    CLIInterface = get_cli_interface()
    return CLIInterface()


@pytest.fixture
def capture_output():
    """Capture stdout for testing."""
    class OutputCapture:
        def __enter__(self):
            self.output = StringIO()
            self._old_stdout = sys.stdout
            sys.stdout = self.output
            return self
        
        def __exit__(self, *args):
            sys.stdout = self._old_stdout
        
        def get_output(self):
            return self.output.getvalue()
    
    return OutputCapture()


class TestDisplayReport:
    """Test report display functionality."""
    
    def test_displays_summary_report(self, cli, capture_output):
        """Should display summary report correctly."""
        report_data = {
            'mode': 'summary',
            'data': {'Food': 150.50, 'Transport': 200.00},
            'total': 350.50
        }
        
        with capture_output as out:
            cli.display_report(report_data)
        
        output = out.get_output()
        assert 'SUMMARY' in output.upper()
        assert 'Food' in output
        assert '150.50' in output
        assert '350.50' in output
    
    def test_displays_monthly_report(self, cli, capture_output):
        """Should display monthly report correctly."""
        report_data = {
            'mode': 'monthly',
            'data': {'2024-01': 500.00, '2024-02': 450.00},
            'total': 950.00
        }
        
        with capture_output as out:
            cli.display_report(report_data)
        
        output = out.get_output()
        assert 'MONTHLY' in output.upper()
        assert '2024-01' in output
        assert '500.00' in output
    
    def test_displays_total(self, cli, capture_output):
        """Should display total in all reports."""
        report_data = {
            'mode': 'summary',
            'data': {'Food': 100.00},
            'total': 100.00
        }
        
        with capture_output as out:
            cli.display_report(report_data)
        
        output = out.get_output()
        assert 'TOTAL' in output.upper()
        assert '100.00' in output


class TestDisplayError:
    """Test error display functionality."""
    
    def test_displays_file_not_found_error(self, cli, capture_output):
        """Should display file not found errors."""
        error = FileNotFoundError("File 'expenses.csv' not found")
        
        with capture_output as out:
            cli.display_error(error)
        
        output = out.get_output()
        assert 'ERROR' in output.upper()
        assert 'expenses.csv' in output
    
    def test_displays_value_error(self, cli, capture_output):
        """Should display value errors."""
        error = ValueError("Invalid amount format")
        
        with capture_output as out:
            cli.display_error(error)
        
        output = out.get_output()
        assert 'ERROR' in output.upper()
        assert 'Invalid' in output
    
    def test_displays_generic_error(self, cli, capture_output):
        """Should display generic errors."""
        error = Exception("Something went wrong")
        
        with capture_output as out:
            cli.display_error(error)
        
        output = out.get_output()
        assert 'ERROR' in output.upper()
        assert 'Something went wrong' in output
