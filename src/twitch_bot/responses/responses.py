# responses.py
# old version

from twitch_bot.validation.validation import Validator

class ResponseManager:
    def __init__(self):
        self.validator = Validator()  # Instance de Validator pour la correspondance floue

        # Mise à jour des motifs de salutation et des questions communes
        self.greeting_patterns = [
            'salut', 'bonjour', 'bonsoir', 'hey', 'coucou', 'hello', 'hi',
            'yo', 'wesh', 'yop', 'hé', 'bien le bonjour', 'hello there', 'bienvenue',
            'allo', 'holà', 'tiens', 'quoi de neuf', 'ça va', 'salutations', 'comment ça va'
        ]
        self.status_patterns = [
            'comment ça va', 'ça va', 'comment vas-tu', 'la forme', 'comment te sens-tu', 
            'bien et toi', 'ça roule', 'ça boume', 'tu vas bien', 'bien ou quoi', 
            'comment allez-vous', 'vous allez bien', 'tout va bien', 'vous allez bien ?', 
            'tu vas bien ?', 'ça va bien ?', 'ça va pas ?', 'tu vas comment', 
            'tout va bien ?', 'ça va comment', 'ça gaze', 'en forme', 'en forme ?'
        ]
        self.game_question_patterns = [
            'quel est le jeu', 'c\'est quoi le jeu', 'jeu actuel',
            'quel jeu', 'à quel jeu joues-tu', 'quel est ce jeu', 'à quoi tu joues'
        ]

    def detect_greeting(self, message_content):
        """Détecte les salutations dans le message en utilisant la correspondance floue."""
        return self.validator.fuzzy_match(message_content, self.greeting_patterns)

    def detect_status_question(self, message_content):
        """Détecte les questions sur l'état de l'utilisateur en utilisant la correspondance floue."""
        return self.validator.fuzzy_match(message_content, self.status_patterns)

    def detect_game_question(self, message_content):
        """Détecte les questions sur le jeu actuel en utilisant la correspondance floue."""
        return self.validator.fuzzy_match(message_content, self.game_question_patterns)

    def respond_to_message(self, message_content, author_name, bot_name):
        """Détermine la réponse appropriée en fonction du contenu du message."""
        # Vérifier si le message mentionne un autre utilisateur
        if "@" in message_content:
            # Vérifier si le bot est mentionné
            if f"@{bot_name.lower()}" not in message_content.lower():
                return None  # Ne pas répondre si le bot n'est pas mentionné

        # Vérifier les différents types de messages et répondre en conséquence
        if self.detect_greeting(message_content):
            return f"Salut {author_name} ! Comment ça va ?"
        elif self.detect_status_question(message_content):
            return f"Je suis juste un bot, mais je vais bien ! Merci de demander, {author_name}!"
        elif self.detect_game_question(message_content):
            return "Vous voulez savoir quel est le jeu actuel ? Utilisez la commande !game."
        
        return None
