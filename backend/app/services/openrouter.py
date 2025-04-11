import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class OpenRouterService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_response(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Erreur lors de l'appel à OpenRouter: {str(e)}")
            return "Désolé, je n'ai pas pu générer de réponse pour le moment." 