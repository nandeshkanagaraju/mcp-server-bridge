import requests

url = "http://localhost:8000/query"
data = {"query": "SELECT * FROM employees LIMIT 5"}

response = requests.post(url, json=data)
print(response.json())
