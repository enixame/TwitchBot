from twitchio.ext import commands, routines
from twitch_bot.config import config
from twitch_bot.game.games import GameManager
from twitch_bot.jokes.jokes import JokeManager
from twitch_bot.validation.validation import Validator
from twitch_bot.responses.responses import ResponseManager
from twitch_bot.twitch.twitch_api import TwitchAPIManager
from twitch_bot.detectors.wit_ai_manager import WitAIManager
from twitch_bot.intents.intent_handler import IntentHandler
from twitch_bot.intents.intent_detector import IntentDetector
from twitch_bot.intents.intent_handlers import handle_greetings, handle_status, handle_nothing, handle_congrats, handle_ask, handle_bad, handle_backseat

class TwitchBot(commands.Bot):
    def __init__(self, token, client_id, nick, prefix, channel, intent_detector: IntentDetector):
        super().__init__(token=token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=[channel])
        self.channel_name = channel
        self.game_manager = GameManager()  # Instance de gestion des jeux
        self.joke_manager = JokeManager()  # Instance de gestion des blagues
        self.validator = Validator()  # Instance de validation des choix
        self.response_manager = ResponseManager()  # Instance de gestion des réponses
        self.twitch_api_manager = TwitchAPIManager(client_id, token)  # Instance de gestion de l'API Twitch
        
        # Définir le gestionnaire d'intentions avec les fonctions de rappel
        intent_handlers = {
            'greetings': handle_greetings,
            'health_status': handle_status,
            'bad': handle_bad,
            'backseat': handle_backseat,
            'ask': handle_ask,
            'congrats': handle_congrats,
            'common_confirmation': handle_nothing,
            'common': handle_nothing

            # Ajoute d'autres intentions et leurs gestionnaires ici
        }

        self.intent_handler = IntentHandler(nick, intent_handlers)  # Instance de IntentHandler avec callbacks
        self.intent_detector = intent_detector  # Instance de IntentDetector (flexible)

    @commands.command(name='startgame')
    async def start_game(self, ctx):
        """Commande pour démarrer le jeu de deviner le nombre."""
        message = self.game_manager.start_number_game()
        await ctx.send(message)

    @commands.command(name='guess')
    async def guess_number(self, ctx, guess: int):
        """Commande pour deviner le nombre."""
        user_name = ctx.author.name  # Récupère le nom de l'utilisateur qui a envoyé la commande
        message = self.game_manager.guess_number(guess, user_name)
        await ctx.send(message)

    @commands.command(name='quiz')
    async def start_quiz(self, ctx, difficulty: str = 'medium'):
        """Commande pour démarrer un quiz avec une difficulté optionnelle."""
        message = self.game_manager.start_quiz(difficulty=difficulty)
        await ctx.send(message)

    @commands.command(name='answer')
    async def answer_quiz(self, ctx, *, answer: str):
        """Commande pour répondre à la question de quiz."""
        user_name = ctx.author.name  # Récupère le nom de l'utilisateur qui a envoyé la commande
        message = self.game_manager.answer_quiz(answer, user_name)
        await ctx.send(message)
    
    @commands.command(name='resetquiz')
    async def reset_quiz_command(self, ctx):
        """Commande pour réinitialiser le quiz actuel."""
        message = self.game_manager.reset_quiz()  # Appelle reset_quiz et obtient le message à envoyer
        await ctx.send(message)

    @commands.command(name='score')
    async def show_score(self, ctx):
        """Commande pour afficher le score actuel des joueurs."""
        message = self.game_manager.show_scores()
        # Sépare le message en lignes et envoie chaque ligne séparément
        for line in message.split('\n'):
            await ctx.send(line)

    @commands.command(name='rps')
    async def play_rps(self, ctx, choice: str):
        """Commande pour jouer à Pierre-Papier-Ciseaux."""
        valid_choices = ['pierre', 'papier', 'ciseaux']
        user_choice = self.validator.validate_choice(choice, valid_choices)
        if user_choice is None:
            await ctx.send(f"Choix invalide. Choisissez parmi {', '.join(valid_choices)}.")
            return

        message = self.game_manager.play_rps(user_choice)
        await ctx.send(message)

    @commands.command(name='bet')
    async def place_bet(self, ctx, choice: str, amount: int):
        """Commande pour placer un pari."""
        await ctx.send(f"{ctx.author.name} a placé un pari de {amount} points sur {choice}!")

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Commande pour afficher la liste des commandes disponibles."""
        help_message = (
            "!startgame - Commence un nouveau jeu pour deviner le nombre.\n"
            "!guess <nombre> - Devine le nombre pour le jeu en cours.\n"
            "!quiz <difficulté> - Démarre un quiz de culture générale. Choisissez parmi easy, medium, hard (par défaut: medium).\n"
            "!resetquiz - Réinitialise le quiz actuel \n"
            "!answer <réponse> - Répond à la question du quiz.\n"
            "!score - Affiche les scores actuels des joueurs.\n"
            "!rps <choix> - Joue à Pierre-Papier-Ciseaux contre le bot. Choisissez parmi pierre, papier, ciseaux.\n"
            "!bet <choix> <montant> - Place un pari sur un événement.\n"
            "!help - Affiche ce message d'aide."
        )
        # Sépare le message en lignes et envoie chaque ligne séparément
        for line in help_message.split('\n'):
            await ctx.send(line)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.joke_task.start()

    async def event_message(self, message):
        if message.author is None or message.author.name is None:
            return

        if message.author.name.lower() == self.nick.lower():
            return

        ctx = await self.get_context(message)

        # Vérifie si le message est une commande
        if ctx.command:
            await self.handle_commands(message)
        else:
            # Vérifier si le bot doit répondre en fonction des mentions d'utilisateur
            if self.intent_handler.should_respond(message.content):
                # Utiliser le détecteur d'intention pour détecter l'intention du message
                intent = self.intent_detector.detect_intent(message.content)
        
                # Générer une réponse en fonction de l'intention détectée
                response = self.intent_handler.handle_intent(intent, message.author.name)
                
                # Si une réponse est trouvée, l'envoyer
                if response:
                    await message.channel.send(response)
                elif self.response_manager.detect_game_question(message.content):
                    game_name = self.twitch_api_manager.get_current_game(self.channel_name)
                    await message.channel.send(f"Le jeu actuel est {game_name}." if game_name else "Je ne peux pas déterminer le jeu actuel.")

    @routines.routine(minutes=20)
    async def joke_task(self):
        joke = self.joke_manager.get_joke()
        channel = self.get_channel(self.channel_name)
        if channel:
            await channel.send(joke)

def main():
    """Fonction principale pour démarrer le bot Twitch."""
    token = config.OAUTH_TOKEN
    client_id = config.CLIENT_ID
    nick = config.BOT_NAME
    prefix = '!'
    channel = config.CHANNEL_NAME
    wit_ai_token = config.WIT_AI_TOKEN
    # Choisir le détecteur d'intention (WitAI par défaut)
    intent_detector = WitAIManager(wit_ai_token)
    # Si tu veux utiliser OpenAI, par exemple :
    # openai_api_key = config.OPENAI_API_KEY
    # intent_detector = OpenAIIntentDetector(openai_api_key)

    bot = TwitchBot(token=token, client_id=client_id, nick=nick, prefix=prefix, channel=channel, intent_detector=intent_detector)
    bot.run()

if __name__ == "__main__":
    main()
