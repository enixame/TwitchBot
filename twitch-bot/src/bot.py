import requests
from twitchio.ext import commands, routines
from fuzzywuzzy import fuzz
import re
import config

class TwitchBot(commands.Bot):
    def __init__(self, token, client_id, nick, prefix, channel):
        super().__init__(token=token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=[channel])
        self.channel_name = channel

    def generate_joke(self):
        api_key = config.OPENAI_API_KEY  # Utilise la clé API OpenAI depuis .env
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "text-davinci-003",  # Ou un autre modèle disponible
            "prompt": "Tell me a funny joke in French.",
            "max_tokens": 50  # Limite le nombre de tokens pour éviter des réponses trop longues
        }
        
        response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
        joke = response.json()["choices"][0]["text"].strip()
        return joke

    def get_current_game(self):
        client_id = config.CLIENT_ID  # Utilise le Client ID depuis .env
        access_token = config.OAUTH_TOKEN.replace('oauth:', '')  # Utilise le token OAuth depuis .env

        headers = {
            'Client-ID': client_id,
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params={'user_login': self.channel_name})
        data = response.json()
        
        if data['data']:
            game_id = data['data'][0]['game_id']
            game_response = requests.get(f'https://api.twitch.tv/helix/games?id={game_id}', headers=headers)
            game_data = game_response.json()
            
            if game_data['data']:
                game_name = game_data['data'][0]['name']
                return game_name
        return None

    def detect_game_question(self, message_content):
        patterns = [
            r'\bquel est le jeu\b', r'\bc\'est quoi le jeu\b', r'\bjeu actuel\b',
            r'\bquel jeu\b', r'\bà quel jeu joues-tu\b', r'\bquel est ce jeu\b'
        ]
        
        for pattern in patterns:
            if re.search(pattern, message_content, re.IGNORECASE):
                return True

        game_questions = [
            "quel est le jeu", "c'est quoi le jeu", "jeu actuel", "quel jeu", 
            "à quel jeu joues-tu", "quel est ce jeu"
        ]
        
        for question in game_questions:
            if fuzz.partial_ratio(question.lower(), message_content.lower()) > 80:
                return True
        
        return False

    def detect_greeting(self, message_content):
        patterns = [
            r'\bsalut\b', r'\bbonjour\b', r'\bhey\b', r'\bcoucou\b',
            r'\bcomment ça va\b', r'\bça va\b', r'\bcomment vas-tu\b',
            r'\bla forme\b', r'\bcomment te sens-tu\b'
        ]

        for pattern in patterns:
            if re.search(pattern, message_content, re.IGNORECASE):
                return True

        common_phrases = [
            "salut", "bonjour", "hey", "coucou", "comment ça va", "ça va", 
            "comment vas-tu", "la forme", "comment te sens-tu"
        ]

        for phrase in common_phrases:
            if fuzz.partial_ratio(phrase.lower(), message_content.lower()) > 80:
                return True
        
        return False

    @routines.routine(minutes=20)
    async def joke_task(self):
        joke = self.generate_joke()
        channel = self.get_channel(self.channel_name)
        if channel:
            await channel.send(joke)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        
        # Démarre la tâche d'envoi de blagues lorsque le bot est prêt
        self.joke_task.start()  # Pas besoin de vérifier si la tâche est en cours d'exécution

    async def event_message(self, message):

        # Ignore les messages du bot lui-même
        if message.author.name.lower() == self.nick.lower():
           return

        if self.detect_greeting(message.content):
            await message.channel.send(f"Salut {message.author.name}, ça va bien, et toi ?")
        elif self.detect_game_question(message.content):
            game_name = self.get_current_game()
            if game_name:
                await message.channel.send(f"Le jeu actuel est '{game_name}'.")
            else:
                await message.channel.send("Désolé, je n'ai pas pu récupérer le jeu actuellement diffusé.")
        
        await self.handle_commands(message)

if __name__ == "__main__":
    token = config.OAUTH_TOKEN  # Utilise le token OAuth depuis .env
    client_id = config.CLIENT_ID()  # Utilise le Client ID depuis .env
    nick = config.BOT_NAME  # Utilise le nom du bot depuis .env
    prefix = '!'  # Préfixe pour les commandes
    channel = config.CHANNEL_NAME  # Utilise le nom de la chaîne depuis .env

    bot = TwitchBot(token=token, client_id=client_id, nick=nick, prefix=prefix, channel=channel)
    bot.run()
