# Concept 5: AI Documentation Generation

**Exercise Goal**: Generate comprehensive documentation for the complete expense tracker: README for users, ARCHITECTURE.md for developers, and enhanced docstrings.

## Prompt Examples (Adjust as needed)

**Prompt 1** (Generate User README):

```xml
<role>
Technical writer creating clear end-user documentation
</role>

<task>
Revise the exisiting project and generate an updated README.md for expense tracker CLI application
</task>

<target_audience>
End users who want to track and analyze expenses:
- May not be Python developers
- Need clear setup and usage instructions
- Want examples they can copy/paste
- Need to understand CSV format requirements
</target_audience>

<application_context>
<what_it_does>
CLI tool that loads expense transactions from CSV and generates reports:
- Summary by category (Food, Transport, etc.)
- Monthly totals breakdown
Displays formatted reports in terminal
</what_it_does>

<technical_details>
- Python 3.8+ required
- No external dependencies (stdlib only)
- CSV format: date,amount,category,description
- Entry point: main.py
- Sample data included in data/ folder
</technical_details>
</application_context>

<content_requirements>
Include these sections:

## Overview
- One paragraph: what it does, who it's for

## Installation
- Prerequisites (Python version)
- Setup steps (clone, navigate)
- How to verify it works

## Quick Start
- Simplest usage example
- Show expected output

## Usage
- All command-line options explained
- CSV format specification with example
- Different report mode examples with outputs

## Examples
- Basic usage with sample data
- Custom data file
- Different report types
- Show actual terminal output for each

## Troubleshooting
- File not found errors
- Invalid CSV format
- Common mistakes and solutions
</content_requirements>

<style_guidelines>
- Use clear, concise language (no jargon unless explained)
- Every command in code block
- Show expected output for examples
- Use real-world expense examples (groceries, transport, etc.)
- Include emoji for visual sections (sparingly)
- Markdown formatting for readability
</style_guidelines>
```

**Prompt 2** (Generate Developer Architecture Documentation):

```xml
<task>
Generate ARCHITECTURE.md explaining system design for developers
</task>

<target_audience>
Software developers who need to:
- Understand how the system works
- Modify existing functionality
- Add new features (new report types, data sources)
- Debug issues
- Contribute to the project
</target_audience>

<system_components>
<modules>
- transaction_loader.py: CSV loading and validation (TransactionLoader ABC, CSVTransactionLoader implementation)
- report_modes.py: Report strategies (ReportMode ABC, SummaryByCategory, MonthlyTotalReport)
- report_engine.py: Orchestration (ReportEngine coordinates loader and mode)
- cli_interface.py: Terminal display formatting
- main.py: CLI entry point with argument parsing
</modules>

<design_patterns>
- Strategy Pattern: For pluggable report types
- Dependency Injection: ReportEngine depends on abstractions
- Abstract Base Classes: Define clear contracts
</design_patterns>

</system_components>

<content_requirements>
## Overview
- System purpose and goals
- Key design principles

## Architecture Diagram
- ASCII art or simple text diagram showing components
- Data flow visualization
- Dependency relationships

## Design Patterns
- Which patterns used and where
- Why each pattern was chosen
- Benefits for this application

## Module Descriptions
For each module:
- Purpose and responsibility
- Public interface (key classes/methods)
- Dependencies
- Extension points

## Adding New Features
### How to add a new report type:
- Step-by-step instructions
- Code example showing new strategy implementation
- Where to register it

### How to add a new data source:
- Implement TransactionLoader
- Integration points

## Design Decisions
- Why Strategy pattern for reports
- Why ABC for interfaces
- Why CSV not database
- Trade-offs considered

## Testing Strategy
- How modules are tested
- Mocking strategy
- Where to find tests
</content_requirements>
```

**Prompt 3** (Enhance Module Docstrings):

```xml
<task>
Review and enhance docstrings in all Python modules for completeness
</task>

<modules_to_review>
- transaction_loader.py
- report_modes.py
- report_engine.py
- cli_interface.py
</modules_to_review>

<docstring_standards>
Module Level:
- Purpose statement
- Brief usage example
- Key classes/functions listed

Class Level:
- What the class does
- When/why to use it
- Simple usage example
- Attributes if any

Method Level (for public methods):
- One-line summary
- Args: with types and descriptions
- Returns: with type and description
- Raises: all exceptions that can be raised
- Example for complex methods

Follow Google-style docstring format
</docstring_standards>

<action>
For each module, identify any missing or incomplete docstrings and provide enhanced versions. Show before/after for the most significant improvements.
</action>
```