# Streamy
Chatbot [TwitchAPI](https://github.com/Teekeks/pyTwitchAPI) do canal da NenaNee_ que utiliza a API do [Gemini](https://ai.google.dev/gemini-api/docs?hl=pt-br) para responder perguntas dos viewers.

## Tutorial
As dependências estão listadas em requirements.txt
```
pip install -r requirementes.txt
```

Para funcionar, o bot precisa que 3 variáveis de ambiente sejam definidas:
- **CLIENT_SECRET** (Obtida a partir da criação de um [App](https://dev.twitch.tv/console/apps) na Twitch)
- **GOOGLE_API_KEY** ([Chave da API do Google](https://aistudio.google.com/apikey))
- **ENCRYPT_KEY** (Chave que você deve gerar aleatoriamente - como uma senha - para descriptografar o Token de Acesso)

Você pode definir as variáveis no próprio Windows, criando um ambiente virtual Python, ou utilizando Docker.
