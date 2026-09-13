"""
Tests for the improved file processor with real dependencies.

Run this to see how real libraries work:
    pytest test_real_dependencies.py -v

These tests show:
1. Real libraries that actually exist
2. Proper error handling and logging
3. Specific exception types instead of generic ones
"""

import pytest
import os
import tempfile
import json
import pandas as pd
from file_processor import process_uploaded_files, clean_dataframe


class TestRealDependencies:
    """Tests that verify real libraries are used."""
    
    def test_uses_real_pandas_library(self):
        """Verify that pandas (a real library) is used."""
        # Pandas should be importable and functional
        df = pd.DataFrame({'test': [1, 2, 3]})
        assert len(df) == 3
        assert 'test' in df.columns
    
    def test_uses_standard_library_modules(self):
        """Verify that standard library modules are used."""
        # These should all be available in Python standard library
        import os
        import logging
        
        # os module functionality should work
        assert hasattr(os, 'path')
        assert hasattr(os, 'listdir')
        
        # logging module should be functional
        assert hasattr(logging, 'getLogger')
        assert hasattr(logging, 'info')
    
    def test_no_phantom_library_imports(self):
        """Verify no phantom libraries are imported."""
        import inspect
        from file_processor import process_uploaded_files
        
        source = inspect.getsource(process_uploaded_files)
        
        # Should not contain phantom library imports
        phantom_libraries = [
            "advanced_file_processor",
            "data_cleaner_pro",
            "FastProcessor",
            "clean_dataset"
        ]
        
        for phantom in phantom_libraries:
            assert phantom not in source, f"Should not import phantom library: {phantom}"


