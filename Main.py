import os
import requests 
import time
import csv
import PyPDF2 as PyPdf
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def Scrapper_boletim():

    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    navegador.get('https://www.cjf.jus.br/cjf/corregedoria-da-justica-federal/turma-nacional-de-uniformizacao/publicacoes-1/boletim-tnu-1')

    time.sleep(9)

    source = navegador.find_element(By.XPATH,'//*[@id="content"]/div').get_attribute("outerHTML")

    site = BeautifulSoup(source, 'html.parser')
    html = site.prettify().split('\n')

    #print(site)

    i = 0
    url = ''
    #boletins = site.find_all('h4')
    while i < len(html):    
    
        if html[i].find('<a class="outstanding-link" href="') != -1:
        
            while html[i].find('ACESSE') == -1:
                url = url +  html[i]
                i += 1

            url = url.replace('     <a class="outstanding-link" href="', '')
            url = url.split('" ng-href')
            print(url[0])
            save_boletim(url[0])
            url = ''

        i += 1

    navegador.close()


def save_boletim(url):
    
    count = 0
    
    path_dir ='C:/Docs/Boletins/'  #Define o local dos arquivos 
    os.chdir(path_dir)  

    for path in os.scandir(path_dir):
        if path.is_file():
            count += 1

    response = requests.get(url)
    pdf = open("Arq_Bol_" +str(count)+".pdf", 'wb')
    pdf.write(response.content)
    pdf.close()

def Bol_parser():
    path_dir ='C:/Docs/Boletins/'  #Define o local dos arquivos 
    os.chdir(path_dir)                    #Posiciona a biblioteca de navegação de pastas na pasta correta 

    file_list = os.listdir()              #Retorna uma lista com todos os arquivos na pasta selecioanda                 

    for file_name in file_list:
        arq = open(path_dir+file_name,'rb')
        try:
            leitor = PyPdf.PdfFileReader(arq, strict=False)
        except:
            print('erro') 
        for k in range(len(leitor.pages)):

            arq_cont = leitor.getPage(k).extractText().split('\n')  

            for i in range(len(arq_cont)):

                if arq_cont[i].find("PUIL") != -1 and arq_cont[i].find("Sessão") == -1 :
                    Proc = arq_cont[i]
                    Proc = Proc + arq_cont[i+1].split('/')[0]

                    Proc = Proc.replace('.', '')
                    Proc = Proc.replace('-', '')
                    Proc = Proc.replace('º', '')
                    Proc = Proc.replace('/', '')
                    Proc = Proc.replace(' ', '')
                    Proc = Proc.replace('N', '')
                    Proc = Proc.replace('n', '')

                    Proc = (Proc.split('PUIL')[1])[0:20]
                    print('Numero Processo:'+Proc)
                    busca_tnu(Proc)
        arq.close()  


