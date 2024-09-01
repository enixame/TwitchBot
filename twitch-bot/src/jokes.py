# src/jokes

import requests

class JokeManager:
    def __init__(self):
        self.joke_api_url = "https://v2.jokeapi.dev/joke/Any?lang=fr&format=json&blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

    def get_joke(self):
        """Récupère une blague en français sans contenu inapproprié."""
        response = requests.get(self.joke_api_url)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data["type"] == "single":
                return joke_data["joke"]
            else:
                return f"{joke_data['setup']} ... {joke_data['delivery']}"
        else:
            return "Je n'ai pas pu trouver de blague pour le moment."
        