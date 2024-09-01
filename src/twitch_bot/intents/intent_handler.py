# intent_handler.py

class IntentHandler:
    def __init__(self, bot_name, intent_handlers=None):
        self.bot_name = bot_name.lower()
        # Utilise les gestionnaires d'intention fournis par l'utilisateur ou des valeurs par défaut
        self.intent_handlers = intent_handlers or {}

    def should_respond(self, message_content):
        """Détecte si le bot doit répondre, en fonction des mentions d'utilisateur dans le message."""
        if "@" in message_content:
            if f"@{self.bot_name}" not in message_content.lower():
                return False  # Ne pas répondre si le bot n'est pas mentionné
        return True

    def handle_intent(self, intent, message_author):
        """Génère une réponse en fonction de l'intention détectée et des gestionnaires d'intention fournis."""
        if intent in self.intent_handlers:
            # Utiliser le gestionnaire d'intention spécifique fourni par l'utilisateur
            return self.intent_handlers[intent](message_author)
        else:
            # Optionnel : fournir un comportement par défaut si l'intention n'est pas reconnue
            return f"Désolé, je ne comprends pas l'intention '{intent}'." if intent else None