def busca_tnu(Proc):

    path_dir ='C:/Docs/Acordaos'  #Define o local dos arquivos 
    os.chdir(path_dir)          

    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    navegador.get('https://www2.cjf.jus.br/jurisprudencia/tnu/')

    navegador.find_element('xpath','//*[@id="formulario:ckbAvancada"]/div[2]').click() #x_path Pesquisa Avançada
    navegador.find_element('xpath','//*[@id="formulario:textoLivre"]').send_keys(Proc)
    navegador.find_element('xpath','//*[@id="formulario:actPesquisar"]').click()

    time.sleep(10)

    try:    
        source = navegador.find_element(By.CLASS_NAME,'table_resultado').get_attribute("outerHTML") #Colocar um validor  formulario:tabelaDocumentos:0:j_idt200:j_idt201 # table_resultado
    except:
        return

    site = BeautifulSoup(source, 'html.parser')
    html = site.prettify().split('\n')

    i = 0
    Dbtipo = ''
    DbNumero = ''
    DbClasse = ''
    Dbrelator = ''
    DbrelatorA = ''
    Dborigem = ''
    DbOJulgad = ''
    DbData = ''
    DbDataPubli = ''
    DbFPubl = ''
    Dbementa = ''
    DbDecisão = ''
    DbLink = ''


    while i < len(html):
        if html[i].find('<span class="label_pontilhada">') != -1: ##find("span", {"class": "label_pontilhada"}):
            if html[i+1].find('Tipo') != -1:
                while html[i].find('</tr>') == -1:
                    Dbtipo = Dbtipo + html[i+5]
                    i += 1
                    
            if html[i+1].find('Número') != -1:
                while html[i].find('</tr>') == -1:
                    DbNumero = DbNumero + html[i+5]
                    i += 1

            if html[i+1].find('Classe') != -1:
                while html[i].find('</tr>') == -1:
                    DbClasse = DbClasse + html[i+4]
                    i += 1

            if html[i+1].find('Relator(a)') != -1:
                while html[i].find('</tr>') == -1:
                    Dbrelator = Dbrelator + html[i+4]
                    i += 1

            if html[i+1].find('Relator para Acórdão') != -1:
                while html[i].find('</tr>') == -1:
                    DbrelatorA = DbrelatorA + html[i+4]
                    i += 1

            if html[i+1].find('Origem') != -1:
                while html[i].find('</tr>') == -1:
                    Dborigem = Dborigem + html[i+4]
                    i += 1

            if html[i+1].find('Órgão julgador') != -1:
                while html[i].find('</tr>') == -1:
                    DbOJulgad = DbOJulgad + html[i+4]
                    i += 1

            if html[i+1].find('Data da publicação') != -1:
                while html[i].find('</tr>') == -1:
                    DbDataPubli = DbDataPubli + html[i+4]
                    i += 1

            if html[i+1].find('Data') != -1:
                while html[i].find('</tr>') == -1:
                    DbData = DbData + html[i+4]
                    i += 1

            if html[i+1].find('Fonte da publicação') != -1:
                while html[i].find('</tr>') == -1:
                    DbFPubl = DbFPubl + html[i+4]
                    i += 1


            if html[i+1].find('Ementa') != -1:
                while html[i+1].find('<span class="label_pontilhada">') == -1:
                    Dbementa = Dbementa + html[i+2]
                    i += 1
            
            if html[i+1].find('Decisão') != -1:
                while html[i+1].find('<span class="label_pontilhada">') == -1:
                    DbDecisão = DbDecisão + html[i+2]
                    i += 1

            if html[i+1].find('Inteiro teor') != -1:
                while html[i+1].find('_blank') == -1:
                    DbLink = DbLink + html[i+2]
                    i += 1

        i += 1

    Dbtipo = Dbtipo.replace('</tr>  <tr>   <td>', '')
    Dbtipo = Dbtipo.replace('<tr>   <td>', '')
    Dbtipo = Dbtipo.replace('    <br/>', '')
    Dbtipo = Dbtipo.replace('</td>', '')
    Dbtipo = Dbtipo[6:]

    DbNumero = DbNumero.replace('</tr>  <tr>   <td>', '')
    DbNumero = DbNumero.replace('<tr>   <td>', '')
    DbNumero = DbNumero.replace('    <br/>', '')
    DbNumero = DbNumero.replace('</td>', '')
    DbNumero = DbNumero[6:]
   
    DbClasse = DbClasse.replace('</tr>  <tr>   <td>', '')
    DbClasse = DbClasse.replace('<tr>   <td>', '')
    DbClasse = DbClasse.replace('    <br/>', '')
    DbClasse = DbClasse.replace('</td>', '')
    DbClasse = DbClasse[6:]

    Dbrelator = Dbrelator.replace('</tr>  <tr>   <td>', '')
    Dbrelator = Dbrelator.replace('<tr>   <td>', '')
    Dbrelator = Dbrelator.replace('    <br/>', '')
    Dbrelator = Dbrelator.replace('</td>', '')
    Dbrelator = Dbrelator[6:]

    DbrelatorA = DbrelatorA.replace('</tr>  <tr>   <td>', '')
    DbrelatorA = DbrelatorA.replace('<tr>   <td>', '')
    DbrelatorA = DbrelatorA.replace('    <br/>', '')
    DbrelatorA = DbrelatorA.replace('</td>', '')
    DbrelatorA = DbrelatorA[6:]

    Dborigem = Dborigem.replace('</tr>  <tr>   <td>', '')
    Dborigem = Dborigem.replace('<tr>   <td>', '')
    Dborigem = Dborigem.replace('    <br/>', '')
    Dborigem = Dborigem.replace('</td>', '')
    Dborigem = Dborigem[6:]

    DbOJulgad = DbOJulgad.replace('</tr>  <tr>   <td>', '')
    DbOJulgad = DbOJulgad.replace('<tr>   <td>', '')
    DbOJulgad = DbOJulgad.replace('    <br/>', '')
    DbOJulgad = DbOJulgad.replace('</td>', '')
    DbOJulgad = DbOJulgad[6:]

    DbData = DbData.replace('</tr>  <tr>   <td>', '')
    DbData = DbData.replace('<tr>   <td>', '')
    DbData = DbData.replace('    <br/>', '')
    DbData = DbData.replace('</td>', '')
    DbData = DbData[6:]
    
    DbDataPubli = DbDataPubli.replace('</tr>  <tr>   <td>', '')
    DbDataPubli = DbDataPubli.replace('<tr>   <td>', '')
    DbDataPubli = DbDataPubli.replace('    <br/>', '')
    DbDataPubli = DbDataPubli.replace('</td>', '')
    DbDataPubli = DbDataPubli[6:]

    DbFPubl = DbFPubl.replace('</tr>  <tr>   <td>', '')
    DbFPubl = DbFPubl.replace('<tr>   <td>', '')
    DbFPubl = DbFPubl.replace('    <br/>', '')
    DbFPubl = DbFPubl.replace('</td>', '')
    DbFPubl = DbFPubl[6:]

    Dbementa = Dbementa.replace('</tr>  <tr>   <td>', '')
    Dbementa = Dbementa.replace('<tr>   <td>', '')
    Dbementa = Dbementa.replace('    <br/>', '')
    Dbementa = Dbementa.replace('</td>', '')
    Dbementa = Dbementa.replace('<span class="label_pontilhada">', '')
    Dbementa = Dbementa.replace(' </div>', '')
    Dbementa = Dbementa[61: ]

    DbDecisão = DbDecisão.replace('</tr>  <tr>   <td>', '')
    DbDecisão = DbDecisão.replace('<tr>   <td>', '')
    DbDecisão = DbDecisão.replace('    <br/>', '')
    DbDecisão = DbDecisão.replace('</td>', '')
    DbDecisão = DbDecisão.replace('<span class="label_pontilhada">', '')
    DbDecisão = DbDecisão[20:]

    DbLink = DbLink.replace('</tr>  <tr>   <td>', '')
    DbLink = DbLink.replace('<tr>   <td>', '')
    DbLink = DbLink.replace('    <br/>', '')
    DbLink = DbLink.replace('</td>', '')
    DbLink = DbLink.replace('<span class="label_pontilhada">', '')
    DbLink = DbLink.replace('    </span>         <a href="', '')  
    DbLink = DbLink.replace('" target="_blank">', '')  


    with open('Banco.txt', 'a+') as arq:
        arq.write(''.join(DbNumero +'|'+ Dbrelator.strip()+ '|'+'RELATOR\n'))
        arq.write(''.join(DbNumero +'|'+ DbClasse.strip()+ '|'+'CLASSE\n'))
        arq.write(''.join(DbNumero +'|'+ DbData.strip()+ '|'+'DATA\n'))

    to_csv(Dbtipo, DbNumero,DbClasse,Dbrelator,DbrelatorA,Dborigem,DbOJulgad,DbData,DbDataPubli,DbFPubl,Dbementa,DbDecisão,DbLink)
        

def to_csv(Dbtipo,DbNumero,DbClasse,Dbrelator,DbrelatorA,Dborigem,DbOJulgad,DbData,DbDataPubli,DbFPubl,Dbementa,DbDecisão,DbLink):
    
    info = [Dbtipo, DbNumero,DbClasse,Dbrelator,DbrelatorA,Dborigem,DbOJulgad,DbData,DbDataPubli,DbFPubl,Dbementa,DbDecisão,DbLink]
    #cabec = ['Tipo', 'Numero','Classe','Relator','Relator Acordão','Origem','Órgão Julgador','Data','Data Publicação','Fonte Publicação','Ementa','Decisão']

    with open ('TNU_PROCESSOS.csv', 'a', encoding='UTF-16', newline='') as arq:
        writer = csv.writer(arq, quoting=csv.QUOTE_NONNUMERIC, delimiter='\t')
        writer.writerow(info)



# O Projeto precisa incialmente acessar o portal do TNU e realizar o download desses arquivos  
Scrapper_boletim()
Bol_parser()

