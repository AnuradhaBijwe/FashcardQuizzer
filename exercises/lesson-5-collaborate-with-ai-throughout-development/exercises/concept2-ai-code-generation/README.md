# Concept 2: AI Code Generation

## Overview

Learn to generate high-quality, maintainable code through effective AI collaboration. You'll implement specific modules following the architecture planned in Concept 1, focusing on generating production-ready code with proper error handling, type hints, and testability.

## Learning Objectives

- Generate structured, maintainable code with AI assistance
- Maintain architectural consistency across generated modules
- Apply code quality standards to AI-generated output
- Validate generated code against engineering principles

## Exercise: Implementing the Flashcard Quizzer Core

Using the architecture from Concept 1, you'll generate the core modules of the flashcard quizzer CLI:

### Implementation Requirements
- Follow the planned architecture exactly
- Include comprehensive error handling
- Add complete type hints and docstrings
- Ensure all code is testable
- Validate input at appropriate boundaries

## Instructions

### Step 1: Generate the Flashcard Loader

Create the core flashcard loading module using structured prompting from Lesson 3:

```xml
<role>Senior Python developer expert in data validation and file I/O</role>
<task>
Implement FlashcardLoader for loading and validating flashcard data from JSON files
</task>
<context>
<application>CLI flashcard quizzer with JSON data storage</application>
<data_format>JSON files containing flashcard arrays with question/answer pairs</data_format>
<integration_points>Must work with quiz engine and provide validated flashcard data</integration_points>
</context>
<requirements>
<data_model>
- question: str (required, the question text)
- answer: str (required, the correct answer)
- difficulty: str (optional, values: "easy", "medium", "hard")
- category: str (optional, subject categorization)
- hints: List[str] (optional, helpful hints for users)
- explanation: str (optional, detailed explanation of answer)
</data_model>
<core_methods>
- load_flashcards(file_path: Path) -> List[Dict[str, Any]]: Load from JSON file
- validate_flashcard(flashcard: Dict) -> bool: Validate single flashcard structure
- validate_flashcards(flashcards: List[Dict]) -> List[Dict]: Validate entire set
- get_categories(flashcards: List[Dict]) -> Set[str]: Extract unique categories
</core_methods>
<validation_rules>
- Required fields (question, answer) must be non-empty strings
- Difficulty must be one of: "easy", "medium", "hard" if provided
- Hints must be a list of strings if provided
- Handle missing optional fields gracefully
- Provide clear error messages for validation failures
</validation_rules>
</requirements>
<constraints>
<code_quality>
- Complete type hints using typing module
- Comprehensive docstrings following Google style
- Robust error handling for file I/O operations
- Clean validation logic with early returns
</code_quality>
<error_handling>
- Custom FlashcardValidationError for data issues
- Handle FileNotFoundError, JSONDecodeError gracefully
- Clear error messages indicating specific validation problems
- Graceful handling of malformed JSON structure
</error_handling>
</constraints>
<deliverables>
- FlashcardLoader class implementation
- FlashcardValidationError custom exception
- Complete type hints and comprehensive docstrings
- Robust file loading and validation logic
</deliverables>
```

### Step 2: Generate the Repository Interface

Implement the abstract repository using structured prompting:

```xml
<role>Senior Python developer expert in repository pattern and ABC design</role>
<task>
Create abstract TaskRepository interface for task persistence
</task>
<context>
<design_pattern>Repository pattern for data access abstraction</design_pattern>
<implementation>Python ABC (Abstract Base Class) with type hints</implementation>
<data_model>Task objects with CRUD and filtering operations</data_model>
</context>
<requirements>
<interface_methods>
- save(task: Task) -> None: Persist task to storage
- get_all() -> List[Task]: Retrieve all tasks
- get_by_id(task_id: str) -> Optional[Task]: Find specific task
- update(task: Task) -> bool: Update existing task
- delete(task_id: str) -> bool: Remove task from storage
- filter_by_status(status: Status) -> List[Task]: Filter by completion status
- filter_by_priority(priority: Priority) -> List[Task]: Filter by priority level
</interface_methods>
<error_handling>
- Custom RepositoryError for persistence failures
- FileNotFoundError for missing storage files
- ValidationError for invalid task data
</error_handling>
</requirements>
<constraints>
<implementation_style>
- Use Python ABC module correctly
- All methods must be abstract with @abstractmethod
- Complete type hints including imports
- Comprehensive docstrings with parameters and exceptions
</implementation_style>
<integration_requirements>
- Must work with Task model from previous step
- Compatible with JSON file storage implementation
- Support for future database implementations
</integration_requirements>
</constraints>
<deliverables>
- TaskRepository abstract base class
- Custom exception classes for repository errors
- Complete type hints and docstring documentation
- Import statements for all dependencies
</deliverables>
```

### Step 3: Generate the JSON Repository Implementation

Create the concrete JSON storage implementation using structured prompting:

