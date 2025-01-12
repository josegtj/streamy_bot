import random
import string

from pydantic import BaseSettings


def generate_random_string(length: int) -> string:
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


class Settings(BaseSettings):
    # Nos atributos da classe devemos utilizar os mesmos nomes das variáveis no .env
    # O resto o pydantic vai cuidar

    CLIENT_SECRET: str

    GOOGLE_API_KEY: str

    ENCRYPT_KEY: str

    CLIENT_ID: str

    CLIENT_NICK: str

    TARGET_CHANNEL: str

    SCOPE: str

    AUTH_URL: str = ""

    STATE: str = generate_random_string(16)

    REDIRECT_DOMAIN: str

    REDIRECT_PORT: int

    REDIRECT_URI: str = ""

    REDIRECT_PATH: str

    #Aqui estamos definindo de onde vão vir as variáveis de ambiente
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
"""
    Esta é uma classe que herda os atributos de BaseSettings, o objetivo dela é lidar com as variáveis de ambiente.
    Dessa forma temos uma forma mais eficiente gerenciar essas credenciais, inclusive isso abre a possibilidade de
    aceitar inclusive variáveis que sejam listas :D \n
    Também é possível definir valores padrão para as variáveis.\n
    Para utilizar essa classe basta importar ela no meio do código e acessar os atributos.
"""
settings.REDIRECT_URI = f"http://{settings.REDIRECT_DOMAIN}:{settings.REDIRECT_PORT}"
settings.AUTH_URL = f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}&scope={settings.SCOPE}&state={settings.STATE}"
