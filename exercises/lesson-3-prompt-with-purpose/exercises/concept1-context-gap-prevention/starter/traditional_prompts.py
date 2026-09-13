"""
Traditional prompts that demonstrate common structural problems.

Students will practice converting these to XML format to improve clarity and effectiveness.
"""

# Traditional Prompt 1: Vague and ambiguous
TRADITIONAL_PROMPT_1 = """
Write a function to process data from users and make sure it's secure and follows our patterns.
"""

# Traditional Prompt 2: Missing context and requirements
TRADITIONAL_PROMPT_2 = """
Add caching to the API endpoints so they're faster. Make sure it works with our current setup.
"""

# Traditional Prompt 3: Buried requirements and unclear constraints
TRADITIONAL_PROMPT_3 = """
Create a user authentication system that handles login, logout, and password reset while being secure and scalable, and make sure it integrates with our existing user database and follows industry best practices for security but don't use any external authentication services.
"""

# Example problems these prompts will cause:
EXPECTED_PROBLEMS = {
    "prompt_1": [
        "AI doesn't know what kind of data processing is needed",
        "Security requirements are vague",
        "No specific patterns are mentioned",
        "Function signature and return type are undefined"
    ],
    "prompt_2": [
        "No specific performance targets given", 
        "Current setup is not described",
        "Caching strategy unspecified",
        "No constraints on cache backends mentioned"
    ],
    "prompt_3": [
        "Multiple requirements buried in run-on sentence",
        "Security best practices not specified",
        "Database integration details missing",
        "Scalability requirements unclear",
        "Constraint about external services buried at the end"
    ]
}

def display_traditional_prompts():
    """Display traditional prompts and their common problems."""
    prompts = [
        ("Prompt 1: Vague Data Processing", TRADITIONAL_PROMPT_1),
        ("Prompt 2: Missing Context Caching", TRADITIONAL_PROMPT_2), 
        ("Prompt 3: Buried Requirements Auth", TRADITIONAL_PROMPT_3)
    ]
    
    print("=== TRADITIONAL PROMPTS ANALYSIS ===\n")
    
    for i, (title, prompt) in enumerate(prompts, 1):
        print(f"{title}:")
        print("-" * 50)
        print(prompt.strip())
        print("\nCommon problems this causes:")
        for problem in EXPECTED_PROBLEMS[f"prompt_{i}"]:
            print(f"  • {problem}")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    display_traditional_prompts()