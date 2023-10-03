# Importando as bibliotecas necessárias
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from random import choices
from time import sleep
import json
import requests
import warnings
from names import generate_name

# Definindo a URL base para criar a conta no Valorant
BASE_URL = 'https://auth.riotgames.com/login#client_id=play-valorant-web-prod&nonce=NzcsMTA2LDEwMCwx&prompt=signup&redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in%2F%3Fredirect%3D%2Fdownload%2F&response_type=token%20id_token&scope=account%20openid&state=c2lnbnVw&ui_locales=it'

# Classe para gerar nomes coloridos no console
class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Função para atualizar o arquivo de extensão do hcaptcha solver
def update_crx():
    crx_page_url = "https://chrome.google.com/webstore/detail/hektcaptcha-hcaptcha-solv/bpfdbfnkjelhloljelooneehdalcmljb"
    ext_id = crx_page_url.split('/')[-1]
    download_link = f"https://clients2.google.com/service/update2/crx?response=redirect&os=crx&arch=x86-64&nacl_arch=x86-64&prod=chromecrx&prodchannel=unknown&prodversion=88.0.4324.150&acceptformat=crx2,crx3&x=id%3D{ext_id}%26uc"
    with open('solver.crx', 'wb') as file:
        addon_binary = requests.get(download_link).content
        file.write(addon_binary)
    print(f"[*] hcaptcha solver updated {bcolors.MAGENTA}[{bcolors.RESET}{ext_id}{bcolors.MAGENTA}]{bcolors.RESET}")

# Classe para criar contas no Valorant
class RiotGen():
    def __init__(self):
        update_crx()
        options = webdriver.ChromeOptions()
        options.add_extension('solver.crx')
        options.headless = False
        # Inicializando o driver do Chrome com o serviço configurado
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.email = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890', k=6)) + "@gmail.com"
        self.name = generate_name()
        self.password = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))

    # Método para criar uma conta no Valorant
    def login(self):
        try:
            # Navegando até a página de criação de conta
            self.driver.get(BASE_URL)
            sleep(2)
            # Preenchendo os campos do formulário de registro
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[1]/div/input', self.email)
            birthdate = '01012000'  # Data de nascimento a ser inserida
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div/div[1]/input', birthdate)
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div/div/input', self.name)
            self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[1]/div/input').send_keys(self.password)
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[3]/div/input', self.password)
            print('[*] solving the hcaptcha')

            not_solved = True
            while not_solved:
                try:
                    # Verificando se a conta foi criada com sucesso
                    if self.driver.current_url != BASE_URL:
                        print(f'{bcolors.GREEN}[+]{bcolors.RESET}{bcolors.CYAN} Account Created:{bcolors.RESET} {self.name},{self.password},{birthdate}')  # Adicionando birthdate
                        not_solved = False
                except Exception:
                    # Se o teste do hcaptcha falhar, tenta novamente
                    print("hcaptcha test failed. Retrying...")
                    next_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/button')
                    self.driver.execute_script("arguments[0].click();", next_btn)

            # Salvando as credenciais em um arquivo
            with open('Credentials.txt','a') as handler:
                handler.write(f'{datetime.now()}\n')
                handler.write(f'Email: {self.email}\n')
                handler.write(f'Username: {self.name}\n')
                handler.write(f'Password: {self.password}\n')
                handler.write(f'Birthdate: {birthdate}\n')  # Adicionando birthdate
                handler.write('---------------------------\n')

        except Exception as e:
            # Se ocorrer um erro, imprime a mensagem de erro
            print(f'{bcolors.RED}[-]{bcolors.RESET}{bcolors.CYAN} Failed to Create Account {bcolors.RESET}, reason:', e)

    # Método para inserir dados em um campo do formulário
    def insert_field(self, value, arg):
        self.driver.find_element(by=By.XPATH, value=value).send_keys(arg)
        next_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/button')
        self.driver.execute_script("arguments[0].click();", next_btn)

# Criando uma instância da classe RiotGen e chamando o método login para criar uma conta no Valorant
bot = RiotGen()
bot.login()
