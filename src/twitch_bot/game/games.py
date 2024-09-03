# games.py

import random
from collections import defaultdict
from fuzzywuzzy import fuzz
from twitch_bot.game.quiz_manager import QuizManager
from twitch_bot.game.categories import QuizCategory

class GameManager:
    def __init__(self):
        self.target_number = None
        self.game_active = False
        self.quiz_manager = QuizManager()
        self.player_scores = defaultdict(int)
        self.rps_game_active = False

    def start_number_game(self):
        """Commence un nouveau jeu de deviner le nombre."""
        if not self.game_active:
            self.target_number = random.randint(1, 100)
            self.game_active = True
            return f"Jeu de devinettes lancé ! Devinez un nombre entre 1 et 100."
        return "Un jeu est déjà en cours!"

    def guess_number(self, guess, user_name):
        """Gère une supposition dans le jeu de devinettes."""
        if self.game_active:
            if guess == self.target_number:
                self.game_active = False  # Fin du jeu
                self.player_scores[user_name] += 1  # Met à jour le score de l'utilisateur
                return f"Bravo @{user_name}, tu as deviné le bon nombre {self.target_number}! Ton score est maintenant de {self.player_scores[user_name]}."
            elif guess < self.target_number:
                return f"@{user_name}, plus haut!"
            else:
                return f"@{user_name}, plus bas!"
        return "Aucun jeu en cours. Tapez !startgame pour commencer un jeu."

    def start_quiz(self, category_name='VIDEO_GAMES', difficulty='medium'):
        """Démarre un quiz avec une catégorie et une difficulté spécifiées, et renvoie un message prêt à être envoyé."""
        if self.quiz_manager.quiz_in_progress:
            return "Un quiz est déjà en cours ! Répondez à la question actuelle avant d'en démarrer un nouveau."

        try:
            category = QuizCategory[category_name.upper()]  # Convertit le nom de la catégorie en Enum
        except KeyError:
            return f"Catégorie invalide. Choisissez parmi : {[cat.name for cat in QuizCategory]}"

        if difficulty not in ['easy', 'medium', 'hard']:
            return "Difficulté invalide. Choisissez parmi 'easy', 'medium', 'hard'."

        question, options = self.quiz_manager.fetch_question(category, difficulty)
        if question:
            return f"Question: {question}\n - Options: {' | '.join(options)}"
        else:
            return "Désolé, je n'ai pas pu récupérer une question de quiz."

    def answer_quiz(self, answer, user_name):
        """Vérifie la réponse du quiz et renvoie un message prêt à être envoyé."""
        if not self.quiz_manager.quiz_in_progress:
            return f"@{user_name}, aucun quiz en cours. Utilisez la commande !quiz pour en démarrer un."

        if self.quiz_manager.check_answer(answer):
            self.player_scores[user_name] += 1  # Met à jour le score de l'utilisateur
            self.quiz_manager.reset_quiz()  # Réinitialise le quiz après une réponse correcte
            return f"Correct! Bien joué, @{user_name}! Ton score est maintenant de {self.player_scores[user_name]}."
        else:
            correct_answer = self.quiz_manager.correct_answer
            self.quiz_manager.reset_quiz()  # Réinitialise le quiz après une réponse incorrecte
            return f"@{user_name}. Incorrect. La bonne réponse était : {correct_answer}. Utilises la commande !quiz pour en démarrer un nouveau."
    
    def reset_quiz(self):
        """Réinitialise le quiz en cours et renvoie un message de confirmation."""
        if self.quiz_manager.quiz_in_progress:
            self.quiz_manager.reset_quiz()
            return "Le quiz a été réinitialisé. Utilisez la commande !quiz pour en démarrer un nouveau."
        else:
            return "Aucun quiz en cours à réinitialiser."
    
    def show_scores(self):
        """Renvoie un message avec les scores actuels des utilisateurs."""
        if not self.player_scores:
            return "Aucun score enregistré pour le moment."
        score_message = "Voici les scores:\n"
        for user, score in self.player_scores.items():
            score_message += f"@{user}: {score} points\n"
        return score_message

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
