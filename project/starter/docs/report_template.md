# AI-Assisted Development Project Report

**Student Name:** Anuradha Bijwe 
**Project Title:** Flashcard Quizzer 
**Date:** 09/14/2026

## Executive Summary

Provide a brief overview of your project (2-3 paragraphs):
- What application did you build?
For this project, I built a Python command-line application called Flashcard Quizzer. The application allows users to load flashcards from a JSON file and practice them directly from the terminal. It supports different quiz modes so that users can choose how they want the questions to be presented.
- What were the main features and functionality?
The main features include JSON data loading and validation, sequential, random, and adaptive quiz modes, command-line arguments, colored feedback for correct and incorrect answers, quiz statistics, and graceful exit handling. I used the Strategy and Factory design patterns to keep the quiz logic organized and make the application easier to extend.
- How did you collaborate with AI throughout the development process?
AI was used throughout the development process as a coding assistant. Instead of asking AI to build the entire application at once, I divided the requirements into smaller phases and provided specific prompts for each one. I reviewed the generated code, refined my prompts when needed, and used pytest to verify that the final implementation worked as expected.
## Project Overview

### Problem Statement
The goal of this project was to create a simple tool that helps users study and remember information using flashcards. The application needed to run completely from the command line, read flashcard information from JSON files, and provide multiple ways of practicing the questions.
Another important goal was to make the application reliable and easy to maintain. Invalid or incomplete JSON data should not crash the program, and the code should be structured so that additional quiz modes or features can be added later without making major changes.

### Solution Approach
Explain your approach to solving the problem, including:
- Key design decisions
I divided the implementation into three main parts. First, I created the data layer to load and validate flashcards. The loader supports both a JSON array of flashcards and an object containing a cards array. Validation was added to detect malformed JSON and missing required fields such as front and back, while providing understandable error messages.
- Architecture choices
For the quiz logic, I used the Strategy Pattern to separate the three quiz behaviors. SequentialMode presents cards in their original order, RandomMode shuffles them, and AdaptiveMode gives additional attention to cards answered incorrectly. I also used the Factory Pattern to create the correct quiz mode based on the mode selected by the user.
- Technology stack used
The CLI was then connected to these components using Python's argparse module. The application accepts the flashcard file and quiz mode through command-line arguments. The solution mainly uses Python's standard libraries, with pytest and pytest-cov used for testing and coverage verification.
### Final Features
List the features you implemented:
- [X] Core functionality #1 - Load and validate the Flashcards from JSON file.
- [X] Core functionality #2 - Sequence, Random and Adaptive quiz modes
- [X] Core functionality #3 - Strategy and Factory pattern implementation along with handling command line argument using argparse
- [ ] Additional feature #1 - CLI option with colored correct/incorrect feedback.
- [ ] Additional feature #2 - Quiz Statetics and graceful error handling.

## AI Collaboration Experience

### AI Tools Used
List the AI tools/assistants you worked with:
- [X] Claude
- [ ] GitHub Copilot
- [ ] ChatGPT
- [ ] Other: ________

### Collaboration Workflow
Describe your typical workflow when working with AI:
1. How did you structure your requests/prompts?
   I broke the project into smaller phases instead of asking AI to build everything at once. For each phase, I provided the project context, clear requirements, constraints, and examples of the expected behavior. This helped keep the responses focused and easier to review.
3. What types of tasks did you ask AI to help with?
   I used AI mainly for implementing the JSON data loader, quiz modes, Strategy and Factory design patterns, CLI interaction, error handling, and pytest test cases. I also used it to review the code and suggest improvements where needed.
5. How did you review and validate AI-generated code?
   After each response, I reviewed the generated files and checked whether the code matched the project requirements. I ran the application manually and used pytest to verify the expected behavior. I also checked error scenarios, quiz modes, and code coverage instead of accepting the first AI response without validation.
7. What was your process for refining AI suggestions?
When the output was incomplete, too large, or did not fully match the requirements, I gave follow-up prompts with more specific instructions. I asked the AI to make only the required changes, preserve the existing working code, and fix issues identified during testing. This iterative process helped improve the final solution.
### Most Valuable AI Interactions
Document 3-5 specific examples where AI assistance was particularly helpful:

#### Example 1: [Flashcard Data Loading and Validation]
**Context:** I needed to create the data layer that could read flashcards from JSON files and validate the input before starting the quiz.
**AI Prompt:** I asked AI to create a flashcard loader that supports both a JSON array and an object containing a cards array. I also specified that every card must contain front and back fields and that invalid JSON should be handled without displaying raw Python errors.
**AI Response:** AI created the file-loading and validation logic and added error handling for malformed JSON, missing fields, and invalid data structures.
**Your Changes:** I reviewed the implementation against the project requirements and refined my prompts to make the validation and error messages clearer.
**Outcome:** The application could successfully load valid flashcards and gracefully reject invalid or incomplete JSON files.

