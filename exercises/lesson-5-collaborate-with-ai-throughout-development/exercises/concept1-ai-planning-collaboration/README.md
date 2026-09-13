# Concept 1: AI Planning Collaboration

## Overview

Learn to collaborate with AI during the architectural planning phase. You'll use AI to explore design alternatives, evaluate trade-offs, and create a solid foundation for implementation—all while maintaining ownership of engineering decisions.

## Learning Objectives

- Use structured XML prompts to guide AI through architectural exploration
- Evaluate multiple architectural alternatives with clear trade-off analysis
- Design modular systems with clear responsibilities and interfaces
- Make informed architectural decisions based on engineering principles
- Create implementation roadmaps that guide development

## Exercise Structure

This exercise has two parts:

- **Part A (Guided Practice)**: Plan an expense tracker architecture to learn the methodology
- **Part B (Your Project)**: Apply the same techniques to plan your own application

The goal is to master the planning process,not to become an expense tracker expert.

---

## Part A: Guided Practice - Expense Tracker Planning

### Scenario

You're building a CLI expense tracker that helps users analyze their spending from CSV transaction files. The application should support different types of reports (by category, by month, etc.) and be easily extensible for new report types.

### Functional Requirements

- Load expense transactions from CSV files
- Support multiple report modes: summary by category, monthly totals
- Display formatted reports in the terminal
- Calculate totals and provide accurate summaries
- Handle invalid data gracefully

### Technical Requirements

- Python 3.8+ with standard library only
- Modular architecture following SOLID principles
- Strategy pattern for different report types
- Clean separation: data loading, business logic, UI
- Comprehensive error handling

---

## Step 1: Architectural Exploration (15 minutes)

Use AI to generate 2-3 architectural alternatives. Copy this prompt template and use it with your AI assistant:

```xml
<role>Senior Python architect with expertise in SOLID principles and design patterns</role>

<task>
Evaluate and compare 2-3 architectural approaches for a CLI expense tracker application
</task>

<context>
<application_type>Command-line personal finance report generator</application_type>
<tech_stack>Python 3.8+, CSV file storage, terminal interface</tech_stack>
<user_workflow>Load transactions from CSV → Select report mode → View formatted report</user_workflow>
<data_structure>Transactions with date, description, category, amount (negative for expenses)</data_structure>
</context>

<requirements>
<functional_requirements>
- Load and validate expense transactions from CSV files
- Support multiple report modes (summary by category, monthly totals, etc.)
- Display formatted reports in terminal with totals
- Handle invalid data and missing files gracefully
- Track and display summary statistics
</functional_requirements>

<extensibility_requirements>
- Easy to add new report modes without modifying existing code
- Support for different data formats (JSON, etc.) in future
- Configurable report formatting and display options
- Plugin architecture for custom report types
</extensibility_requirements>

<quality_attributes>
- High testability with minimal mocking required
- Clear separation of concerns (data, logic, UI)
- Minimal coupling between components
- Single responsibility for each module
</quality_attributes>
</requirements>

<constraints>
<architecture_principles>Follow SOLID principles explicitly</architecture_principles>
<complexity_limits>Keep each module under 200 lines, single responsibility</complexity_limits>
<dependencies>Standard library only, no external frameworks</dependencies>
<error_handling>Comprehensive validation and clear error messages</error_handling>
</constraints>

<deliverables>
- 2-3 distinct architectural approaches with trade-offs
- Specific design patterns to use and why (Strategy, Factory, etc.)
- Module responsibilities and interfaces
- Extension points for future report types
- Recommendation with justification
</deliverables>
```

**What to do with AI's response:**
1. Read through each architectural alternative carefully
2. Note the trade-offs for each approach
3. Consider: Which approach makes testing easier? Which is more extensible? Which is simpler to implement?
4. Don't just accept AI's recommendation—evaluate it against your own judgment

**Document your findings** in `architecture_plan.md`:
- List the alternatives AI suggested
- Note the key trade-offs
- State which you'd choose and why

