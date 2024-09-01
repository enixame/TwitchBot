# src/validation

from fuzzywuzzy import fuzz

class Validator:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def validate_choice(self, user_input, valid_choices):
        """Valide l'entrée de l'utilisateur en utilisant la correspondance floue."""
        for choice in valid_choices:
            if fuzz.ratio(user_input.lower(), choice) > self.threshold:
                return choice
        return None
