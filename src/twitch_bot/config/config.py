# config.py

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les variables d'environnement
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
CHANNEL_ID = os.getenv('CHANNEL_ID')
BOT_NAME = os.getenv('BOT_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WIT_AI_TOKEN = os.getenv('WIT_AI_TOKEN')