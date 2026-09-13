"""
Meta-tests to validate the quality of the generated test suite.

This checks that students created comprehensive, well-structured tests.
Provides helpful feedback when tests are missing or incomplete.
"""
import pytest
import inspect
from pathlib import Path

# Try to import the student's test module
try:
    import test_report_engine
    TEST_MODULE_EXISTS = True
except ImportError:
    TEST_MODULE_EXISTS = False
    test_report_engine = None


@pytest.mark.skipif(not TEST_MODULE_EXISTS, reason="test_report_engine.py not created yet - see test_report_engine_EXAMPLES.py for guidance")
class TestTestSuiteStructure:
    """Validate that test suite has proper structure and coverage."""

    def test_file_exists_and_imports(self):
        """test_report_engine.py should exist and be importable."""
        assert TEST_MODULE_EXISTS, """
        test_report_engine.py not found or has import errors.

        Create this file with your tests for ReportEngine.
        See test_report_engine_EXAMPLES.py for patterns to follow.
        """

    def test_has_test_classes(self):
        """Should organize tests into classes.

        Good test organization uses classes to group related tests.
        """
        classes = [name for name, obj in inspect.getmembers(test_report_engine, inspect.isclass)
                  if name.startswith('Test')]
        assert len(classes) >= 2, f"""
        Found {len(classes)} test classes. Create at least 2 test classes:
        - One for happy path scenarios (e.g., TestReportGenerationSuccess)
        - One for error handling (e.g., TestReportGenerationErrors)

        Example:
        class TestReportEngineBasics:
            def test_can_instantiate(self, mock_loader):
                engine = ReportEngine(mock_loader)
                assert engine is not None
        """

    def test_has_sufficient_tests(self):
        """Should have at least 10 test methods covering different scenarios."""
        # Count methods from all test classes
        test_methods = []
        for class_name, cls in inspect.getmembers(test_report_engine, inspect.isclass):
            if class_name.startswith('Test'):
                methods = [name for name, obj in inspect.getmembers(cls, inspect.isfunction)
                          if name.startswith('test_')]
                test_methods.extend(methods)

        assert len(test_methods) >= 10, f"""
        Found {len(test_methods)} tests. Create at least 10 tests covering:

        Happy Path (4-5 tests):
        - Can instantiate ReportEngine
        - Generates report successfully
        - Calls loader with correct filepath
        - Passes transactions to mode
        - Returns mode output

        Error Handling (3-4 tests):
        - FileNotFoundError from loader
        - ValueError from invalid data
        - Mode not called when loader fails

        Edge Cases (2-3 tests):
        - Empty transaction list
        - Multiple reports with same engine

        See test_report_engine_EXAMPLES.py for patterns.
        """


@pytest.mark.skipif(not TEST_MODULE_EXISTS, reason="test_report_engine.py not created yet")
class TestTestQuality:
    """Validate test quality and best practices."""

    def test_uses_fixtures(self):
        """Tests should use pytest fixtures for setup."""
        source = Path('test_report_engine.py').read_text()
        assert '@pytest.fixture' in source, """
        No fixtures found. Use fixtures to avoid repeating setup code.

        Example fixtures to create:
        @pytest.fixture
        def mock_loader():
            return Mock()

        @pytest.fixture
        def sample_transactions():
            return [{'date': '2024-01-15', 'amount': 45.50, ...}]

        Then use in tests:
        def test_something(self, mock_loader, sample_transactions):
            # fixtures automatically provided
        """

    def test_uses_mocking(self):
        """Tests should mock external dependencies."""
        source = Path('test_report_engine.py').read_text()
        has_mock = ('unittest.mock' in source or
                   'from unittest.mock import' in source or
                   'Mock' in source)
        assert has_mock, """
        No mocking found. Use mocks to test ReportEngine in isolation.

        Example:
        from unittest.mock import Mock

        def test_report_generation(self):
            mock_loader = Mock()
            mock_loader.load.return_value = [...]

            mock_mode = Mock()
            mock_mode.process_transactions.return_value = {...}

            engine = ReportEngine(mock_loader)
            result = engine.generate_report('file.csv', mock_mode)

        See test_report_engine_EXAMPLES.py for complete examples.
        """

    def test_has_good_docstrings(self):
        """Most test functions should have docstrings."""
        # Count methods from all test classes
        test_funcs = []
        for class_name, cls in inspect.getmembers(test_report_engine, inspect.isclass):
            if class_name.startswith('Test'):
                methods = [obj for name, obj in inspect.getmembers(cls, inspect.isfunction)
                          if name.startswith('test_')]
                test_funcs.extend(methods)

        funcs_with_docs = [f for f in test_funcs if f.__doc__ and len(f.__doc__.strip()) > 10]
        doc_ratio = len(funcs_with_docs) / max(len(test_funcs), 1)

        assert doc_ratio >= 0.6, f"""
        {doc_ratio*100:.0f}% of tests have docstrings. Aim for at least 60%.

        Docstrings help explain what each test verifies:

        def test_generates_report_successfully(self, mock_loader):
            \"\"\"Should generate report when given valid file and mode.\"\"\"
            # test code...
        """


@pytest.mark.skipif(not TEST_MODULE_EXISTS, reason="test_report_engine.py not created yet")
class TestTestCoverage:
    """Validate test coverage of important scenarios."""

    def test_covers_happy_path(self):
        """Should test successful report generation."""
        test_methods = []
        for class_name, cls in inspect.getmembers(test_report_engine, inspect.isclass):
            if class_name.startswith('Test'):
                methods = [name for name, obj in inspect.getmembers(cls, inspect.isfunction)
                          if name.startswith('test_')]
                test_methods.extend(methods)

        success_patterns = ['success', 'generate', 'valid', 'happy', 'work']
        success_tests = [t for t in test_methods
                        if any(pattern in t.lower() for pattern in success_patterns)]

        assert len(success_tests) >= 3, f"""
        Found {len(success_tests)} happy path tests. Include at least 3 tests for:
        - Successful report generation
        - Correct loader call
        - Correct mode call
        """

    def test_covers_error_handling(self):
        """Should test error scenarios."""
        source = Path('test_report_engine.py').read_text()

        has_file_error = 'FileNotFoundError' in source
        has_value_error = 'ValueError' in source or 'raises' in source

        assert has_file_error or has_value_error, """
        Should test error scenarios. Include tests for:
        - FileNotFoundError (file doesn't exist)
        - ValueError (invalid data)

        Example:
        def test_file_not_found_error(self, mock_loader):
            mock_loader.load.side_effect = FileNotFoundError("Not found")
            engine = ReportEngine(mock_loader)

            with pytest.raises(FileNotFoundError):
                engine.generate_report('missing.csv', Mock())
        """


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
