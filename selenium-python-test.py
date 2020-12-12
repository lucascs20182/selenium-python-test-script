from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

arquivo_excel = Workbook()

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

def setup():
    driver.get('https://www.amazon.com.br/')

def navigation():
    iptBusca = driver.find_element_by_id('twotabsearchtextbox')

    iptBusca.clear()
    iptBusca.send_keys('iphone')
    iptBusca.send_keys(Keys.ENTER)

def getPreco(lista):
    i = 0
    while(i < len(lista)):
        if 'R$' in lista[i]:
            return lista[i] + ',' + lista[i+1]

        i += 1

def Deve_Pegar_O_Nome_E_Preco_De_Cada_Item_Da_Busca():
    dados = driver.find_elements_by_css_selector('#search > div.s-desktop-width-max.s-desktop-content.sg-row > div.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div > div')

    dadosFormatados = []
    dadosSelecionados = []

    for registro in dados:
        temp = registro.text.split('\n')
        dadosFormatados.append(temp)
    
    for registro in dadosFormatados:
        dadosSelecionados.append((registro[0], getPreco(registro)))
    
    return dadosSelecionados

def construirArquivoExcel(valores):
    planilha1 = arquivo_excel.active
    planilha1.title = "Resultados Página 1"

    for linha in valores:
        planilha1.append(linha)

    arquivo_excel.save('desafio.xlsx')

def tearDown():
    driver.quit()

setup()
navigation()
dados = Deve_Pegar_O_Nome_E_Preco_De_Cada_Item_Da_Busca()
construirArquivoExcel(dados)
tearDown()
