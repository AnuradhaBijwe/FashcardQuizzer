"""
Test suite to validate architectural planning deliverables for Concept 1.

This test validates that students have completed the planning exercise
and created the required artifacts with appropriate content and quality.

Tests are organized to provide clear feedback on what's missing or needs improvement.
"""
import pytest
from pathlib import Path
import ast
import re


class TestPlanningArtifacts:
    """Validate that all required planning artifacts exist."""

    def test_architecture_plan_exists(self):
        """Architecture plan document must exist."""
        plan_file = Path("architecture_plan.md")
        assert plan_file.exists(), """
        architecture_plan.md not found. Create this file documenting your architectural decisions.

        Hint: Include sections for:
        - Architectural alternatives considered
        - Trade-offs between approaches
        - Selected architecture and rationale
        - Module design and responsibilities
        """

    def test_interfaces_file_exists(self):
        """Interfaces Python file must exist."""
        interfaces_file = Path("interfaces.py")
        assert interfaces_file.exists(), """
        interfaces.py not found. Create this file with your interface definitions.

        Hint: Define interfaces for:
        - TransactionLoader (loads CSV data)
        - ReportMode (strategy for different report types)
        Use ABC or Protocol pattern.
        """

    def test_project_structure_exists(self):
        """Project structure file must exist."""
        structure_file = Path("project_structure.txt")
        assert structure_file.exists(), """
        project_structure.txt not found. Create this file with your directory layout.

        Hint: Show directory structure with comments explaining each part.
        Include: main.py, utils/, tests/, data/
        """


class TestArchitecturePlanContent:
    """Validate architecture plan has required sections and quality."""

    @pytest.fixture
    def plan_content(self):
        """Load architecture plan content."""
        plan_file = Path("architecture_plan.md")
        if not plan_file.exists():
            pytest.skip("architecture_plan.md not found")
        return plan_file.read_text()

    def test_documents_alternatives(self, plan_content):
        """Plan should document multiple architectural alternatives."""
        alternatives_keywords = ['alternative', 'approach', 'option']
        found = any(keyword in plan_content.lower() for keyword in alternatives_keywords)
        assert found, """
        Architecture plan should document alternatives considered.

        Example: Include sections like "## Alternatives" or "## Approach Options"
        Describe at least 2-3 different ways to structure the system.
        """

    def test_includes_tradeoff_analysis(self, plan_content):
        """Plan should analyze trade-offs between approaches."""
        tradeoff_keywords = ['trade-off', 'tradeoff', 'pros', 'cons', 'advantage', 'disadvantage', 'benefit', 'drawback']
        found = any(keyword in plan_content.lower() for keyword in tradeoff_keywords)
        assert found, """
        Architecture plan should analyze trade-offs.

        Example: For each alternative, discuss:
        - Pros/Cons or Advantages/Disadvantages
        - When this approach works well vs poorly
        - Trade-offs in complexity vs extensibility
        """

    def test_states_selected_architecture(self, plan_content):
        """Plan should clearly state which architecture was selected."""
        selection_keywords = ['selected', 'chosen', 'decided', 'final', 'recommended', 'will use']
        found = any(keyword in plan_content.lower() for keyword in selection_keywords)
        assert found, """
        Architecture plan should clearly state the selected architecture.

        Example: Add section "## Selected Architecture" or "## Final Decision"
        Explain WHY you chose this approach over alternatives.
        """

    def test_describes_module_responsibilities(self, plan_content):
        """Plan should describe module design and responsibilities."""
        # Check for both module keywords AND responsibility indicators
        module_keywords = ['module', 'component', 'class']
        responsibility_keywords = ['responsib', 'handle', 'manage', 'orchestrate']

        has_modules = any(keyword in plan_content.lower() for keyword in module_keywords)
        has_responsibilities = any(keyword in plan_content.lower() for keyword in responsibility_keywords)

        assert has_modules and has_responsibilities, """
        Architecture plan should describe module design and what each part is responsible for.

        Example: Include section like "## Module Design" describing:
        - TransactionLoader: Responsible for loading and validating CSV data
        - ReportMode: Responsible for processing transactions into reports
        - ReportEngine: Responsible for orchestrating the report generation
        """