---

## Step 2: Module Design (15 minutes)

Once you've selected an architecture, use AI to design the specific modules and interfaces:

```xml
<role>Senior Python developer expert in module design and interface definition</role>

<task>
Design detailed module structure and interfaces for expense tracker using [YOUR CHOSEN ARCHITECTURE]
</task>

<context>
<selected_architecture>
[Paste the architecture you selected from Step 1]
</selected_architecture>
<design_principles>SOLID principles, dependency injection, interface segregation</design_principles>
<integration_requirements>Modules must integrate smoothly with minimal coupling</integration_requirements>
</context>

<requirements>
<module_specifications>
- Each module has single, clear responsibility
- Public interfaces with complete type hints
- Private implementation details hidden
- Minimal dependencies between modules
</module_specifications>

<interface_design>
- Method signatures with type annotations
- Docstring specifications (purpose, params, returns, raises)
- Error handling strategy for each module
- Input validation boundaries
</interface_design>

<core_modules>
1. TransactionLoader - CSV loading and validation
2. ReportMode (Protocol/ABC) - Interface for report strategies
3. ReportEngine - Orchestrates report generation
4. CLIInterface - Terminal UI and user interaction
</core_modules>

<data_models>
- Transaction representation (date, description, category, amount)
- Report data structure
- Error types (FileNotFoundError, ValidationError, etc.)
</data_models>
</requirements>

<constraints>
<implementation_guidelines>
- Interfaces are minimal and focused
- No circular dependencies
- Design for testability (dependency injection)
- Extension points clearly identified
</implementation_guidelines>
</constraints>

<deliverables>
- Module responsibility descriptions
- Interface definitions with type hints (as Python Protocol or ABC)
- Data model specifications
- Dependency diagram showing relationships
</deliverables>
```

**What to do with AI's response:**
1. Review each module's responsibility—is it focused and clear?
2. Check interfaces—are they minimal and testable?
3. Look for circular dependencies—none should exist
4. Verify extension points—can new report modes be added easily?

**Create `interfaces.py`** with the interface definitions AI suggested (as Protocols or ABCs).

---

## Step 3: Project Structure (10 minutes)

Generate the complete directory structure:

```xml
<role>Senior Python developer expert in project organization</role>

<task>
Create comprehensive project directory structure for CLI expense tracker
</task>

<context>
<modules>
[List the modules from Step 2]
</modules>
<architecture>
[Brief description of chosen architecture]
</architecture>
</context>

<requirements>
<source_organization>
- Logical grouping of related modules
- Clear entry point (main.py)
- Utility modules in dedicated folder
- Sample data for development/testing
</source_organization>

<testing_structure>
- Test directory mirroring source structure
- Unit tests for each module
- Integration tests for workflows
- Test fixtures and mock data
</testing_structure>

<development_support>
- README with setup and usage
- requirements.txt (even if empty for stdlib-only)
- Sample CSV files for testing
- Documentation folder structure
</development_support>
</requirements>

<constraints>
- Follow Python packaging best practices
- Use standard directory names
- Clear naming conventions
- Support development and distribution
</constraints>

<deliverables>
- Complete directory tree with explanations
- File naming conventions
- Import path strategy
</deliverables>
```

**Create `project_structure.txt`** showing your planned directory layout.

---

## Deliverables for Part A

In the `starter/` folder, create these files:

### 1. `architecture_plan.md`
Document your architectural decisions:
- **Alternatives Considered**: What options did AI suggest?
- **Trade-off Analysis**: Pros/cons of each approach
- **Selected Architecture**: Your choice with justification
- **Module Design**: Responsibilities and interfaces
- **Extension Strategy**: How to add new features
- **Implementation Roadmap**: Order of development

