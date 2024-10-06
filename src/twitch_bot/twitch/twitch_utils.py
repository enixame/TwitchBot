# src/twitch_bot/twitch/twutch_utils.py

def split_message(text, max_length=500):
    """Divise un texte en plusieurs morceaux de maximum 500 caractères sans couper les mots"""
    words = text.split()  # Divise le texte en mots
    messages = []
    current_message = ""

    for word in words:
        # Si l'ajout du mot dépasse la longueur maximale, on ajoute le message actuel et on recommence un nouveau
        if len(current_message) + len(word) + 1 > max_length:  # +1 pour l'espace
            messages.append(current_message)  # Ajoute la ligne complète
            current_message = word  # Démarre un nouveau message avec le mot actuel
        else:
            # Ajoute le mot à la ligne actuelle
            if current_message:
                current_message += " " + word
            else:
                current_message = word

    # Ajouter le dernier message s'il existe
    if current_message:
        messages.append(current_message)
    
    return messages