#### Example 2: [Implementing Quiz Modes Using Design Patterns]
**Context:**  I needed three different quiz behaviors while keeping the code modular and easy to extend.
**AI Prompt:** I asked AI to implement a QuizMode abstract base class with SequentialMode, RandomMode, and AdaptiveMode, using the Strategy Pattern. I also requested a Factory Pattern to select the correct mode based on user input.
**AI Response:** AI created the common quiz-mode abstraction, the three strategy classes, and factory logic for selecting the requested mode.
**Your Changes:** I reviewed how each mode handled the flashcards, especially Adaptive Mode, and refined the requirements so incorrectly answered cards would be prioritized correctly.
**Outcome:** The application supported all three required quiz modes while keeping each mode's behavior separate and maintainable.

#### Example 3: [Building and Testing the CLI]
**Context:**  I needed to connect the data loader and quiz logic into a complete command-line application and verify that the components worked together.
**AI Prompt:** I asked AI to implement the CLI using argparse, support -f, -m, and --stats, display colored feedback, and allow graceful exit using exit or Ctrl+C. I later asked AI to generate pytest tests for the required scenarios.
**AI Response:** AI connected the application components, implemented the command-line interaction, and generated tests for the data loader, quiz modes, and full-session behavior.
**Your Changes:** I reviewed the generated tests and implementation, ran the test suite, and used the test results to identify areas that needed refinement instead of assuming the generated code was correct.
**Outcome:** The individual components worked together as a complete Flashcard Quizzer, and automated tests were available to verify the required functionality.

[Continue for additional examples...]

### Challenges with AI Collaboration
Describe any difficulties you encountered:
- What types of requests did AI struggle with?
  AI was useful for generating the initial implementation, but some responses needed additional refinement. When a prompt contained too many requirements at once, the generated solution sometimes became more complex than necessary or did not fully follow the existing project structure
- When did you need to significantly modify AI suggestions?
  Breaking the work into smaller phases helped me get more focused results.
I also noticed that AI was good at creating the initial code structure and suggesting design patterns, but I still needed to review the generated code against the project requirements
- What patterns did you notice in AI strengths/weaknesses?
  For areas such as Adaptive Mode, error handling, and testing, I used more specific follow-up prompts to clarify the expected behavior. This showed me that AI works best when the requirements and constraints are clearly defined and its output is reviewed and tested rather than accepted directly.

## Software Engineering Practices

### Code Quality Measures
Document the practices you implemented:
- [ ] Code formatting (Black, isort)
- [X] Linting (flake8, mypy)
- [X] Type hints
- [X] Documentation/comments
- [X] Error handling

### Testing Strategy
Describe your approach to testing:
- What types of tests did you write?
  I wrote both unit and integration tests using pytest. The unit tests covered JSON loading and validation, invalid data, quiz mode selection, and Adaptive Mode behavior. I also added an integration test to check a complete quiz session and verify that the different components work together correctly.
- What was your test coverage percentage?
  I used pytest-cov to measure the test coverage. My goal was to achieve the project requirement of more than 80% coverage. The final percentage was 97%
  ========================================================= tests coverage ==========================================================
________________________________________ coverage: platform linux, python 3.10.14-final-0 _________________________________________

Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
main.py                             93      2    98%   167, 287
tests/__init__.py                    0      0   100%
tests/test_file_handler.py          42      0   100%
tests/test_flashcard_loader.py     157      0   100%
tests/test_integration.py          304      0   100%
tests/test_task_manager.py          48      0   100%
utils/__init__.py                    0      0   100%
utils/console.py                    36      4    89%   44, 46, 66, 93
utils/file_handler.py               89      2    98%   58-59
utils/quiz_engine.py               136     16    88%   94, 124, 159-160, 172-175, 210-211, 272, 274, 292, 356, 368-373, 379
utils/task_manager.py               26      0   100%
--------------------------------------------------------------
TOTAL                              931     24    97%
- How did you ensure code reliability?
I tested both normal and error scenarios instead of checking only successful cases. This included malformed JSON, missing required fields, different quiz modes, incorrect answers, and complete quiz sessions. I also reran the test suite after making changes to make sure existing functionality was not affected.
- Did you use test-driven development?
I did not follow strict test-driven development. I first implemented each project phase and then created tests to validate the functionality. When tests identified an issue, I refined the implementation and ran the tests again. So, my approach was more iterative development and testing than pure TDD.
### Design Patterns Used
List and explain the design patterns you implemented:
- **Strategy Pattern:** Used for the quiz modes. A common `QuizMode` abstraction allows `SequentialMode`, `RandomMode`, and `AdaptiveMode` to implement different question-selection behaviors independently. This keeps the quiz logic modular and makes it easier to add new modes later.
- **Factory Pattern:** Used to select and create the appropriate quiz mode based on the user's command-line input. This keeps object-creation logic separate from the main application flow and avoids multiple mode-selection conditions throughout the code.

