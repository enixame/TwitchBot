# intent_handlers.py

def handle_greetings(author_name):
    return f"Salut {author_name} ! Comment ça va ?"

def handle_status(author_name):
    return f"Je suis juste un bot, mais je vais bien ! Merci de demander, {author_name}!"

def handle_nothing(author_name):
    print(f'Message ignoré de {author_name}')
    return None  # Renvoie None pour indiquer qu'il n'y a pas de réponse à envoyer

def handle_ask(author_name):
    return f"C'est une question pour the_last_engineer, {author_name}. N'hésites pas à utiliser les commandes pour le réveiller."

def handle_congrats(author_name):
    return f"Merci à toi, {author_name}!"

def handle_bad(author_name):
    return f"C'est ton avis, {author_name}. Mais honnêtement, je m'en fiche!"

def handle_backseat(author_name):
    return f"Il ne faut pas hésiter à aider the_last_engineer, {author_name}. Le backseat est autorisé mais n'abuse pas."
