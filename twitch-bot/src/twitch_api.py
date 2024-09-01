# src/twitch_api

import requests
import config

class TwitchAPIManager:
    def __init__(self, client_id, oauth_token):
        self.client_id = client_id
        self.oauth_token = oauth_token

    def get_current_game(self, channel_name):
        """Récupère le jeu actuel diffusé sur la chaîne donnée."""
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.oauth_token.replace("oauth:", "")}'
        }

        try:
            response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params={'user_login': channel_name})
            response.raise_for_status()
            data = response.json()
            
            if data['data']:
                game_id = data['data'][0]['game_id']
                game_response = requests.get(f'https://api.twitch.tv/helix/games?id={game_id}', headers=headers)
                game_response.raise_for_status()
                game_data = game_response.json()
                
                if game_data['data']:
                    return game_data['data'][0]['name']
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à Twitch API: {e}")
        
        return None
