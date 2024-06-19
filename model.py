import google.generativeai as genai
import os

#Criar o modelo de IA
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#Arquivo contendo as características do modelo
context = open("file_context.txt", "r", encoding="UTF-8")
#Escolhendo o modelo utilizado, passando o contexto e as opções de segurança
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=context, 
                              safety_settings= {genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                                                genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH})
#Criando um novo chat com a IA
def create_chat(history:list=[]):
    chat = model.start_chat(history=history)
    return chat

def send_message(message:str, author:str=""):
    chat = create_chat()
    response = chat.send_message(f"{author} diz: {message}")
    if message._done == True:
        return response
    else:
        

message = send_message("Olá bot")
if message._done == True:
    print(message.text)
else:
    print("Erro no envio da mensagem")