# twitch_api.py

import requests
import time
from googletrans import Translator

from twitch_bot.twitch.twitch_utils import split_message

class TwitchAPIManager:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = None
        self.token_expires_at = 0  # Timestamp d'expiration du token


    def get_auth_token(self):
        """Récupère un jeton d'identification"""

        url = 'https://id.twitch.tv/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(url, headers=headers, data=data)

            # Assurer que la requête a réussi
            if response.status_code == 200:
                token_data = response.json()

                # Récupérer l'access token et l'expiration
                access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in')  # temps d'expiration en secondes

                # Afficher le token et le temps avant expiration
                print(f"Access Token: {access_token}")
                print(f"Expires in: {expires_in} seconds")

                # Stocker le token et calculer l'heure d'expiration
                self.oauth_token = access_token
                self.token_expires_at = time.time() + expires_in  # Stocke l'heure d'expiration en timestamp

            else:
                print(f"Failed to retrieve token. Status code: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à Twitch API: {e}")
 

    def is_token_expired(self):
        """Vérifie si le token est expiré ou proche de l'expiration"""
        return time.time() > self.token_expires_at - 300  # Vérifie si le token expire dans les 5 minutes


    def translate_text(self, text, target_language='fr'):
        """Traduit un texte en utilisant l'API Google Translate"""
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        return translated.text


    def get_game_details_from_igdb(self, game_name):
        """Récupère les détails d'un jeu via l'API IGDB"""
        url = 'https://api.igdb.com/v4/games'
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.oauth_token}'
        }
        data = f'search "{game_name}"; fields name, genres.name, storyline, summary;'

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            game_data = response.json()

            if game_data:
                game_info = game_data[0]
                game_name = game_info.get('name')
                genres = ', '.join([genre['name'] for genre in game_info.get('genres', [])]) if game_info.get('genres') else 'Unknown'
                storyline = game_info.get('storyline', 'No storyline available')
                summary = game_info.get('summary', 'No summary available')

                genres_fr = self.translate_text(genres)
                storyline_fr = self.translate_text(storyline)
                summary_fr = self.translate_text(summary)

                # Créer une réponse sous forme de tableau
                response = [f"Le jeu actuel est {game_name} (Source IGDB)", f"Genres: {genres_fr}"]
                response += split_message(f"Storyline: {storyline_fr}")
                response += split_message(f"Summary: {summary_fr}")

                return response

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à IGDB API: {e}")
        
        return None
    

    def get_current_game(self, channel_name):
        """Récupère le jeu actuel diffusé sur la chaîne donnée."""

        # Vérifier si le token est expiré ou va bientôt expirer
        if not self.oauth_token or self.is_token_expired():
            print("Le jeton a expiré ou va bientôt expirer. Obtention d'un nouveau jeton.")
            self.get_auth_token() 
    
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.oauth_token.replace("oauth:", "")}'
        }

        try:
            response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params={'user_login': channel_name})
            response.raise_for_status()
            data = response.json()
            
            print(f"{data}")

            if data['data']:
                game_id = data['data'][0]['game_id']
                game_response = requests.get(f'https://api.twitch.tv/helix/games?id={game_id}', headers=headers)
                game_response.raise_for_status()
                game_data = game_response.json()
                
                if game_data['data']:
                    game_name = game_data['data'][0]['name']
                    print(f"Game Name: {game_name}")

                    # Récupérer les détails du jeu via IGDB
                    game_details = self.get_game_details_from_igdb(game_name)
                    if game_details:
                        return game_details
                    else:
                        return [f"Le jeu actuel est {game_name}"]
                    
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à Twitch API: {e}")
        
        return None