```xml
<role>Senior Python developer expert in file I/O and data persistence</role>
<task>
Implement JSONTaskRepository that extends TaskRepository for JSON file storage
</task>
<context>
<storage_mechanism>JSON file-based persistence with atomic writes</storage_mechanism>
<base_interface>TaskRepository abstract base class from previous step</base_interface>
<data_safety>Must prevent data corruption and support recovery</data_safety>
</context>
<requirements>
<file_operations>
- Atomic file writes using temporary files and rename
- Read JSON data with proper error handling
- Create backup files before modifications
- Handle missing files gracefully (empty repository)
</file_operations>
<implementation_methods>
- Implement all abstract methods from TaskRepository
- Efficient filtering without loading entire dataset
- Proper serialization of Task objects to/from JSON
- Thread-safe operations for concurrent access
</implementation_methods>
</requirements>
<constraints>
<data_integrity>
- Never lose data due to interrupted writes
- Validate JSON structure on load
- Handle corrupted files with clear error messages
- Maintain backup of previous state
</data_integrity>
<performance>
- Lazy loading for large datasets
- Efficient filtering algorithms
- Minimal memory usage for file operations
- Proper cleanup of temporary files
</performance>
<error_handling>
- Handle FileNotFoundError, PermissionError, JSONDecodeError
- Custom RepositoryError with descriptive messages
- Logging for debugging without exposing sensitive data
- Graceful degradation for file system issues
</error_handling>
</constraints>
<deliverables>
- JSONTaskRepository class implementing TaskRepository
- Helper methods for file operations and JSON serialization
- Comprehensive error handling and logging
- Complete type hints and documentation
</deliverables>
```

### Step 4: Generate the Service Layer

Implement the business logic layer using structured prompting:

```xml
<role>Senior Python developer expert in service layer architecture and dependency injection</role>
<task>
Create TaskService class that encapsulates all business logic for task management
</task>
<context>
<architecture_layer>Service layer between CLI interface and repository</architecture_layer>
<dependency_injection>Accepts TaskRepository interface for testability</dependency_injection>
<business_domain>Task management with validation and business rules</business_domain>
</context>
<requirements>
<crud_operations>
- create_task(title, description, priority) -> Task: Create and save new task
- get_all_tasks() -> List[Task]: Retrieve all tasks with sorting
- get_task(task_id) -> Optional[Task]: Find specific task
- update_task(task_id, **updates) -> bool: Modify existing task
- complete_task(task_id) -> bool: Mark task as complete
- delete_task(task_id) -> bool: Remove task permanently
</crud_operations>
<business_logic>
- Generate unique task IDs using UUID
- Validate task data according to business rules
- Enforce status transitions (pending -> complete only)
- Set completion timestamps automatically
- Default sorting by priority then creation date
</business_logic>
<filtering_capabilities>
- filter_tasks(status=None, priority=None) -> List[Task]
- get_pending_tasks() -> List[Task]
- get_completed_tasks() -> List[Task]
- get_high_priority_tasks() -> List[Task]
</filtering_capabilities>
</requirements>
<constraints>
<validation_rules>
- Task titles must be 1-200 characters
- Descriptions must be under 1000 characters
- Cannot complete already completed tasks
- Cannot modify completed tasks except deletion
</validation_rules>
<error_handling>
- Custom ServiceError for business logic violations
- Propagate repository errors with context
- Clear error messages for validation failures
- Handle edge cases gracefully
</error_handling>
<testability>
- Accept repository through constructor (dependency injection)
- No direct file system access
- Pure business logic separate from I/O operations
- Easy to mock dependencies for unit testing
</testability>
</constraints>
<deliverables>
- TaskService class with all required methods
- Business validation and rule enforcement
- Custom exception handling
- Complete type hints and comprehensive docstrings
</deliverables>
```

## Validation Criteria

Your generated code should demonstrate:

- ✅ Consistent architecture following the planned design
- ✅ Comprehensive error handling with custom exceptions
- ✅ Complete type hints and docstrings
- ✅ Testable design with dependency injection
- ✅ Input validation at appropriate boundaries
- ✅ Professional code quality and style

## Files to Create

In the `starter/` directory, implement:
- `flashcard_loader.py` - JSON file loading and validation
- `quiz_engine.py` - Core quiz orchestration logic
- `quiz_modes.py` - Strategy pattern implementations (Sequential, Random, Adaptive)
- `cli_interface.py` - Terminal UI and user interaction
- `exceptions.py` - Custom exception hierarchy for validation and quiz errors

## Tips for Effective Code Generation

1. **Be specific about requirements** - Include all quality criteria in prompts
2. **Generate one module at a time** - Focus on getting each component right
3. **Review and iterate** - Don't accept the first version, refine for quality
4. **Validate integration** - Ensure modules work together as planned
5. **Test as you go** - Generate simple tests to validate functionality

## Time Estimate

45-60 minutes