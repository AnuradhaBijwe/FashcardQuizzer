# Concept 4: API Error Handling Review

## Learning Objective
Learn to identify and fix basic error handling issues in API client code, focusing on network errors, HTTP status codes, and user-friendly error messages.

## Background
API clients need proper error handling to provide good user experience and prevent crashes. Common issues include:
- Unhandled network timeouts and connection errors
- Poor HTTP status code handling  
- Returning None without explanation
- Missing input validation

## Exercise Structure

### Starter Code (`starter/`)
- **File**: `api_client.py` - Simple API client with error handling problems
- **Issues**: Network errors crash the program, HTTP failures return None, no input validation
- **Test File**: `test_api_errors.py` - Tests that demonstrate the problems

### Solution Code (`solution/`)
- **File**: `api_client.py` - Fixed API client with proper error handling
- **Improvements**: Try/catch blocks, HTTP status checking, structured error responses, input validation
- **Test File**: `test_api_improvements.py` - Tests that verify the fixes work

## How to Run

### Test the Starter Code (Shows Problems)
```bash
cd starter/
python api_client.py
pytest test_api_errors.py -v
```

### Test the Solution Code (Shows Fixes)
```bash
cd solution/
python api_client.py
pytest test_api_improvements.py -v
```

## Key Issues to Find

### 1. Network Error Handling
- **Problem**: Network timeouts and connection errors crash the program
- **Fix**: Use try/catch blocks to handle requests exceptions gracefully

### 2. HTTP Status Code Handling
- **Problem**: Only checks for 200, returns None for all other status codes
- **Fix**: Check for common status codes (404, 401, 500) and return helpful error messages

### 3. Error Information
- **Problem**: Functions return None without explaining what went wrong
- **Fix**: Return structured responses with error details

### 4. Input Validation
- **Problem**: No validation of parameters (empty URLs, user IDs, etc.)
- **Fix**: Add basic validation with clear error messages

## Code Review Questions

When reviewing the starter code, consider:

1. **Error Handling**: What happens when network requests fail?
2. **Status Codes**: How are different HTTP response codes handled?
3. **User Experience**: Do users get helpful error messages?
4. **Input Validation**: Are parameters validated before use?
5. **Return Values**: Do functions return useful information about failures?

## Expected Learning Outcomes

After completing this exercise, you should be able to:
- Identify missing network error handling in API clients
- Recognize poor HTTP status code handling patterns
- Implement try/catch blocks for network operations
- Design user-friendly error response structures
- Add basic input validation to API methods