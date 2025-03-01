from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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

# Espera o nome do parecerista aparecer e rola até ele
parecerista_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//span[@class='label' and contains(text(), 'Elen Cristina')]"))
)

# Garante que o parecerista esteja visível rolando até ele
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", parecerista_element)

# Verifica se o elemento está visível
is_visible = driver.execute_script("return arguments[0].offsetParent !== null;", parecerista_element)
print(f"Elemento parecerista visível: {is_visible}")

# Print do texto do elemento para debug
print(f"Texto do parecerista: {parecerista_element.text}")

# Espera o botão "show_extras" e tenta clicar
extras_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class='show_extras']"))
)

# Verifica se o botão está visível e clicável
is_visible_button = driver.execute_script("return arguments[0].offsetParent !== null;", extras_button)
print(f"Botão 'show_extras' visível: {is_visible_button}")

# Rolar para o botão e tentar clicar
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", extras_button)

# Print do estado do botão antes do clique
print(f"Estado do botão 'show_extras' antes do clique: {extras_button.is_displayed()}")

# Tentativa de clique direto via JavaScript
try:
    driver.execute_script("arguments[0].click();", extras_button)
    print("Clique via JavaScript realizado com sucesso")
except Exception as e:
    print(f"Erro ao clicar via JavaScript: {e}")

# Espera e clica em "Detalhes da avaliação"
detalhes_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Detalhes da avaliação')]"))
)

# Rolar para o botão e tentar clicar
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", detalhes_button)

# Print do estado do botão antes do clique
print(f"Estado do botão 'Detalhes da avaliação' antes do clique: {detalhes_button.is_displayed()}")

# Tentativa de clique direto via JavaScript
try:
    driver.execute_script("arguments[0].click();", detalhes_button)
    print("Clique via JavaScript realizado com sucesso")
except Exception as e:
    print(f"Erro ao clicar via JavaScript: {e}")

# Espera pela data de conclusão
data_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='pkp_controllers_informationCenter_itemLastEvent' and contains(text(), 'Completo em:')]"))
)
data_text = data_element.text

# Extraindo a data no formato DD/MM/AAAA
data_completa = data_text.split("Completo em: ")[1].split(" ")[0]
ano, mes, dia = data_completa.split('-')
data_formatada = f"{dia}/{mes}/{ano}"

print(f"Data de conclusão: {data_formatada}")

# Fechar o navegador
driver.quit()
