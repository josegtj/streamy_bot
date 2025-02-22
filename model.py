import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.api_core.exceptions
from core.settings import settings
import time
from log import logger

#Criar o modelo de IA
genai.configure(api_key=settings.GOOGLE_API_KEY)
#Arquivo contendo as características do modelo
context = open("file_context.txt", "r", encoding="UTF-8")
#Escolhendo o modelo utilizado, passando o contexto e as opções de segurança
model = genai.GenerativeModel('gemini-2.0-flash-exp', system_instruction=context, 
                              safety_settings= {HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_ONLY_HIGH,
						HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_ONLY_HIGH,})

def create_chat():
    chat = model.start_chat(history=[])
    return chat

#Criando o chat e mandando a mensagem
def send_message(message:str, chat, author:str="", isReply:bool=False, msgAnterior:str=""):
    max_retries = 3
    retry_delay = 1
    for attempt in range(1, max_retries + 1):
        try:
            if isReply:
                print(msgAnterior)
                response = chat.send_message(f"Em resposta à sua mensagem anterior, que dizia {msgAnterior}, {author} diz: {message}")
            else:
                response = chat.send_message(f"{author} diz: {message}")
        except google.api_core.exceptions.InternalServerError as e:
            if attempt == max_retries:
                logger.critical("Número máximo de tentativas alcançado")
                response = {"text":"Peço perdão pelo transtorno, mas parece que o meu cérebro deu uma fritada! Tente novamente em alguns minutos."}
                return response
            else:
                logger.error(e)
                logger.info(f"Erro interno do sistema Google, tentando novamente em {retry_delay} segundos")
                time.sleep(retry_delay)
        except genai.types.StopCandidateException as e:
            logger.error(e)
            logger.info("Erro nos filtros de segurança, reformulando mensagem.")
            response = chat.send_message(f"Você quase disse algo inapropriado! Reformule a sua resposta à {author}, que dizia: {message}")
            return response
        else:
            return response