class TestInterfaceDefinitions:
    """Validate interface definitions are well-designed."""

    @pytest.fixture
    def interfaces_module(self):
        """Load and parse interfaces.py."""
        interfaces_file = Path("interfaces.py")
        if not interfaces_file.exists():
            pytest.skip("interfaces.py not found")

        content = interfaces_file.read_text()
        try:
            tree = ast.parse(content)
            return tree
        except SyntaxError as e:
            pytest.fail(f"interfaces.py has syntax errors: {e}")

    def test_uses_interface_pattern(self, interfaces_module):
        """Should use Protocol or ABC for interface definitions."""
        has_protocol = False
        has_abc = False

        for node in ast.walk(interfaces_module):
            if isinstance(node, ast.ImportFrom):
                if node.module == 'typing' and any(alias.name == 'Protocol' for alias in node.names):
                    has_protocol = True
                if node.module == 'abc' and any(alias.name in ['ABC', 'abstractmethod'] for alias in node.names):
                    has_abc = True

        assert has_protocol or has_abc, """
        interfaces.py should use Protocol or ABC for interface definitions.

        Example:
        from abc import ABC, abstractmethod

        class TransactionLoader(ABC):
            @abstractmethod
            def load(self, filepath: str) -> List[Dict[str, Any]]:
                pass
        """

    def test_defines_interfaces(self, interfaces_module):
        """Should define interface classes."""
        classes = [node for node in ast.walk(interfaces_module) if isinstance(node, ast.ClassDef)]
        assert len(classes) >= 1, """
        interfaces.py should define at least one interface class.

        Hint: Define interfaces for TransactionLoader and ReportMode based on your architecture plan.
        """

    def test_interfaces_documented(self, interfaces_module):
        """Interface classes should have docstrings."""
        classes = [node for node in ast.walk(interfaces_module) if isinstance(node, ast.ClassDef)]

        classes_without_docstrings = []
        for cls in classes:
            docstring = ast.get_docstring(cls)
            if not docstring:
                classes_without_docstrings.append(cls.name)

        assert len(classes_without_docstrings) == 0, \
            f"""
            These interface classes need docstrings: {', '.join(classes_without_docstrings)}

            Example:
            class TransactionLoader(ABC):
                \"\"\"Interface for loading transaction data from files.\"\"\"
            """


class TestProjectStructure:
    """Validate project structure is well-organized."""

    @pytest.fixture
    def structure_content(self):
        """Load project structure content."""
        structure_file = Path("project_structure.txt")
        if not structure_file.exists():
            pytest.skip("project_structure.txt not found")
        return structure_file.read_text()

    def test_includes_key_components(self, structure_content):
        """Should include essential project components."""
        # Check for main entry point
        has_main = 'main.py' in structure_content.lower()

        # Check for code organization
        has_utils = 'utils/' in structure_content.lower() or 'utils\\' in structure_content or 'src/' in structure_content.lower()

        # Check for tests
        has_tests = 'tests/' in structure_content.lower() or 'test/' in structure_content.lower()

        # Check for data
        has_data = 'data/' in structure_content.lower()

        missing = []
        if not has_main: missing.append("main.py (entry point)")
        if not has_utils: missing.append("utils/ or src/ (code directory)")
        if not has_tests: missing.append("tests/ (test directory)")
        if not has_data: missing.append("data/ (data directory)")

        assert len(missing) == 0, f"""
        Project structure is missing: {', '.join(missing)}

        Example structure:
        expense-tracker/
        ├── main.py
        ├── utils/
        │   ├── transaction_loader.py
        │   └── report_modes.py
        ├── tests/
        └── data/
        """

    def test_structure_has_comments(self, structure_content):
        """Structure should include comments explaining directories."""
        has_comments = '#' in structure_content or '//' in structure_content or '--' in structure_content
        assert has_comments, """
        Add comments to project_structure.txt explaining what each directory/file is for.

        Example:
        ├── main.py                    # CLI entry point
        ├── utils/
        │   ├── transaction_loader.py  # CSV loading and validation
        """


class TestDesignQuality:
    """Validate overall design quality and architectural thinking."""

    @pytest.fixture
    def all_content(self):
        """Load all planning artifacts."""
        content = {}
        files = ['architecture_plan.md', 'interfaces.py', 'project_structure.txt']
        for filename in files:
            filepath = Path(filename)
            if filepath.exists():
                content[filename] = filepath.read_text()
        return content

    def test_applies_solid_principles(self, all_content):
        """Should demonstrate understanding of SOLID principles."""
        combined = ' '.join(all_content.values()).lower()
        solid_keywords = ['solid', 'single responsibility', 'srp', 'open/closed', 'ocp',
                         'liskov', 'interface segregation', 'isp', 'dependency inversion', 'dip']

        mentions = [kw for kw in solid_keywords if kw in combined]
        assert len(mentions) >= 1, """
        Planning should reference SOLID principles.

        Example: Explain how your design follows principles like:
        - Single Responsibility: Each module has one clear job
        - Open/Closed: Easy to add new report types without modifying existing code
        - Dependency Inversion: Depend on interfaces (TransactionLoader) not concrete classes
        """

    def test_considers_extensibility(self, all_content):
        """Should explain how to extend the system."""
        combined = ' '.join(all_content.values()).lower()
        extensibility_keywords = ['extensib', 'extend', 'add new', 'future', 'plugin', 'strategy pattern']

        found = any(keyword in combined for keyword in extensibility_keywords)
        assert found, """
        Planning should address extensibility.

        Example: Explain how to:
        - Add new report types (new ReportMode strategy)
        - Support different data formats (new TransactionLoader)
        - Add new features without breaking existing code
        """


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
