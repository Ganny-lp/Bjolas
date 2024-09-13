from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Caminho para o driver do Edge
driver_path = 'edgedriver_win64/msedgedriver.exe'

# Configura o serviço do Edge WebDriver
service = Service(driver_path)

# Inicializa o WebDriver
driver = webdriver.Edge(service=service)

# Acessa o site de login
driver.get('https://revistas.usp.br/prolam/login')

# Espera até que o campo de login seja carregado e realiza o login
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)

# Preenche o usuário e senha
usuario = 'prolamjournal'
senha = 'revistaprl@2020'

driver.find_element(By.ID, 'username').send_keys(usuario)
driver.find_element(By.ID, 'password').send_keys(senha)

# Envia o formulário de login
driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)

# Aguarda até a próxima página ser carregada
time.sleep(5)

# Variável de submissão
ID_Submissao = '227308'

# Acessa a página protegida da submissão
url_submissao = f'https://revistas.usp.br/prolam/workflow/index/{ID_Submissao}/3'
driver.get(url_submissao)

# Espera o nome do parecerista aparecer
try:
    parecerista_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='label' and contains(text(), 'Elen Cristina')]"))
    )
    parecerista = parecerista_element.text
    print(f"Parecerista encontrado: {parecerista}")
except Exception as e:
    print(f"Erro ao encontrar parecerista: {e}")
    driver.quit()
    exit()

# Expande o botão "show_extras"
try:
    extras_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='hide_extras']"))
    )
    extras_button.click()
except Exception as e:
    print(f"Erro ao clicar em 'show_extras': {e}")
    driver.quit()
    exit()

# Encontrar e clicar no próximo elemento que contém "Detalhes"
try:
    # Localiza todos os elementos que podem conter o texto "Detalhes"
    detalhes_elements = driver.find_elements(By.XPATH, "//a[contains(text(), 'Detalhes da avaliação')]")
    
    if detalhes_elements:
        # Obtém o primeiro elemento que contém "Detalhes"
        detalhes_button = detalhes_elements[0]

        # Scroll para o elemento para garantir que ele esteja visível
        driver.execute_script("arguments[0].scrollIntoView(true);", detalhes_button)

        # Adiciona um pequeno delay para garantir que o elemento esteja interativo
        time.sleep(2)

        # Tenta clicar no elemento usando JavaScript
        driver.execute_script("arguments[0].click();", detalhes_button)

        print("Achou e clicou em 'Detalhes da avaliação'")
    else:
        print("Não encontrou elementos contendo 'Detalhes da avaliação'")

except Exception as e:
    print(f"Erro ao encontrar ou clicar em 'Detalhes da avaliação': {e}")

# Fechar o navegador
driver.quit()
