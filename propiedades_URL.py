import requests
from bs4 import BeautifulSoup
import math
import time
import sys
import os

from datetime import datetime
from pathlib import Path
#import cloudscraper



def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1

def navega_page(pagina):
     
    
    print(pagina)
    #headers = {'User-Agent': 'Mozilla/5.0'}
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}

# Returns a requests.models.Response object
    #scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    #page =  scraper.get(URL, headers=headers)
    page = requests.get(pagina, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='content-result cont-search-list')
    #elements = results.select('div[class*="posting-card"]')
    return soup


 


def navega_cada_pagina(pagina):
     
    print(pagina)
    #headers = {'User-Agent': 'Mozilla/5.0'}
    
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}
    #scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    #page =  scraper.get(URL, headers=headers)
    page = requests.get(pagina, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    OPERACION(soup,pagina)
     
        
    

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
        ("Ñ", "N"),
        ("ñ", "n"),
        ("Ü", "U"),
        ("ü", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s



def OPERACION(soup,pagina):
    try:
         
        precio = soup.find('span', class_='price')
        precio=precio.text.replace("$","")
        
        if "MDP" in str(precio):
            
            precio=precio.split("MDP")
            precio=precio[0]
          
            precio= float(precio)*(1000000)
            precio="{:.0f}".format(precio)
            
            
             
        if "mil" in str(precio):
            
            precio=precio.split("mil MN")
            precio=precio[0]
            precio= float(precio)*(1000)
            precio="{:.0f}".format(precio)
            
            
    except:
        print("error")
        return False
    
    operation="None"
    if "venta" in pagina:
        operation="Venta"
    if "renta" in pagina:
        operation="Renta"
    
    file_catego="None"
    if "casa" in pagina:
        file_catego="Casa"
    elif "edificio" in pagina:
        file_catego="edificio"
    elif "departamento" in pagina:
        file_catego="Departamento"
    elif "oficina" in pagina:
            file_catego="oficina"
    elif "terreno" in pagina:
        file_catego="terreno"
    elif "bodega" in pagina:
            file_catego="bodega"
 
            

    
    try:
        nombre = soup.find('h1', class_='title-gallery').find('em')
        
            #f.write(nombre.text.lstrip().rstrip()+"|")
        nombre=nombre
        nombre=nombre.text.lstrip().rstrip()
        nombre=nombre.replace(",","")
        nombre=nombre.replace("\"","")
    except:
        nombre="None"

  
    try:    
        Descripcion = soup.find('div', class_='subsection-content').find_all('p')    
    except:
        Descripcion="None"
    #print(Descripcion)
    #f.write(Descripcion.text+"|")
    bandera=True
    for item in Descripcion:
        
        if "type"  in str(item):
            Descripcion="None"
            continue
            
        elif "average" in  str(item):
            #print("average")
            Descripcion="None"
            continue
        elif "<a class" in str(item):
            #print("a class")
            Descripcion="None"
            continue
        elif "Este porcentaje muestra el valor de la propiedad" in str(item):
            #print("a class")
            Descripcion="None"
            continue
        elif "Aunque haya un precio medio en una colonia," in str(item):
            #print("a class")
            Descripcion="None"
            continue

        elif "El porcentaje se ofrece solo como una guía y" in str(item):
            #print("a class")
            Descripcion="None"
            continue

        else: 
            bandera=False
            try:   
                Descripcion=str(item.text)
            except:
                Descripcion="None"
            a="Este porcentaje muestra el valor de la propiedad con respecto a la tendencia de los precios de la zona."
            b="Aunque haya un precio medio en una colonia, cada vivienda cuenta con particularidades que podrían incrementar o disminuir el valor."
            c="El porcentaje se ofrece solo como una guía y podría no reflejar el valor particular de la propiedad."
            
            Descripcion=Descripcion.replace(a,"").replace(b,"").replace(c,"").replace("!","").replace("¡","").replace("\"","")
            #print(Descripcion)
            try:
                    Descripcion=normalize(str(Descripcion))
                    f.write("\""+pagina.lstrip().rstrip()+"\",")
                    
                    f.write("\""+str(precio)+"\",")
                    
                    f.write("\""+operation+"\",")
                    
                    if "casa" in Descripcion or "casa" in nombre:
                        file_catego="Casa"
                    elif "departamento" in Descripcion or "departamento" in nombre:
                        file_catego="Departamento"
                    elif "depto" in Descripcion or "depto" in nombre:
                        file_catego="Departamento"
                    elif "Depto" in Descripcion or "Depto" in nombre:
                        file_catego="Departamento"
                        
                    f.write("\""+file_catego+"\",")
                    f.write("\""+normalize(str(nombre))+"\",")
                    f.write("\""+Descripcion+"\",")
            except:
                bandera=True    
            break
    
    
    if bandera   :
        Descripcion="None"
        if "casa" in Descripcion or "casa" in nombre:
            file_catego="Casa"
        elif "departamento" in Descripcion or "departamento" in nombre:
            file_catego="Departamento"
        elif "depto" in Descripcion or "depto" in nombre:
            file_catego="Departamento"
        elif "Depto" in Descripcion or "Depto" in nombre:
            file_catego="Departamento"
            
        f.write("\""+file_catego+"\",")
        f.write("\""+normalize(str(nombre))+"\",")
        f.write("\""+Descripcion+"\",")
         
   
    
    status = soup.find('ul', class_='carac-large')
    try:
        columns = status.find_all('li')
    except:
        terreno="None"
        construidos="None"
        banios="None"
        estacionamientos="None"
        Recamaras="None"
        Medios="None"
        Antiguedad="None"
        
    terreno="None"
    construidos="None"
    banios="None"
    estacionamientos="None"
    Recamaras="None"
    Medios="None"
    Antiguedad="None"
    try:
        for column in columns:
            #column=str(column).replace('<br>','')
            #print("XXX"+str(column.text.strip()))
            dato=column.find_all('span')
            
            
            #f.write(str(dato)+"|")
            
            if "terreno" in str(dato[0]):
                terreno= dato[1].text
                
            if "construcción" in str(dato[0]):         
                construidos= dato[1].text

            
            if "Baño" in str(dato[0]):      
                banios=dato[1].text
                banios=banios.rstrip().lstrip()
                
            
            
            if "Estacionamiento" in str(dato[0]):
                estacionamientos=dato[1].text
            
            
            if "Recámara" in str(dato[0]):
                Recamaras=dato[1].text
            
        
            if "Edad" in str(dato[0]):
                Antiguedad=dato[1].text
                Antiguedad=Antiguedad.rstrip().lstrip()
        items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\","
        
    except:
               
        items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\","
        
    #print("\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\",")    
    f.write(normalize(str(items_data)))
 
    calle="None"
    colonia="None"
    delegacion="None"
    ciudad="None"   
    try:    
        location=soup.find('h1',class_='title-gallery').find_all('span')
            #location=location.split(",")
        #print(location)
        items_data2="\""+str(calle)+"\","+"\""+str(location[0]).replace("\n","").replace("<span>","").replace("</span>","").replace(",","")+"\","+"\""+str(location[2]).replace("\n","").replace("<span>","").replace("</span>","").replace(",","").replace("\"","").replace("<span itemprop=addressLocality","").replace(">","")+"\","+"\""+str(location[5]).replace("\n","").replace("<span>","").replace("</span>","").replace(",","").replace("\"","").replace("<span itemprop=addressRegion","").replace(">","")+"\","
        f.write(normalize(str(items_data2)))
    except:
        items_data2="\""+str(calle)+"\","+"\""+str("None")+"\","+"\""+str("None")+"\","+"\""+str("None")+"\","
        f.write(normalize(str(items_data2)))
     
    

     
    try:
        publicado=soup.find('p',class_='info-update')
    
        
        if publicado!=None:
            
            publicado=publicado.text
        else:
            publicado="None"
        #print (publicado)
        publicado=publicado.replace("Propiedad actualizada el:","").lstrip().rstrip()
        f.write("\""+normalize(str(publicado))+"\"\n")
    except:
        f.write("\""+str("None")+"\"\n")
    


def cuerpo(URL):
          
 
 
           
        soup=navega_page(URL)
        #print(soup)
        try:
            print("entra")    
            no_results=soup.find('div', class_='content-errors')
            if no_results!=None:
                 return False
            Total_pages = soup.find('div', class_='title-result')
            
            Total_pages=Total_pages.find('span').text.replace(",","")
            print("entra2") 
            print(str(Total_pages)+" resultados")
            Total_pages=int(Total_pages)/42
            #print(Total_pages)
            Total_pages=my_round(Total_pages+0.5)


            print(str(Total_pages) + " paginas" )
            
        except:
             print("error")    
             return False
        
        
        for pages in range(1,Total_pages+1) :
            list_url=list()
            URL2=URL
            URL2=URL2+"?pagina="+str(pages)
            #
            print("PAGINA:"+ str(pages))
            soup =  navega_page(URL2)
            #time.sleep(5)
            no_results=soup.find('div', class_='content-errors')
            if no_results!=None:
                continue
            
            results = soup.find('div', class_='list-new')
        
            #elements = results.find_all('div', class_='posting-card super-highlighted')
            elements = results.select('div[class*="properties-list"]')
            
 
            #print(elements)
            for job_elem in elements:
                
                
                a_href = job_elem["data-href"]
                #print(a_href)
                if a_href==None:
                    print("continua")
                    continue        
               
                

                list_url.append(str(a_href))
                
                 
         
            for item in list_url:
                #scraper = cloudscraper.create_scraper() 
                navega_cada_pagina(item)

#python3 scrap_uno.py "comprar" "departamento" "narvarte"

#operation=["en-venta-","en-renta-","desarrollos-","oficinas-","en-temporal-vacacional-","en-venta-incluir-comercializa-remates-publisher-"]
#categories=["departamentos-","casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-","oficinas-","locales-comerciales-","bodegas-comerciales-","terrenos-","otros-tipos-de-propiedades-"]
 
        
URL=sys.argv[1]
    
    
# Asigna formato de ejemplo1
formato1 = "%Y-%m-%d %H_%M_%S"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\PROPIEDADES_COM_URL\\"
if os.path.exists(path):
    pass
else:
     
    os.mkdir(path)

    
path=str(Path().absolute())+"\\PROPIEDADES_COM_URL\\"+"URL_"+hoy

print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)


f= open(path+"\\"+"URL_"+hoy+".csv","w+")
        								                                                                                                                                			


f.write("\"URL\","+"\"PRECIO\","+"\"TIPO\","+"\"CATEGORIA\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"TERRENO\","+"\"CONSTRUIDOS\","+"\"BAÑOS\","+"\"ESTACIONAMIENTO\","+"\"RECAMARAS\","+"\"MEDIOS BAÑOS\","+"\"ANTIGÜEDAD\","+"\"CALLE\","+"\"COLONIA\","+"\"DELEGACION\","+"\"CIUDAD\","+"\"PUBLICADO\"\n")



cuerpo(URL)

f.close() 



