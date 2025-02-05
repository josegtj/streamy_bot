import logging
from logging import handlers

#Configurando o logger
logger = logging.getLogger("modelLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#Salvando o log em um arquivo
file_handler = handlers.RotatingFileHandler("app.log", encoding="utf-8", maxBytes=256000, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
#Exibindo o log no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
#Adicionando os manipuladores do log
logger.addHandler(file_handler)
logger.addHandler(console_handler)