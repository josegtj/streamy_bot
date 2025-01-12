# Streamy
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-886FBF?style=for-the-badge&logo=googlegemini&logoColor=fff)

Chatbot [TwitchAPI](https://github.com/Teekeks/pyTwitchAPI) do canal da NenaNee_ que utiliza a API do [Gemini](https://ai.google.dev/gemini-api/docs?hl=pt-br) para responder perguntas dos viewers.

## Tutorial

Defina o canal da Twitch em que o bot estará ativo mudando a variável **TARGET_CHANNEL** em main.py
https://github.com/josegtj/streamy_bot/blob/19239ac276eaea317da44a3b567ba8cab669c202/main.py#L13

Edite o arquivo file_context.txt, dando as instruções de como o Chatbot deve se comportar.

As dependências estão listadas em requirements.txt
```
pip install -r requirements.txt
```

Para funcionar, o bot precisa que 3 variáveis de ambiente sejam definidas:
- **CLIENT_SECRET** (Obtida a partir da criação de um [App](https://dev.twitch.tv/console/apps) na Twitch)
- **GOOGLE_API_KEY** ([Chave da API do Google](https://aistudio.google.com/apikey))
- **ENCRYPT_KEY** (Chave que você deve gerar aleatoriamente - como uma senha - para descriptografar o Token de Acesso)

Você pode definir as variáveis no próprio Windows, criando um ambiente virtual Python, ou utilizando Docker.
