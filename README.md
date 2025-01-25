# Streamy
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-886FBF?style=for-the-badge&logo=googlegemini&logoColor=fff)

Chatbot [TwitchAPI](https://github.com/Teekeks/pyTwitchAPI) do canal da NenaNee_ que utiliza a API do [Gemini](https://ai.google.dev/gemini-api/docs?hl=pt-br) para responder perguntas dos viewers.

## Tutorial
### Twitch

1. Em primeiro lugar, você vai precisar criar uma conta nova na Twitch para o bot. Teoricamente, você pode usar sua própria conta, mas por motivos de segurança, evitando um potencial ban, recomendo que crie uma conta nova.

2. [Crie um aplicativo](https://dev.twitch.tv/console/apps)

3. Dê um nome próprio ao aplicativo. Mantenha o URL de direcionamento padrão (http://localhost:3000). Copie os valores de **ID do cliente** e gere um **Segredo de cliente**. Guarde-os por enquanto

### Gemini

4. Utilizando sua conta do Google, vá para https://aistudio.google.com/apikey e crie uma **chave de API**

### Configurando variáveis

5. Clone o repositório e crie um arquivo ".env" na pasta raíz do bot, nesse arquivo, deverão ser definidas as variáveis no formato VARIAVEL="exemplo"

    Será necessário definir:
 - CLIENT_SECRET - Segredo de cliente gerado no passo 3
 - CLIENT_ID - ID do cliente obtido no passo 3
 - CLIENT_NICK - Username da conta que vc usou para criar o aplicativo no passo 2
 - TARGET_CHANNEL - Username do canal ao qual o bot deve se conectar e resopnder perguntas
 - GOOGLE_API_KEY - Chave de API do Google obtida no passo 4
 - ENCRYPT_KEY - Chave que será usada para encriptar o token de acesso. Você pode interpretá-la como uma senha, que você pode definir ou gerar aleatóriamente
 - SCOPE="chat:read+chat:edit"
 - REDIRECT_DOMAIN="localhost"
 - REDIRECT_PORT=3000

6. Edite o arquivo file_context.txt, dando as instruções de como o Chatbot deve se comportar

7. Instale as dependências que estão listadas em requirements.txt
```
pip install -r requirements.txt
```
8. Rode o script https://github.com/josegtj/streamy_bot/blob/0351bda2bfb5896ddb520937bc6a00d2bb3f54bf/main.py através do Python
```
python3 main.py
```