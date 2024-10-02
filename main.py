from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent, InvalidTokenException
from twitchAPI.chat import Chat, EventData, ChatCommand
from twitchAPI.chat.middleware import ChannelCommandCooldown
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import StreamOnlineEvent, ChannelUpdateEvent
from twitchAPI.helper import first
import auth, model, json, os, asyncio
from cryptography.fernet import Fernet

APP_ID = 'koyw45naylibn6z1p8rajnjo1rxgv6'
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
chat_model = model.create_chat()
TARGET_CHANNEL = "jose_gtj"
is_live = False

key = os.getenv("ENCRYPT_KEY")
cipher_suite = Fernet(key)

async def on_ready(cmd: EventData):
    global is_live
    await cmd.chat.join_room(TARGET_CHANNEL)
    print("Bot está operante...")
    while is_live == False:
        continue
    else:
        response = model.send_message("A Live acabou de começar, dê um olá ao pessoal do chat!", chat_model)
        await cmd.chat.send_message(TARGET_CHANNEL, "Teste")

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

async def on_stream_online(data: ChannelUpdateEvent):
    global is_live
    is_live = True
    print(TARGET_CHANNEL + " está ao vivo!")

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

    # registrando o comando ask
    chat.register_command('ask', ask_command, command_middleware=[ChannelCommandCooldown(10,
                                                execute_blocked_handler=handle_blocked_user)])
    
    chat.register_event(ChatEvent.READY, on_ready)
    chat.start()
    
    channel = await first(twitch.get_users(logins=TARGET_CHANNEL))
    
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()

    await eventsub.listen_stream_online(channel.id, on_stream_online)

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\n')
    except KeyboardInterrupt:
        pass
    finally:
        # now we can close the chat bot and the twitch api client
        await eventsub.stop()
        chat.stop()
        await twitch.close()

asyncio.run(run())