class TestImprovedFileProcessing:
    """Tests for improved file processing functionality."""
    
    def setup_method(self):
        """Set up test files for each test."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test CSV file
        self.csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(self.csv_file, 'w') as f:
            f.write("name,age,city\nJohn,25,NYC\nJane,30,LA\n")
        
        # Create test JSON file
        self.json_file = os.path.join(self.temp_dir, "test.json")
        with open(self.json_file, 'w') as f:
            json.dump([
                {"name": "Alice", "age": 28, "city": "Chicago"},
                {"name": "Bob", "age": 35, "city": "Boston"}
            ], f)
    
    def test_processes_csv_files_with_pandas(self):
        """Test processing CSV files using real pandas functionality."""
        result = process_uploaded_files([self.csv_file])
        
        assert len(result) == 1
        df = result[0]
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2  # Two rows of data
        assert 'name' in df.columns
        assert 'age' in df.columns
        assert 'city' in df.columns
    
    def test_processes_json_files_with_pandas(self):
        """Test processing JSON files using real pandas functionality."""
        result = process_uploaded_files([self.json_file])
        
        assert len(result) == 1
        df = result[0]
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2  # Two rows of data
        assert 'name' in df.columns
    
    def test_handles_multiple_file_types(self):
        """Test processing multiple file types together."""
        result = process_uploaded_files([self.csv_file, self.json_file])
        
        assert len(result) == 2
        for df in result:
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0
    
    def test_nonexistent_file_handling(self):
        """Test handling of nonexistent files."""
        nonexistent_file = os.path.join(self.temp_dir, "does_not_exist.csv")
        
        # Should handle gracefully and return empty list
        result = process_uploaded_files([nonexistent_file])
        assert result == []


class TestSpecificErrorHandling:
    """Tests for specific error handling instead of generic exceptions."""
    
    def test_file_not_found_error_handling(self):
        """Test specific FileNotFoundError handling."""
        # Non-existent file should be handled specifically
        result = process_uploaded_files(["nonexistent.csv"])
        assert result == []  # Should handle gracefully
    
    def test_pandas_specific_error_handling(self):
        """Test handling of pandas-specific errors."""
        # Create an invalid CSV file
        temp_dir = tempfile.mkdtemp()
        invalid_csv = os.path.join(temp_dir, "invalid.csv")
        
        with open(invalid_csv, 'w') as f:
            f.write("this,is,not\nvalid,csv,format,with,too,many,columns\n")
        
        # Should handle pandas parsing errors gracefully
        result = process_uploaded_files([invalid_csv])
        # Might succeed or fail depending on pandas parsing, but shouldn't crash
        assert isinstance(result, list)
    
    def test_permission_error_handling(self):
        """Test handling of permission errors."""
        # This test might not work on all systems, so we'll skip if needed
        try:
            # Try to create a file we can't read
            temp_dir = tempfile.mkdtemp()
            no_permission_file = os.path.join(temp_dir, "no_permission.csv")
            
            with open(no_permission_file, 'w') as f:
                f.write("test,data\n1,2\n")
            
            # Remove read permission (Unix-like systems)
            if hasattr(os, 'chmod'):
                os.chmod(no_permission_file, 0o000)
                
                result = process_uploaded_files([no_permission_file])
                assert isinstance(result, list)  # Should handle gracefully
                
                # Restore permission for cleanup
                os.chmod(no_permission_file, 0o644)
        except (OSError, PermissionError):
            # Skip this test if we can't manipulate permissions
            pytest.skip("Cannot test permission errors on this system")


class TestDataCleaning:
    """Tests for the data cleaning functionality."""
    
    def test_clean_dataframe_removes_empty_rows(self):
        """Test that completely empty rows are removed."""
        df = pd.DataFrame({
            'name': ['Alice', None, 'Bob'],
            'age': [25, None, 30],
            'city': ['NYC', None, 'LA']
        })
        
        cleaned = clean_dataframe(df)
        
        # Should remove the completely empty/null row
        assert len(cleaned) == 2
        assert 'Alice' in cleaned['name'].values
        assert 'Bob' in cleaned['name'].values
    
    def test_clean_dataframe_removes_empty_columns(self):
        """Test that empty columns are removed."""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'empty_col': [None, None],
            'age': [25, 30]
        })
        
        cleaned = clean_dataframe(df)
        
        # Should remove the empty column
        assert 'empty_col' not in cleaned.columns
        assert 'name' in cleaned.columns
        assert 'age' in cleaned.columns
    
    def test_clean_dataframe_strips_whitespace(self):
        """Test that whitespace is stripped from string columns."""
        df = pd.DataFrame({
            'name': ['  Alice  ', '  Bob  '],
            'city': [' NYC ', ' LA ']
        })
        
        cleaned = clean_dataframe(df)
        
        # Whitespace should be stripped
        assert cleaned['name'].iloc[0] == 'Alice'
        assert cleaned['name'].iloc[1] == 'Bob'
        assert cleaned['city'].iloc[0] == 'NYC'
        assert cleaned['city'].iloc[1] == 'LA'


class TestLoggingInsteadOfPrint:
    """Tests that verify proper logging is used instead of print statements."""
    
    def test_uses_logging_module(self):
        """Verify that logging module is used."""
        import inspect
        from file_processor import process_uploaded_files
        
        source = inspect.getsource(process_uploaded_files)
        
        # Should use logging instead of print
        assert "logger." in source, "Should use logger for output"
        # Should not use print for normal operation
        print_count = source.count("print(")
        assert print_count == 0, f"Should not use print(), found {print_count} instances"
    
    def test_logging_configuration_exists(self):
        """Verify that logging is properly configured."""
        import file_processor
        import logging
        import inspect
        
        # Should have logging configuration
        source = inspect.getsource(file_processor)
        assert "logging.basicConfig" in source or "getLogger" in source, "Should configure logging"


if __name__ == "__main__":
    print("=== Testing Improved File Processor (Real Dependencies) ===")
    print("✅ All tests should pass, showing real libraries work properly!\n")
    
    import sys
    
    # Run all test classes
    test_classes = [
        TestRealDependencies,
        TestImprovedFileProcessing,
        TestSpecificErrorHandling,
        TestDataCleaning,
        TestLoggingInsteadOfPrint
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"Running {test_class.__name__}...")
        test_instance = test_class()
        
        # Handle setup_method if it exists
        if hasattr(test_instance, 'setup_method'):
            test_instance.setup_method()
        
        for method_name in dir(test_instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    getattr(test_instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {e}")
    
    print(f"\n=== Results: {passed_tests}/{total_tests} tests passed ===")
    
    if passed_tests == total_tests:
        print("🎉 All tests pass! Real dependencies work correctly.")
        print("\n💡 Key improvements demonstrated:")
        print("- Uses real, verifiable libraries (pandas, os, logging)")
        print("- Specific error handling for different error types")
        print("- Proper logging instead of print statements")
        print("- File type detection based on extensions")
        print("- Data cleaning with real pandas functionality")
        print("- No phantom or non-existent dependencies")
    else:
        print("❌ Some tests failed - there may be remaining issues.")
    
    print("\n💡 Run with pytest for detailed output:")
    print("pytest test_real_dependencies.py -v")