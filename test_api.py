import requests
import time

# Wait for server to start
time.sleep(2)

try:
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}") 