import html
import random
import requests
from fuzzywuzzy import fuzz
from twitch_bot.game.categories import QuizCategory

class QuizManager:
    def __init__(self):
        self.api_url = "https://opentdb.com/api.php"
        self.current_question = None
        self.correct_answer = None
        self.quiz_in_progress = False  # Indicateur d'état pour savoir si un quiz est en cours

    def fetch_question(self, category=QuizCategory.VIDEO_GAMES, difficulty='medium', qtype='multiple'):
        """Récupère une nouvelle question de l'Open Trivia Database dans la catégorie spécifiée."""
        if self.quiz_in_progress:
            return None, None  # Retourne None si un quiz est déjà en cours

        params = {
            'amount': 1,
            'category': category.value,
            'difficulty': difficulty,
            'type': qtype
        }
        response = requests.get(self.api_url, params=params)
        data = response.json()

        if data['response_code'] == 0:  # Succès
            question_data = data['results'][0]
            self.current_question = html.unescape(question_data['question'])  # Décoder les entités HTML
            correct_answer  = html.unescape(question_data['correct_answer'])  # Décoder les entités HTML
            incorrect_answers = [html.unescape(ans) for ans in question_data['incorrect_answers']]  # Décoder les entités HTML

            # Combine la réponse correcte et les réponses incorrectes dans une liste unique
            options = incorrect_answers + [correct_answer]

            # Mélange la liste pour positionner la réponse correcte de manière aléatoire
            random.shuffle(options)
            
            self.quiz_in_progress = True  # Indique qu'un quiz est maintenant en cours
            return self.current_question, options
        else:
            return None, None

    def check_answer(self, answer, threshold=80):
        """
        Vérifie si la réponse fournie est correcte, en tolérant certaines erreurs d'orthographe.
        Utilise une correspondance floue pour comparer la réponse à la réponse correcte.
        """
        similarity = fuzz.ratio(answer.strip().lower(), self.correct_answer.strip().lower())
        if similarity >= threshold:
            self.quiz_in_progress = False  # Réinitialise l'état une fois le quiz terminé
            return True
        return False

    def reset_quiz(self):
        """Réinitialise l'état du quiz pour permettre de démarrer un nouveau quiz."""
        self.quiz_in_progress = False
        self.current_question = None
        self.correct_answer = None
