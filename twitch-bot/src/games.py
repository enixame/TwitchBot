# src/games.py

import random
from fuzzywuzzy import fuzz

class GameManager:
    def __init__(self):
        self.target_number = None
        self.game_active = False
        self.quiz_active = False
        self.quiz_question = None
        self.quiz_answer = None
        self.player_scores = {}
        self.rps_game_active = False

    def start_number_game(self):
        """Commence un nouveau jeu de deviner le nombre."""
        if not self.game_active:
            self.target_number = random.randint(1, 100)
            self.game_active = True
            return f"Jeu de devinettes lancé ! Devinez un nombre entre 1 et 100."
        return "Un jeu est déjà en cours!"

    def guess_number(self, guess):
        """Gère une supposition dans le jeu de devinettes."""
        if self.game_active:
            if guess == self.target_number:
                self.game_active = False  # Fin du jeu
                return f"Bravo, tu as deviné le bon nombre {self.target_number}!"
            elif guess < self.target_number:
                return "Plus haut!"
            else:
                return "Plus bas!"
        return "Aucun jeu en cours. Tapez !startgame pour commencer un jeu."

    def start_quiz(self):
        """Commence un nouveau quiz de culture générale."""
        if not self.quiz_active:
            questions = [
                ("Quel est le plus grand océan du monde ?", "Pacifique"),
                ("Combien de couleurs y a-t-il dans un arc-en-ciel ?", "7"),
                ("Qui a peint la Joconde ?", "Leonard de Vinci"),
            ]
            self.quiz_question, self.quiz_answer = random.choice(questions)
            self.quiz_active = True
            return f"Quiz commencé ! Question : {self.quiz_question}"
        return "Un quiz est déjà en cours!"

    def answer_quiz(self, answer):
        """Gère une réponse dans le quiz en utilisant la validation floue."""
        if self.quiz_active:
            if fuzz.ratio(answer.lower(), self.quiz_answer.lower()) > 80:  # Utilise `fuzz` pour la correspondance floue
                self.quiz_active = False
                return f"Bonne réponse! La réponse était bien '{self.quiz_answer}'."
            else:
                return "Mauvaise réponse! Essayez encore."
        return "Aucun quiz en cours. Tapez !quiz pour commencer un quiz."

    def show_scores(self):
        """Affiche les scores actuels des joueurs."""
        scores = "\n".join([f"{player}: {score}" for player, score in self.player_scores.items()])
        return f"Scores actuels:\n{scores}" if scores else "Aucun score enregistré pour le moment."

    def play_rps(self, choice):
        """Joue à Pierre-Papier-Ciseaux."""
        valid_choices = ['pierre', 'papier', 'ciseaux']
        best_match = self.get_best_match(choice, valid_choices)
        if best_match:
            bot_choice = random.choice(valid_choices)
            result = self.determine_rps_winner(best_match, bot_choice)
            return f"Tu as choisi {best_match}. J'ai choisi {bot_choice}. {result}"
        else:
            return f"Choix invalide. Choisissez parmi {', '.join(valid_choices)}."

    def determine_rps_winner(self, player_choice, bot_choice):
        """Détermine le gagnant de Pierre-Papier-Ciseaux."""
        outcomes = {
            ('pierre', 'ciseaux'): "Tu gagnes!",
            ('ciseaux', 'papier'): "Tu gagnes!",
            ('papier', 'pierre'): "Tu gagnes!",
            ('ciseaux', 'pierre'): "Je gagne!",
            ('papier', 'ciseaux'): "Je gagne!",
            ('pierre', 'papier'): "Je gagne!",
        }
        if player_choice == bot_choice:
            return "C'est un match nul!"
        else:
            return outcomes.get((player_choice, bot_choice), "Je gagne!")

    def get_best_match(self, user_input, valid_choices):
        """Trouve la meilleure correspondance pour l'entrée utilisateur parmi les choix valides."""
        best_match = None
        highest_ratio = 0
        for choice in valid_choices:
            ratio = fuzz.ratio(user_input.lower(), choice)
            if ratio > highest_ratio and ratio > 80:  # Seuil de 80 pour accepter la réponse
                highest_ratio = ratio
                best_match = choice
        return best_match
