# Concept 1: AI Planning Collaboration

**Exercise Goal**: Use AI to plan expense tracker architecture with proper module design, testing strategy, and SOLID principles.

## Prompt examples (Adjust as needed)

**Prompt 1** (Initial Architecture Planning):

```xml
<role>
Senior Python developer following SOLID principles
</role>

<task>
Design modular architecture for a CLI expense tracker application
</task>

<context>
<application_type>Command-line expense tracking and reporting tool</application_type>
<tech_stack>Python 3.8+, CSV file storage, standard library only</tech_stack>
<user_workflow>
1. User runs CLI with expense data file
2. User selects report mode (summary by category, monthly totals, etc.)
3. Application displays formatted report in terminal
</user_workflow>
</context>

<requirements>
<functional>
- Load transaction data from CSV files (date, amount, category, description)
- Support multiple report modes that are easy to add/extend
- Display formatted reports in terminal
- Track totals and provide summaries
- Handle errors gracefully (file not found, invalid data)
</functional>

<architectural>
- Follow SOLID principles explicitly (especially Open/Closed for extensibility)
- Use Strategy pattern for different report types
- Separate concerns: data loading, processing, display
- Each module should be independently testable
- Maximum 200 lines per module
</architectural>
</requirements>

<deliverables>
Provide:
1. High-level architecture with module names and responsibilities
2. Specific design patterns to use and why they fit
3. Module dependency diagram showing data flow
4. File/folder structure
5. Extension points for adding new report types
</deliverables>
```

**Prompt 2** (Generate Project Structure and Interfaces):

```xml
<task>
Create detailed project structure and Python interface definitions for the expense tracker
</task>

<architecture_decisions>
Based on previous discussion:
- TransactionLoader: Handles CSV loading and validation
- ReportMode: Strategy interface for different report types
- ReportEngine: Orchestrates the complete workflow
- CLIInterface: Terminal display formatting
</architecture_decisions>

<deliverables>
1. Complete file/folder structure showing all modules and test files
2. Python interface definitions (abstract base classes) for:
   - TransactionLoader (with load method signature)
   - ReportMode (with process_transactions signature)
   Include docstrings specifying contracts
3. Brief implementation notes for each interface
</deliverables>

<constraints>
- Use ABC (Abstract Base Class) from Python standard library
- Include full type hints
- Specify what exceptions each method should raise
- Keep interfaces minimal and focused
</constraints>
```

**Prompt 3** (Quick Risk Assessment):

```xml
<task>
Identify top 3 risks for this expense tracker implementation and mitigation strategies
</task>

<context>
We're building a CLI expense tracker with CSV file loading, multiple report strategies, and terminal display. This is a learning project demonstrating AI collaboration.
</context>

<risk_categories>
- Security risks (file handling, data validation, injection vulnerabilities)
- Reliability risks (error handling, data integrity)
- Ethical risks (data privacy, accessibility)
</risk_categories>

<format>
For each of top 3 risks:
- What could go wrong
- Impact if it happens
- How we'll prevent it
- Keep it concise (2-3 sentences each)
</format>
```