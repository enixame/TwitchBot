# src/response.py

import re
from fuzzywuzzy import fuzz

class ResponseManager:
    def __init__(self):
        # Définir les patterns regex pour les salutations et questions communes
        self.greeting_patterns = [
            r'\bsalut\b', r'\bbonjour\b', r'\bhey\b', r'\bcoucou\b',
            r'\bhello\b'
        ]
        self.status_patterns = [
            r'\bcomment ça va\b', r'\bça va\b', r'\bcomment vas-tu\b',
            r'\bla forme\b', r'\bcomment te sens-tu\b'
        ]
        self.game_question_patterns = [
            r'\bquel est le jeu\b', r'\bc\'est quoi le jeu\b', r'\bjeu actuel\b',
            r'\bquel jeu\b', r'\bà quel jeu joues-tu\b', r'\bquel est ce jeu\b'
        ]

    def detect_greeting(self, message_content):
        """Détecte les salutations dans le message."""
        for pattern in self.greeting_patterns:
            if re.search(pattern, message_content, re.IGNORECASE):
                return True

        return False

    def detect_status_question(self, message_content):
        """Détecte les questions sur l'état de l'utilisateur."""
        for pattern in self.status_patterns:
            if re.search(pattern, message_content, re.IGNORECASE):
                return True

        return False

    def detect_game_question(self, message_content):
        """Détecte les questions sur le jeu actuel."""
        for pattern in self.game_question_patterns:
            if re.search(pattern, message_content, re.IGNORECASE):
                return True

        return False

    def respond_to_message(self, message_content, author_name):
        """Détermine la réponse appropriée en fonction du contenu du message."""
        if self.detect_greeting(message_content):
            return f"Salut {author_name} ! Comment ça va ?"
        elif self.detect_status_question(message_content):
            return f"Je suis juste un bot, mais je vais bien ! Merci de demander, {author_name}!"
        return None
