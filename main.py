from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent, InvalidTokenException
from twitchAPI.chat import Chat, EventData, ChatCommand, ChatMessage
from twitchAPI.chat.middleware import ChannelCommandCooldown
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import StreamOnlineEvent
from twitchAPI.helper import first
from danilo.core.settings import settings
import auth, model, json, asyncio
from cryptography.fernet import Fernet

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
chat_model = model.create_chat()
chat = None
headless = False

cipher_suite = Fernet(settings.ENCRYPT_KEY)

async def on_ready(cmd: EventData):
    await cmd.chat.join_room(settings.TARGET_CHANNEL)
    print("Bot está operante...")

# this will be called whenever the !ask command is issued
async def ask_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('Você precisa dizer algo ao bot')
    else:
        global chat_model
        response = model.send_message(cmd.parameter, chat_model, cmd.user.name)
        await cmd.reply(response.text)

# respondendo à mensagens direcionadas ao bot
async def responder_reply(msg: ChatMessage):
    global chat_model
    if msg.reply_parent_user_login == settings.CLIENT_NICK:
        response = model.send_message(msg.text, chat_model, msg.user.name, isReply=True, msgAnterior=msg.reply_parent_msg_body.replace("\\s", " "))
        await msg.reply(response.text)
    elif settings.CLIENT_NICK in msg.text.lower():
        response = model.send_message(msg.text, chat_model, msg.user.name)
        await msg.reply(response.text)

async def handle_blocked_user(cmd: ChatCommand):
    await cmd.reply("/me Comando em cooldown...")

async def on_stream_online(data: StreamOnlineEvent):
    global chat, chat_model
    print(settings.TARGET_CHANNEL + " está ao vivo!")
    response = model.send_message("A live acabou de começar, dê um oi pro pessoal", chat_model)
    await chat.send_message(settings.TARGET_CHANNEL, response.text)

# this is where we set up the bot
async def run():
    global chat
    # set up twitch api instance and call auth function in auth.py to get tokens
    twitch = await Twitch(settings.CLIENT_ID, authenticate_app=False)
    twitch.auto_refresh_auth = False
    max_retries = 3
    delay = 3
    for attempt in range(1, max_retries + 1):
        try:
            await asyncio.sleep(delay)
            with open('encrypted_access.bin', 'rb') as file:
                    encrypted_data = file.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            token_dict = json.loads(decrypted_data.decode())
            print("Autenticando...")
            await twitch.set_user_authentication(token_dict["access_token"], USER_SCOPE)
            break

        except FileNotFoundError as e:
            await auth.auth(headless)

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
    
    # registrando o bot para detectar mensagens direcionadas à ele, ou quando a live começar
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, responder_reply)

    chat.start()

    channel = await first(twitch.get_users(logins=settings.TARGET_CHANNEL))
    
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