### Code Structure and Organization
Explain how you organized your code:
- Module separation and responsibilities
  I organized the code into separate modules so that each part of the application has a clear responsibility. The file-handling module is responsible for loading and validating the JSON data, while the quiz engine contains the quiz modes and related logic.
- How you maintained separation of concerns
  Code Structure and Organization
I organized the code into separate modules so that each part of the application has a clear responsibility. The file-handling module is responsible for loading and validating the JSON data, while the quiz engine contains the quiz modes and related logic. The main.py file acts as the entry point and handles the command-line interaction.
I maintained separation of concerns by keeping data loading, quiz behavior, and user interaction independent from each other. I also separated the different quiz behaviors using the Strategy Pattern and moved mode creation into the Factory instead of putting all the logic in main.py. This made the code easier to understand, test, and extend.
- Any refactoring you performed
I refactored the code by separating data handling, quiz logic, and CLI interaction into different components. I also used Strategy and Factory patterns to avoid large conditional blocks and make the code easier to maintain and extend.

## Technical Challenges and Solutions

### Challenge 1: [Handling Different JSON Formats]
**Problem:** The application needed to support two JSON structures: a direct array of flashcards and an object containing a cards array. It also needed to handle malformed JSON and missing front or back fields without crashing.
**Solution:** I kept the loading and validation logic in a separate file handler. The input is first loaded, converted into a consistent flashcard structure, and then validated before it is passed to the quiz engine.
**AI Involvement:** AI helped generate the initial loader and validation logic. I used more specific follow-up prompts to make sure both formats and the required error cases were covered.
**Lessons Learned:** I learned that validating external data before using it makes the rest of the application simpler and more reliable.

### Challenge 2: [Supporting Different Quiz Behaviors]
**Problem:** Sequential, Random, and Adaptive modes behave differently. Putting all three behaviors into one large block of conditional logic would make the code difficult to maintain.
**Solution:** I used the Strategy Pattern with a common QuizMode abstraction and separate implementations for each mode. I then used a Factory to create the appropriate mode based on the user's selection.
**AI Involvement:** AI helped me structure the Strategy and Factory implementations. I reviewed the generated logic and refined the prompts, particularly around the expected Adaptive Mode behavior.
**Lessons Learned:** I learned how design patterns can solve practical code-organization problems. Separating each behavior made the solution cleaner and will make it easier to add another quiz mode later.

[Continue for additional challenges...]

## Code Quality Analysis

### Metrics
Provide quantitative measures of your code quality:
- Lines of code: __819_
- Test coverage: __97_%
- Number of functions/classes: __61_
- Linting score: 100% Pass

### Self-Assessment
Rate yourself (1-5, 5 being excellent) and provide justification:
- **Code Readability:** _4/5__ - Why? I kept the code organized with meaningful function and class names, type hints, comments, and docstrings. I also used Flake8 to identify formatting and code-quality issues and corrected them.
- **Code Maintainability:** __4/5_ - Why? I separated the data loading, quiz logic, quiz modes, and CLI responsibilities instead of putting everything in one file. The use of Strategy and Factory patterns also makes it easier to add or change quiz modes later.
- **Test Quality:** 4/5___ - Why? I created unit and integration tests covering valid inputs, invalid JSON, missing required fields, quiz mode creation, adaptive behavior, and a complete quiz session. I also used pytest coverage to identify untested areas.
- **Documentation:** _4/5__ - Why? I added comments and docstrings where needed and documented the project structure, implementation approach, testing, AI collaboration, and lessons learned in the project report.

## Learning Outcomes

### Technical Skills Developed
What new technical skills did you acquire or improve?
- Programming concepts:
  During this project, I improved my understanding of Python classes, abstract base classes, type hints, exception handling, JSON processing, and command-line arguments
- Tools and frameworks:
  I also gained practical experience implementing the Strategy and Factory design patterns rather than only understanding them theoretically. along with hands on AI tool Claude which help me to understand how to work collaboratively with AI to work effectively.  
- Testing practices:
  I became more comfortable using pytest, pytest-cov, Flake8, and argparse. Writing both unit and integration tests helped me understand how individual components can be tested separately and then validated together as a complete application.
