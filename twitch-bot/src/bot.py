from twitchio.ext import commands, routines
import config
from games import GameManager
from jokes import JokeManager
from validation import Validator
from responses import ResponseManager
from twitch_api import TwitchAPIManager
from wit_ai_manager import WitAIManager
from intent_handler import IntentHandler

class TwitchBot(commands.Bot):
    def __init__(self, token, client_id, nick, prefix, channel, wit_ai_token):
        super().__init__(token=token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=[channel])
        self.channel_name = channel
        self.game_manager = GameManager()  # Instance de gestion des jeux
        self.joke_manager = JokeManager()  # Instance de gestion des blagues
        self.validator = Validator()  # Instance de validation des choix
        self.response_manager = ResponseManager()  # Instance de gestion des réponses
        self.twitch_api_manager = TwitchAPIManager(client_id, token)  # Instance de gestion de l'API Twitch
        self.wit_ai_manager = WitAIManager(wit_ai_token)  # Instance de WitAIManager
        self.intent_handler = IntentHandler(nick)  # Instance de IntentHandler

    @commands.command(name='startgame')
    async def start_game(self, ctx):
        """Commande pour démarrer le jeu de deviner le nombre."""
        message = self.game_manager.start_number_game()
        await ctx.send(message)

    @commands.command(name='guess')
    async def guess_number(self, ctx, guess: int):
        """Commande pour deviner le nombre."""
        message = self.game_manager.guess_number(guess)
        await ctx.send(message)

    @commands.command(name='quiz')
    async def start_quiz(self, ctx):
        """Commande pour démarrer un quiz de culture générale."""
        message = self.game_manager.start_quiz()
        await ctx.send(message)

    @commands.command(name='answer')
    async def answer_quiz(self, ctx, *, answer: str):
        """Commande pour répondre à la question de quiz."""
        message = self.game_manager.answer_quiz(answer)
        await ctx.send(message)

    @commands.command(name='score')
    async def show_score(self, ctx):
        """Commande pour afficher le score actuel des joueurs."""
        message = self.game_manager.show_scores()
        await ctx.send(message)

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
            "!quiz - Démarre un quiz de culture générale.\n"
            "!answer <réponse> - Répond à la question du quiz.\n"
            "!score - Affiche les scores actuels des joueurs.\n"
            "!rps <choix> - Joue à Pierre-Papier-Ciseaux contre le bot. Choisissez parmi pierre, papier, ciseaux.\n"
            "!bet <choix> <montant> - Place un pari sur un événement.\n"
            "!help - Affiche ce message d'aide."
        )
        await ctx.send(help_message)

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
            # Utilise le ResponseManager pour gérer les réponses automatiques avec correspondance floue
            # Old code
            # response = self.response_manager.respond_to_message(message.content, message.author.name, self.nick)
            
            # Vérifier si le bot doit répondre en fonction des mentions d'utilisateur
            if self.intent_handler.should_respond(message.content):
                # Utiliser Wit.ai pour détecter l'intention du message
                intent = self.wit_ai_manager.detect_intent(message.content)
        
                # Générer une réponse en fonction de l'intention détectée
                response = self.intent_handler.handle_intent(intent, message.author.name)
            else:
                response = None

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

    bot = TwitchBot(token=token, client_id=client_id, nick=nick, prefix=prefix, channel=channel, wit_ai_token=wit_ai_token)
    bot.run()

if __name__ == "__main__":
    main()
