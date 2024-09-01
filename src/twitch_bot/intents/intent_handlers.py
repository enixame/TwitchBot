# intent_handlers.py

def handle_greetings(author_name):
    return f"Salut {author_name} ! Comment ça va ?"

def handle_status(author_name):
    return f"Je suis juste un bot, mais je vais bien ! Merci de demander, {author_name}!"

def handle_identity(author_name):
    print(f'Message ignoré de {author_name}')
    return None  # Renvoie None pour indiquer qu'il n'y a pas de réponse à envoyer

def handle_game(author_name):
    return f"C'est écrit dans le titre, {author_name}!"

def handle_bad(author_name):
    return f"C'est ton avis, {author_name}. Mais honnêtement, je m'en fiche!"
