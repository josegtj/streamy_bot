from twitchio.ext import commands, routines
from cryptography.fernet import Fernet
import twitchio.errors
import os
import auth
import json
import model
import time
import asyncio


key = os.getenv("ENCRYPT_KEY")
cipher_suite = Fernet(key)

with open('encrypted_access.bin', 'rb') as file:
        encrypted_data = file.read()
decrypted_data = cipher_suite.decrypt(encrypted_data)
token_dict = json.loads(decrypted_data.decode())

token = token_dict["access_token"]
PREFIX = "!"
CHANNEL = ["nenanee_"]

chat = model.create_chat()

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

    @routines.routine(seconds=60, wait_first=True)
    async def check_stream_status():
        stream = await bot.fetch_streams(user_logins = CHANNEL)
        if stream:
            print("Nena está on")
            bot.isLive += 1
            if bot.isLive == 1:
                chan = bot.get_channel(CHANNEL[0])
                if chan:
                    chat = model.create_chat()
                    response = model.send_message("A Nena acabou de começar uma live! Dê um oi ao pessoal do chat!", chat=chat)
                    await chan.send(response.text)
        else:
            print("Nena está off")
            bot.isLive == 0

    @commands.command()
    async def ask(self, ctx: commands.Context, *, message: str,) -> None:
        # Comando !ask, que será chamado quando algum usuário utilizá-lo
        global chat
        print(f"{ctx.author.name} diz: {message}")
        response = model.send_message(message,chat,ctx.author.name)
        await ctx.send(response.text)

    # check_stream_status.start()

max_retries = 3
retry_delay = 1
for attempt in range(1, max_retries + 1):
    try:
        # Inicia o bot
        print("Bot iniciando...")
        bot = Bot()
        bot.run()
    except twitchio.errors.AuthenticationError as e:
        # Erro quando os tokens expiram
        if attempt == max_retries:
            print("Número máximo de tentativas alcançado")
            break
        else:
            asyncio.run(auth.refresh())
            token = os.getenv("ACCESS_TOKEN")
            time.sleep(retry_delay)
            print("Falha na autenticação, tentando novo token")
            print(e)
