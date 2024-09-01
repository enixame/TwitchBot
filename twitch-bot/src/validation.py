# src/validation.py

from fuzzywuzzy import fuzz

class Validator:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def validate_choice(self, user_input, valid_choices):
        """Valide l'entrée de l'utilisateur en utilisant la correspondance floue."""
        for choice in valid_choices:
            if fuzz.partial_ratio(user_input.lower(), choice.lower()) > self.threshold:
                return choice
        return None

    def fuzzy_match(self, user_input, patterns):
        """Utilise la correspondance floue pour vérifier si l'entrée correspond à un des patterns."""
        for pattern in patterns:
            if fuzz.partial_ratio(user_input.lower(), pattern.lower()) > self.threshold:
                return True
        return False
