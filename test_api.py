import requests
from datetime import datetime

# Base URL of your API
BASE_URL = "http://localhost:8000"

# Test GET request with a timestamp parameter
def test_get_articles(timestamp):
    endpoint = f"{BASE_URL}/articles/"
    params = {"timestamp": timestamp}

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        print("GET /articles passed:", response.json())
    else:
        print("GET /articles failed:", response.status_code, response.json())

# Test POST request to fetch articles (simulate background task trigger)
def test_fetch_articles():
    endpoint = f"{BASE_URL}/fetch/"
    response = requests.post(endpoint)
    if response.status_code == 200:
        print("POST /fetch passed:", response.json())
    else:
        print("POST /fetch failed:", response.status_code, response.json())

if __name__ == "__main__":
    # Run the GET test with a sample timestamp
    sample_timestamp = datetime.now().isoformat()  # Example timestamp
    test_get_articles(sample_timestamp)

    # Run the POST test
    test_fetch_articles()
