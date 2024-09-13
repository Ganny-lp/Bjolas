from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Caminho do driver Edge
driver_path = 'Edge_driver/msedgedriver.exe'
driver = webdriver.Edge(driver_path)

# Acessa o site e faz o login
driver.get('https://revistas.usp.br/prolam/login')

# Espera até que o campo de login seja carregado e realiza o login
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
).send_keys('seu_usuario')
usuario = 'prolamjournal'
senha = 'revistaprl@2020'

driver.find_element(By.ID, 'username').send_keys(usuario)
driver.find_element(By.ID, 'password').send_keys(senha)

# Variável de submissão
ID_Submissao = '227308'  # Substitua pelo ID real

# Acessa a página protegida da submissão
url_submissao = f'https://revistas.usp.br/prolam/workflow/index/{ID_Submissao}/3'
driver.get(url_submissao)

# Espera o nome do parecerista aparecer
parecerista_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[@class='label' and contains(text(), 'Elen Cristina Souza Doppenschmitt')]"))
)

parecerista = parecerista_element.text
print(f"Parecerista encontrado: {parecerista}")

# Expande o botão "show_extras"
extras_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@class='hide_extras']"))
)
extras_button.click()

# Espera e clica em "Detalhes da avaliação"
detalhes_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Detalhes da avaliação')]"))
)
detalhes_button.click()

# Procura pela data de conclusão da avaliação
data_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='pkp_controllers_informationCenter_itemLastEvent' and contains(text(), 'Completo em:')]"))
)
data_text = data_element.text

# Extraindo a data no formato DD/MM/AAAA
data_completa = data_text.split("Completo em: ")[1].split(" ")[0]
dia, mes, ano = data_completa.split('-')
data_formatada = f"{dia}/{mes}/{ano}"

print(f"Data de conclusão: {data_formatada}")

# Fechar o navegador
driver.quit()
