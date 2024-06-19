from twitchio.ext import commands, routines
import twitchio.errors
import os
import auth
import json
import model
from cryptography.fernet import Fernet
import asyncio

key = os.getenv("ENCRYPT_KEY")
cipher_suite = Fernet(key)

with open('encrypted_access.bin', 'rb') as file:
        encrypted_data = file.read()
decrypted_data = cipher_suite.decrypt(encrypted_data)
token_dict = json.loads(decrypted_data.decode())

token = token_dict["access_token"]
PREFIX = "!"
CHANNEL = ["jose_gtj"]

#Configurar o bot
class Bot(commands.Bot):
    user = ""
    isLive = 0
    chan = None
    def __init__(self):
        #Inicializando o bot
        super().__init__(token = token, prefix = PREFIX, initial_channels = CHANNEL)
    
    async def event_ready(self):
        # Evento que ocorre quando o bot é ligado
        print(f'Logado como: {self.nick}')
        print(f'O id de usuário é: {self.user_id}')

    @routines.routine(seconds=60)
    async def check_stream_status():
        stream = await bot.fetch_streams(user_logins = CHANNEL)
        if stream:
            print("Nena está on")
            bot.isLive += 1
            if bot.isLive == 1:
                chan = await bot.get_channel(CHANNEL[0])
                if chan:
                    response = chat.send_message("A Nena acabou de começar a live! Dê um olá ao pessoal do chat")
                    try:
                        await chan.send(response.text)
                        print(f"Bot diz: {response.text}")
                    except genai.types.StopCandidateException as e:
                        response = chat.send_message("Você quase falou besteira! Peça desculpas imediatamente.")
                        await chan.send(response.text)
                        print(f"Failed to send message due to safety concerns: {e}")
                        print(f"Safety ratings: {e.safety_ratings}")
        else:
            print("Nena está off")
            bot.isLive == 0

    @commands.command()
    async def ask(self, ctx: commands.Context, *, message: str,) -> None:
        # Comando !ask, que será chamado quando algum usuário utilizá-lo
        if ctx.author.name == bot.user:
            # Verificando se o usuário é o mesmo da mensagem anterior
            print(f"{bot.user} (O mesmo) disse: {message}")
            response = chat.send_message(f"O mesmo usário diz: {message}")
            print(f"Bot disse: {response.text}")
        else:
            # Caso contrário, inicia um novo chat com o usuário
            bot.user = ctx.author.name
            model.start_chat(history=[])
            print(f"{bot.user} disse: {message}")
            response = chat.send_message(f"{ctx.author.name} diz: {message}")
            print(f"Bot disse: {response.text}")
        await ctx.send(response.text)

    check_stream_status.start()

bot = Bot()
try:
    # Inicia o bot
    bot.run()
except twitchio.errors.AuthenticationError as e:
    # Erro quando os tokens expiram
    auth.refresh()
    token = os.getenv("ACCESS_TOKEN")
    try:
        bot.run()
    except:
        print("Falha grave no sistema!")
    print("Falha na autenticação, tentando novo token")
    print(e)
