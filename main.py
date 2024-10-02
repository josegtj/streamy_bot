from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent, InvalidTokenException
from twitchAPI.chat import Chat, EventData, ChatCommand
from twitchAPI.chat.middleware import ChannelUserCommandCooldown
import auth, model, json, os, asyncio
from cryptography.fernet import Fernet

APP_ID = 'koyw45naylibn6z1p8rajnjo1rxgv6'
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = 'jose_gtj'
chat_model = model.create_chat()

key = os.getenv("ENCRYPT_KEY")
cipher_suite = Fernet(key)

# Função chamada quando o bot está pronto
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here
    # Inicializando o chat com o modelo de IA


# this will be called whenever the !ask command is issued
async def ask_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('Você precisa dizer algo ao bot')
    else:
        global chat_model
        response = model.send_message(cmd.parameter, chat_model, cmd.user.name)
        await cmd.reply(response.text)

async def handle_blocked_user(cmd: ChatCommand):
    await cmd.reply("/me Comando em cooldown...")

# this is where we set up the bot
async def run():
    # set up twitch api instance and call auth function in auth.py to get tokens
    twitch = await Twitch(APP_ID, authenticate_app=False)
    twitch.auto_refresh_auth = False
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open('encrypted_access.bin', 'rb') as file:
                    encrypted_data = file.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            token_dict = json.loads(decrypted_data.decode())
            print("Autenticando...")
            await twitch.set_user_authentication(token_dict["access_token"], USER_SCOPE)
            break
        
        except InvalidTokenException as e:
            if attempt == max_retries:
                print("Falha ao gerar um novo token, fechando o programa.")
                await twitch.close()
                break
            else:
                print("Token inválido! Gerando um token novo...")
                await auth.refresh()      

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)

    # registrando o comando ask
    chat.register_command('ask', ask_command, command_middleware=[ChannelUserCommandCooldown(10,
                                                execute_blocked_handler=handle_blocked_user)])

    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()

# lets run our setup
asyncio.run(run())