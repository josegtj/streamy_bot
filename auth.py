import requests
import json
from cryptography.fernet import Fernet
from threading import Thread
from urllib.parse import urlparse, parse_qs, quote
from http.server import SimpleHTTPRequestHandler, HTTPServer
from core.settings import settings

code = None

cipher_suite = Fernet(settings.ENCRYPT_KEY)

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global code
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get('code', [None])[0]
        state = query_components.get('state', [None])[0]

        if code:
            if state != settings.STATE:
                print("Erro no código de confirmação!")
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('Autenticado! Pode fechar a página \n Código de autenticação: '.encode("ISO-8859-1") + code)
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Falha na autenticação'.encode("ISO-8859-1"))

        def stop_server():
            global httpd
            httpd.shutdown()

        Thread(target=stop_server).start()

def run_server():
    global code
    global httpd
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Running server on port 3000...')
    httpd.serve_forever()
    def stop_server():
        httpd.shutdown()
    server_thread = Thread(target=stop_server)
    server_thread.start()
        

def get_code(headless:bool):
    global code
    if headless == True:
        print(f"Cole o link no seu navegador, depois cole o código aqui\n{settings.AUTH_URL}")
        while code == None:
            code = input("Código: ")
        else:
            return code
    else:
        print(f"Autenticação necessária: {settings.AUTH_URL}")
        server_thread = Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        server_thread.join()
        while code == None:
            continue
        else:
            return code
    
async def auth(headless:bool):
    code = get_code(headless)
    base_url = "https://id.twitch.tv/oauth2/token"
    grant_type = "authorization_code"
    data = {
        "client_id":settings.CLIENT_ID,
        "client_secret":settings.CLIENT_SECRET,
        "code":code,
        "grant_type":grant_type,
        "redirect_uri":settings.REDIRECT_URI
    }
    request = requests.post(base_url, json=data).json()
    dict_str = json.dumps(request)
    encrypted_data = cipher_suite.encrypt(dict_str.encode())
    with open('encrypted_access.bin', 'wb') as file:
        file.write(encrypted_data)
    print("Novo token de acesso gerado!")

async def refresh():
    with open('encrypted_access.bin', 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    token_dict = json.loads(decrypted_data.decode())
    base_url = "https://id.twitch.tv/oauth2/token"
    grant_type = "refresh_token"
    data = {
        "client_id":settings.CLIENT_ID,
        "client_secret":settings.CLIENT_SECRET,
        "grant_type":grant_type,
        "refresh_token":quote(token_dict["refresh_token"])
    }
    request = requests.post(base_url, json=data).json()
    if request.get("status") == 400:
       print(request.get("error"))
       print(request.get("message")) 
       return
    else:
        print("Novo token de acesso gerado! (refresh)")
    dict_str = json.dumps(request)
    encrypted_data = cipher_suite.encrypt(dict_str.encode())
    with open('encrypted_access.bin', 'wb') as file:
        file.write(encrypted_data)

def revoke_token():
    with open('encrypted_access.bin', 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    token_dict = json.loads(decrypted_data.decode())
    base_url = "https://id.twitch.tv/oauth2/revoke"
    data = {
        "client_id":settings.CLIENT_ID,
        "token":token_dict['access_token']
    }
    request = requests.post(base_url, data=data)
    if request.status_code == 200:
        print("Código de acesso revogado")
    else:
        request = request.json()
        print("Falha")
        print(request["status"])
        print(request["message"])