- Code organization
I also learned the importance of separating responsibilities across modules so that code is easier to understand, test, and maintain.
### AI Collaboration Skills
What did you learn about working with AI assistants?
One of my main learnings was that the quality of the AI response depends heavily on the quality of the prompt. Instead of asking AI to "build the application," I divided the work into phases and gave it the context, requirements, constraints, and expected behavior for each phase.
I also learned not to accept generated code without reviewing it. I ran the application, executed pytest and Flake8, reviewed errors, and then used more specific follow-up prompts to correct problems. AI was most useful for generating an initial implementation, suggesting design approaches, creating tests, and helping investigate errors. Manual review was still important for checking whether the generated solution actually matched the project requirements.

### Software Engineering Insights
What software engineering principles did you better understand?
This project helped me better understand why design patterns, testing strategies, code organization, and refactoring are important in a real application. The Strategy pattern allowed the quiz behavior to vary without putting all mode-specific logic in one place, while the Factory pattern provided a single place for selecting the correct quiz mode.
I also learned that separation of concerns makes testing and future changes easier. Keeping file handling, validation, quiz logic, and CLI interaction separate meant that a change in one area did not require redesigning the whole application.

## Reflection

### What Worked Well
Reflect on the most successful aspects of your project:
1. Breaking the project into smaller phases worked well. I first focused on loading and validating the flashcard data, then implemented the quiz modes and design patterns, and finally connected everything through the CLI. This made it easier to understand and validate each part before moving forward.
2. Structured prompting was the most effective AI collaboration technique for me. Providing the requirements, constraints, expected behavior, and testing expectations produced much more useful results than using short or general prompts.
3. Testing had the biggest impact on the final solution because it exposed problems that were not obvious just by reading the code. I am particularly satisfied that the final application combines data validation, multiple quiz strategies, CLI interaction, error handling, and automated testing in one structured solution.

### What Could Be Improved
Identify areas for future improvement:
1. Next time, I would define the complete module structure and testing approach before starting the implementation. Some issues were discovered later through pytest and Flake8, so running these checks after every small implementation would have reduced the amount of rework.
2. The code could be enhanced further by simplifying some helper functions and increasing test coverage for additional edge cases. For AI collaboration, I would also make my initial prompts more specific about existing file structure and coding standards so that fewer corrections are needed later.

### Future Enhancements
If you had more time, what features would you add?
1.  I would add features such as saving quiz progress, tracking scores across multiple sessions, and allowing users to select flashcard categories or difficulty levels.
2.  The adaptive mode could also be improved by tracking how often individual cards are answered incorrectly.
For a better user experience, I would consider adding a simple graphical or web interface instead of relying only on the command line.
3.  From a technical perspective, I would further improve validation, logging, test coverage, and performance when working with larger flashcard files.

## Conclusion

Summarize your key takeaways from this project:
1. This project gave me practical experience using AI as part of a software development workflow rather than simply using it to generate code. I learned that AI can speed up implementation and provide useful suggestions, but the developer still needs to understand the requirements, review the generated code, test it, and refine the solution.
2. I will continue using practices such as modular design, separation of concerns, design patterns, automated testing, linting, and incremental refactoring in future projects.
3. I will also continue using structured prompts and iterative AI collaboration, while making sure that the final implementation is validated through my own review and testing.

## Appendices

### Appendix A: AI Interaction Log
Reference your detailed AI interaction log (`ai_edit_log.md`) and highlight key entries.
The detailed AI interaction history is available in `ai_edit_log.md`.
Key AI interactions included:
- Creating the flashcard data loading and validation logic.
- Implementing SequentialMode, RandomMode, and AdaptiveMode using the Strategy pattern.
- Implementing the Factory pattern for quiz mode selection.
- Building the command-line interface using argparse.
- Generating pytest unit and integration tests.
- Reviewing test failures and refining the implementation.
- Reviewing and fixing Flake8 code-quality issues.

### Appendix B: Code Statistics
Include any relevant code metrics, test results, or performance measurements.
The following metrics were collected from the final implementation:
 
- Lines of code: __819_
- Test coverage: __97_%
- Number of functions/classes: __61_
- Linting score: 100% Pass with no errors
- Testing framework: pytest
- Test types: Unit tests and integration tests
 
All automated tests were executed using:
 
`python -m pytest tests/`
 
Test coverage was checked using:
 
`python -m pytest --cov=. --cov-report=term-missing`

### Appendix C: Additional Resources
List any resources that were particularly helpful during your project.
Resources used during the project included:
- Project-provided AI Prompting Best Practices guide
- Python documentation
- pytest documentation
- Flake8 documentation
- Python argparse documentation
- Course instructions and project requirements
---

**Total Report Length:** Aim for 2000-3000 words  
**Due Date:** [Insert due date]  
**Submission Instructions:** [Insert submission details]
