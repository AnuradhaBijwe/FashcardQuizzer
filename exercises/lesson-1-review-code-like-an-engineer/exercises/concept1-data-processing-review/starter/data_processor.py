"""
Code Review Exercise 1: Data Processing Function

Your task: Review this code using the engineering judgment framework.
Look for issues related to:
- Structure & Organization
- Naming & Clarity  
- Error Handling
- Testability

Instructions:
1. Identify all issues you can find
2. Classify each issue by category (structure, naming, error handling, etc.)
3. Suggest specific improvements
4. Rate the overall code quality (Poor, Fair, Good, Excellent)
5. Provide your recommendation (Accept, Modify, Reject)
"""

def process_data(data):
    result = []
    for item in data:
        if item['status'] == 'active':
            temp = item['value'] * 1.2
            if temp > 100:
                temp = 100
            result.append({'id': item['id'], 'processed_value': temp})
    return result


