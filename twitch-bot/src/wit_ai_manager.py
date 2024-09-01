# src/wait_ai_manager

import requests

class WitAIManager:
    def __init__(self, wit_ai_token):
        self.wit_ai_token = wit_ai_token

    def detect_intent(self, message_content):
        """Utilise Wit.ai pour détecter l'intention dans le message."""
        headers = {
            'Authorization': f'Bearer {self.wit_ai_token}',
            'Content-Type': 'application/json'
        }
        url = f"https://api.wit.ai/message?v=20230831&q={requests.utils.quote(message_content)}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            intent = json_response.get('intents', [{}])[0].get('name', None) if json_response.get('intents') else None
            return intent
        else:
            print(f"Erreur Wit.ai: {response.status_code} - {response.text}")
            return None