### 2. `interfaces.py`
Python code with interface definitions:
```python
"""
Core interfaces for expense tracker application.
"""
from typing import Protocol, List, Dict
from abc import ABC, abstractmethod

class ReportMode(Protocol):
    """Protocol defining interface for report generation strategies."""

    def process_transactions(self, transactions: List[Dict]) -> Dict:
        """Process transactions and return report data."""
        ...

class TransactionLoader(Protocol):
    """Protocol for loading and validating transactions."""

    def load(self, filepath: str) -> List[Dict]:
        """Load transactions from file with validation."""
        ...

# Add other interfaces based on your architecture
```

### 3. `project_structure.txt`
```
expense-tracker/
├── main.py                    # CLI entry point
├── utils/
│   ├── __init__.py
│   ├── transaction_loader.py  # CSV loading
│   ├── report_engine.py       # Core orchestration
│   ├── report_modes.py        # Strategy implementations
│   └── cli_interface.py       # Terminal UI
├── tests/
│   ├── __init__.py
│   ├── test_transaction_loader.py
│   ├── test_report_engine.py
│   ├── test_report_modes.py
│   └── test_cli_interface.py
├── data/
│   └── sample_expenses.csv    # Sample data
├── README.md
└── requirements.txt
```

---

## Part B: Apply to Your Project

Now apply the same planning methodology to your own application idea.

### Step 1: Define Your Project

Choose what you want to build:
- **Personal productivity**: Task manager, habit tracker, note organizer
- **Educational tools**: Vocabulary builder, study scheduler, math practice
- **Utilities**: File organizer, log analyzer, data converter
- **Simple games**: Text adventure, quiz game, number puzzle
- **Data tools**: CSV processor, report generator, configuration manager

### Step 2: Adapt the Prompts

Take the XML prompt templates from Part A and adapt them for your domain:
- Change `<application_type>` to your app type
- Modify `<functional_requirements>` for your features
- Update `<data_structure>` for your data models
- Adjust `<design_patterns>` for your specific needs

### Step 3: Document Your Plan

Create `my_project_plan.md` with:
1. **Project Vision**: What you're building and why
2. **Requirements Analysis**: Functional and technical requirements
3. **Architectural Alternatives**: Options explored with trade-offs
4. **Selected Architecture**: Your choice with justification
5. **Module Design**: Interfaces and responsibilities
6. **Implementation Roadmap**: Development order and phases

---

## Validation

Run the provided test to validate your planning:

```bash
cd starter/
pytest test_planning_process.py -v
```

This test checks:
- ✅ `architecture_plan.md` exists and has required sections
- ✅ `interfaces.py` contains properly defined interfaces
- ✅ `project_structure.txt` shows logical organization
- ✅ Interfaces follow Protocol or ABC patterns
- ✅ No obvious circular dependencies in design

---

## Tips for Success

1. **Don't accept first suggestion**: Use `<deliverables>` to request alternatives
2. **Question AI's recommendations**: Apply your engineering judgment
3. **Focus on extensibility**: Make adding features easy
4. **Design for testability**: Dependency injection, clear interfaces
5. **Keep it simple**: Resist over-engineering temptation
6. **Document rationale**: Capture why you made decisions

## Common Pitfalls to Avoid

❌ **Accepting AI's first suggestion without evaluation**
✅ Request alternatives and analyze trade-offs

❌ **Over-engineering the architecture**
✅ Start simple, add complexity only when justified

❌ **Skipping interface definitions**
✅ Clear interfaces enable independent module development

❌ **Ignoring testability in design**
✅ Design for dependency injection and minimal mocking

❌ **Circular dependencies between modules**
✅ Use dependency injection and interface segregation

---

## Time Estimate

- **Part A (Guided)**: 40 minutes
- **Part B (Your Project)**: 30-40 minutes
- **Total**: ~70-80 minutes

## Next Steps

In Concept 2, you'll use AI to generate the actual code for the modules you've designed here. Having a clear plan makes code generation much more effective!

---

## Resources

- Review Lesson 3 for XML prompting techniques
- Reference SOLID principles when evaluating architectures
- Check solution folder for example complete planning documents
