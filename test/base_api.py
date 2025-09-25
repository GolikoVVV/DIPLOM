import requests
from data import BASE_URL, API_KEY

class BaseAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            'X-API-KEY': API_KEY,  # Используем X-API-KEY
            'Content-Type': 'application/json'
        }

    def search(self, query):
        url = f"{self.base_url}/movie/search"
        params = {
            'query': query,
            'page': 1,
            'limit': 5
        }
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при запросе: {e}")
            return None