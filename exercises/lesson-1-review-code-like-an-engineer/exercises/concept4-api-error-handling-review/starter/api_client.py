"""
Code Review Exercise 4: Simple API Client

Your task: Review this API client code for error handling and structural issues.
Look for issues related to:
- Network error handling
- HTTP response handling
- Input validation
- User experience

Instructions:
1. Identify missing error handling
2. Look for network error issues
3. Suggest basic improvements
4. Rate the overall code quality (Poor, Fair, Good, Excellent)
5. Provide your recommendation (Accept, Modify, Reject)
"""

import requests
import json
import time

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = 10  # Reasonable timeout in seconds
        self.max_retries = 3  # Maximum retry attempts
        self.base_delay = 1  # Base delay for exponential backoff in seconds

    def _calculate_backoff_delay(self, attempt):
        """Calculate exponential backoff delay: base_delay * 2^attempt"""
        return self.base_delay * (2 ** attempt)

    def _should_retry(self, exception, status_code=None):
        """Determine if request should be retried based on error type"""
        # Retry on network errors (ConnectionError, Timeout)
        if isinstance(exception, (requests.ConnectionError, requests.Timeout)):
            return True

        # Retry on 5xx server errors
        if status_code and 500 <= status_code < 600:
            return True

        # Don't retry on 4xx client errors
        return False

    def get_user_data(self, user_id):
        url = f"{self.base_url}/users/{user_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        last_exception = None

        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=self.timeout)

                if response.status_code == 200:
                    return response.json()
                elif 500 <= response.status_code < 600:
                    # Server error - retry with backoff
                    last_exception = Exception(f"Server error {response.status_code}: {response.text}")
                    if attempt < self.max_retries - 1:
                        delay = self._calculate_backoff_delay(attempt)
                        time.sleep(delay)
                        continue
                    else:
                        raise last_exception
                else:
                    # Client error (4xx) - don't retry
                    raise Exception(f"API request failed with status {response.status_code}: {response.text}")

            except requests.ConnectionError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Connection error: Unable to reach the server at {url}. Please check your network connection.") from e

            except requests.Timeout as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Request timeout: The server did not respond within {self.timeout} seconds.") from e

            except requests.RequestException as e:
                raise Exception(f"Request failed: An unexpected error occurred while making the request.") from e

            except json.JSONDecodeError as e:
                raise Exception(f"Invalid response: The server returned malformed JSON data.") from e

    def update_user(self, user_id, data):
        url = f"{self.base_url}/users/{user_id}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        last_exception = None

        for attempt in range(self.max_retries):
            try:
                response = requests.put(url, headers=headers, data=json.dumps(data), timeout=self.timeout)

                if response.status_code == 200:
                    return True
                elif 500 <= response.status_code < 600:
                    # Server error - retry with backoff
                    last_exception = Exception(f"Server error {response.status_code}: {response.text}")
                    if attempt < self.max_retries - 1:
                        delay = self._calculate_backoff_delay(attempt)
                        time.sleep(delay)
                        continue
                    else:
                        raise last_exception
                else:
                    # Client error (4xx) - don't retry
                    raise Exception(f"API request failed with status {response.status_code}: {response.text}")

            except requests.ConnectionError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Connection error: Unable to reach the server at {url}. Please check your network connection.") from e

            except requests.Timeout as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Request timeout: The server did not respond within {self.timeout} seconds.") from e

            except requests.RequestException as e:
                raise Exception(f"Request failed: An unexpected error occurred while making the request.") from e