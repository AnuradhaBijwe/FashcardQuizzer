"""
Tests to validate documentation quality.
Checks that required documentation exists and meets quality standards.
"""
import pytest
from pathlib import Path
import ast
import re


DOC_EXISTS = {
    'readme': Path('../solution/README.md').exists(),
    'architecture': Path('../solution/ARCHITECTURE.md').exists(),
}


@pytest.mark.skipif(not DOC_EXISTS['readme'], reason="README.md not created yet")
class TestReadmeQuality:
    """Validate README.md completeness."""

    def test_readme_exists(self):
        """README.md should exist."""
        assert Path('../solution/README.md').exists(), """
        Create README.md with user-facing documentation.

        Should include:
        - Installation instructions
        - Usage examples
        - CSV format specification
        - Troubleshooting guide
        """

    def test_has_installation_section(self):
        """Should have installation instructions."""
        content = Path('../solution/README.md').read_text()
        assert re.search(r'##\s+Installation', content, re.IGNORECASE), """
        Add ## Installation section with setup instructions.
        """

    def test_has_usage_section(self):
        """Should have usage examples."""
        content = Path('../solution/README.md').read_text()
        assert re.search(r'##\s+Usage', content, re.IGNORECASE), """
        Add ## Usage section with examples of how to run the program.
        """

    def test_has_code_examples(self):
        """Should include code examples."""
        content = Path('../solution/README.md').read_text()
        assert '```' in content, """
        Include code examples in ```code blocks```.

        Example:
        ```bash
        python main.py -f expenses.csv -m summary
        ```
        """

    def test_has_substantial_content(self):
        """README should have meaningful content."""
        content = Path('../solution/README.md').read_text()
        assert len(content) > 500, "README seems too brief - aim for comprehensive user guide"


@pytest.mark.skipif(not DOC_EXISTS['architecture'], reason="ARCHITECTURE.md not created yet")
class TestArchitectureDocQuality:
    """Validate ARCHITECTURE.md completeness."""

    def test_architecture_doc_exists(self):
        """ARCHITECTURE.md should exist."""
        assert Path('../solution/ARCHITECTURE.md').exists(), """
        Create ARCHITECTURE.md with developer documentation.

        Should include:
        - Component descriptions
        - Design patterns used
        - Module responsibilities
        - Extension points
        """

    def test_describes_components(self):
        """Should describe system components."""
        content = Path('../solution/ARCHITECTURE.md').read_text()
        assert 'component' in content.lower() or 'module' in content.lower(), """
        Describe the system components/modules and their responsibilities.
        """

    def test_explains_design_patterns(self):
        """Should mention design patterns used."""
        content = Path('../solution/ARCHITECTURE.md').read_text()
        assert 'pattern' in content.lower() or 'strategy' in content.lower(), """
        Explain which design patterns are used (e.g., Strategy pattern for report modes).
        """

    def test_has_substantial_content(self):
        """Architecture doc should have meaningful content."""
        content = Path('../solution/ARCHITECTURE.md').read_text()
        assert len(content) > 500, "Architecture doc seems too brief - provide detailed explanation"


# NEW: Test that source code has docstrings
class TestSourceCodeDocumentation:
    """Validate that source code modules have docstrings."""

    def test_transaction_loader_has_module_docstring(self):
        """transaction_loader.py should have module-level docstring."""
        # Check in solution (where students add docs)
        module_path = Path('../solution/transaction_loader.py')
        if not module_path.exists():
            pytest.skip("transaction_loader.py not found in solution")

        content = module_path.read_text()
        tree = ast.parse(content)
        module_doc = ast.get_docstring(tree)

        assert module_doc is not None, """
        Add module-level docstring to transaction_loader.py.

        Example:
        \"\"\"
        Transaction Loader Module

        Provides CSV loading functionality for transaction data.
        Validates required fields and data types.
        \"\"\"
        """

    def test_report_modes_has_module_docstring(self):
        """report_modes.py should have module-level docstring."""
        module_path = Path('../solution/report_modes.py')
        if not module_path.exists():
            pytest.skip("report_modes.py not found in solution")

        content = module_path.read_text()
        tree = ast.parse(content)
        module_doc = ast.get_docstring(tree)

        assert module_doc is not None, """
        Add module-level docstring to report_modes.py explaining the strategy pattern.
        """

    def test_classes_have_docstrings(self):
        """Major classes should have docstrings."""
        files_to_check = [
            '../solution/transaction_loader.py',
            '../solution/report_modes.py',
            '../solution/report_engine.py',
            '../solution/cli_interface.py'
        ]

        classes_without_docs = []

        for filepath in files_to_check:
            path = Path(filepath)
            if not path.exists():
                continue

            content = path.read_text()
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        classes_without_docs.append(f"{path.name}::{node.name}")

        assert len(classes_without_docs) == 0, f"""
        These classes need docstrings: {', '.join(classes_without_docs)}

        Each class should explain its purpose and usage.
        """


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
