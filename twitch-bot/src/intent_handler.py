# src/intent_handler

class IntentHandler:
    def __init__(self, bot_name):
        self.bot_name = bot_name.lower()

    def should_respond(self, message_content):
        """Détecte si le bot doit répondre, en fonction des mentions d'utilisateur dans le message."""
        if "@" in message_content:
            if f"@{self.bot_name}" not in message_content.lower():
                return False  # Ne pas répondre si le bot n'est pas mentionné
        return True

    def handle_intent(self, intent, message_author):
        """Génère une réponse en fonction de l'intention détectée."""
        if intent == 'greetings':
            return f"Salut {message_author} ! Comment ça va ?"
        elif intent == 'status':
            return f"Je suis juste un bot, mais je vais bien ! Merci de demander, {message_author}!"
        else:
            return None
