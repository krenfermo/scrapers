import requests
from bs4 import BeautifulSoup
import math
import time
import sys
import os

from datetime import datetime
from pathlib import Path
import cloudscraper
import csv 
 



def import_csv(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        print(csvfilename)
        reader = csv.reader(scraped, delimiter=',')
        row_index=1
        for row in reader:
            if row:  # avoid blank lines
                row_index += 1
                try: 
                    columns = [row[0]]
                    data.append(columns)
                except:
                    continue
    f = open(csvfilename, "r+")
    lines = f.readlines()
    lines.pop()
    f = open(csvfilename, "w+")
    f.writelines(lines)
    return data

def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1

def navega_page(pagina):
    
    print(pagina)
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    page =  scraper.get(pagina, headers=headers)
    
    #page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='list-card-container')
    elements = results.select('div[class*="posting-card"]')
    return elements,soup

def navega_cada_pagina(pagina):
  
    print(pagina)
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    page =  scraper.get(pagina, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='status-development card-container')
    
    if results==None:
        #print("venta")
        
                
        venta(soup,pagina)
    else:
        #print("Preventa")
        preventa(soup,pagina)
        

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



def venta(soup,pagina):
    try:
        precio = soup.find('div', class_='price-items').text
    #print(precio.text.lstrip().rstrip())
    except:
        precio="None"
   
    
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
    

    nombre = soup.find('li', class_='bread-item current')
    try:
        if nombre==None:
            nombre=pagina.rsplit('/', 1)[-1]
            nombre=nombre.split("-")
            size=len(nombre)
            nombre.pop()
            name=""
            for item in nombre:
                name+=item.capitalize()+" " 
            #f.write(name.lstrip().rstrip()+"|")
            nombre=normalize(str(name.lstrip().rstrip()))
            
        else:
            
            #f.write(nombre.text.lstrip().rstrip()+"|")
            nombre=nombre.text.lstrip().rstrip()
            nombre=nombre.replace(",","")
            nombre=nombre.replace("\"","")
            nombre=normalize(str(nombre))
    except:
        nombre="None"        
    
    try:
        
        Descripcion = soup.find('div', id='verDatosDescripcion')    
        #print(Descripcion.text)
        #f.write(Descripcion.text+"|")
        Descripcion=Descripcion.text
        Descripcion=Descripcion.replace("\"","")
        Descripcion=normalize(str(Descripcion))
    except:
        Descripcion="None"    
    
    f.write("\""+precio.lstrip().rstrip().replace("MN","").replace(",","")+"\",")
    f.write("\""+operation+"\",")
    if "casa" in Descripcion or "casa" in nombre:
            file_catego="Casa"

    elif "departamento" in Descripcion or "departamento" in nombre:
        file_catego="Departamento"
    elif "depto" in Descripcion or "depto" in nombre:
        file_catego="Departamento"
    elif "Depto" in Descripcion or "Depto" in nombre:
        file_catego="Departamento"
           
    f.write(file_catego+",")
    f.write("\""+nombre+"\",")
    f.write("\""+Descripcion+"\",")
    #f.write("\""+Descripcion.text+"\",")
    
    status = soup.find('ul', class_='section-icon-features')
    columns = status.find_all('li', class_='icon-feature')
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
            dato=column.find('b').text +" "+column.find('span').text
            #print(dato)
            #f.write(str(dato)+"|")
            
            if "Terreno" in str(dato):
                terreno=str(dato).split("m")
                terreno= str(terreno[0].lstrip().rstrip())
                
            if "Construidos" in str(dato):
                
                
                construidos=str(dato).split("m")
                construidos= str(construidos[0].lstrip().rstrip())
                
                    
            if "Medios" in str(dato):
                Medios=str(dato)   
            
            if Medios=="None" and  "Baño" in str(dato):
            
                banios=str(dato)
            
            
            if "Estacionamiento" in str(dato):
                estacionamientos=str(dato).replace("Estacionamientos","").replace("Estacionamiento","")
            
            
            if "Recámaras" in str(dato):
                Recamaras=str(dato) 
            

            
            
        
            if "Antigüedad" in str(dato):
                Antiguedad=str(dato)
    except:
        pass        
 
    #print("\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\",")    
    items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\","
    f.write(normalize(str(items_data)).replace("Recamaras","").replace("Recamara","").replace("Banos","").replace("Bano","").replace("Medios","").replace("Medio",""))
        
    calle="None"
    colonia="None"
    delegacion="None"
    ciudad="None"   
    try:    
        location=soup.find('div',class_='section-location')
        #print(location.text.lstrip().rstrip())   
        #f.write(location.text.lstrip().rstrip()+"|")
        location=location.text.lstrip().rstrip()
        location=location.replace("\"","")
        
        location=location.split(",")
        #print(location)
        items_data2="\"None\",\"None\",\"None\",\"None\","
        if (len(location)==3):
            calle=location[0]
            colonia=location[1]
            delegacion=location[2]
            items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
        if (len(location)>3):
            calle=location[0]
            colonia=location[1]
            delegacion=location[2]
            ciudad=location[3]
            items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
    except:
        items_data2="\"None\",\"None\",\"None\",\"None\","
            
    
    
    f.write(normalize(str(items_data2)))
    try:
        #f.write("\""+location+"\",")
        publicado=soup.find('h5',class_='section-date css-float-r')
        #print(static_map['src'])
        #f.write(static_map['src']+"\n")
        
        if publicado!=None:
            
            publicado=publicado.text
        else:
            publicado="None"
        #print (publicado)
   
        publicado=publicado.replace("Publicado hace","").lstrip().rstrip()
    except:
        publicado="None"
    f.write("\""+normalize(str(publicado))+"\"\n")




def preventa(soup,pagina):
  try:
    precio = soup.find('span', class_='data-price')
    #print(precio.text.lstrip().rstrip())
    #f.write(precio.text.lstrip().rstrip()+"|")
    
    
    
    file_catego="None"
    if "casa" in pagina:
        file_catego="Casas"
    elif "departamento" in pagina:
        file_catego="Departamento"

    
    nombre = soup.find('li', class_='bread-item current')
    #print(nombre.text.lstrip().rstrip())  
    #f.write(nombre.text.lstrip().rstrip()+"|")  
    nombre=nombre.text.lstrip().rstrip()
    nombre=nombre.replace(",","")
    nombre=nombre.replace("\"","")
    

    
    Descripcion = soup.find('div', id='verDatosDescripcion')
    #print(Descripcion.text)
    #f.write(Descripcion.text+"|")
    Descripcion=Descripcion.text
    Descripcion=Descripcion.replace("\"","")

    
    
    status = soup.find('div', class_='status-columns')
    
    columns = status.find_all('div', class_='column')
    
    terreno="None"
    construidos="None"
    banios="None"
    estacionamientos="None"
    Recamaras="None"
    Medios="None"
    Antiguedad="None"
    
    for column in columns:
        rows = column.find_all('div', class_='row')
        for row in rows:
            #print("XXXXXX"+str(row))
            
            span_label=row.find_all('span',class_='label')
            for span in span_label:
                etiqueta=span.text.lstrip().rstrip()
                
            span_data=row.find_all('span',class_='data')
            for span in span_data:
                datos=" "+str(span.text.lstrip().rstrip())
                
            if "Terreno" in str(etiqueta):
                if str(datos)=="-":
                    terreno="None"
                else:
                    terreno=str(datos).split("m")
                    
                    #construidos=[int(s) for s in construidos.split("m") if s.isdigit()]
                    #print(construidos)
                    terreno= str(terreno[0].lstrip().rstrip())
                        
       
            if "construídos" in str(etiqueta):
                if str(datos)=="-":
                    construidos="None"
                else:
                    construidos=str(datos).split("m")
                    
                    #construidos=[int(s) for s in construidos.split("m") if s.isdigit()]
                    #print(construidos)
                    construidos= str(construidos[0].lstrip().rstrip())
                
        
                 
            if "Estacionamiento" in str(etiqueta):
                if str(datos)=="-":
                    estacionamientos="None"
                else:
                                       
                    estacionamientos=str(datos)
                             
            if "Recámaras" in str(etiqueta):
                Recamaras=str(datos) 

            #datos=span_label.text.lstrip().rstrip()+" "+span_data.text.lstrip().rstrip()
            #print (datos)
            #f.write(datos+"|")
            
            #f.write("\""+datos+"\",")
    
    items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\","
    
    
    
              
    
    calle="None"
    colonia="None"
    delegacion="None"
    ciudad="None"
    
    location=soup.find('div',class_='section-location')
    #print(location.text.lstrip().rstrip())
    #f.write(location.text.lstrip().rstrip()+"|")
    location=location.text.lstrip().rstrip()
    location=location.replace("\"","")
    
    location=location.split(",")
    #print(location)
    items_data2="\"None\",\"None\",\"None\",\"None\""
    
    if (len(location)==3):
       calle=location[0]
       colonia=location[1]
       delegacion=location[2]
       items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
    if (len(location)>3):
        calle=location[0]
        colonia=location[1]
        delegacion=location[2]
        ciudad=location[3]
        items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
    
    
    f.write("\""+normalize(str(precio.text.lstrip().rstrip().replace("MN","")))+"\",")
    f.write("\"Preventa\",")
    f.write(file_catego+",")
    f.write("\""+normalize(str(nombre))+"\",")
    f.write("\""+normalize(str(Descripcion))+"\",")
    f.write(normalize(str(items_data)).replace("Recamaras","").replace("Recamara","").replace("Banos","").replace("Bano","").replace("Medios","").replace("Medio",""))
    
    f.write(normalize(str(items_data2)))
    

    f.write("\"None\"\n")
  except:
     return False   
 

def cuerpo(URL):
    
    elements,soup=navega_page(URL)
        
    no_results=soup.find('div', class_='no-results__message')
    if no_results!=None:
        return False
    Total_pages = soup.find('h1', class_='list-result-title')
    #print(Total_pages)
    Total_pages=str(Total_pages).replace('<h1 class="list-result-title">', '').replace('</h1>', '')

    Total_pages=str(Total_pages).split()
    #print(Total_pages)
    Total_pages=str(Total_pages[0]).replace('<b>','').replace(',','')
    print(str(Total_pages)+" Resultados")
    #print(Total_pages)
    Total_pages=int(Total_pages)/20
    #print(Total_pages)
    Total_pages=my_round(Total_pages+0.5)


    print(str(Total_pages)+" Paginas")


    
    for pages in range(comienzo,Total_pages+1) :
        list_url=list()
        
        URL2=URL
        URL2=URL2.replace(".html","-pagina-"+str(pages)+".html")
            
        print("PAGINA:"+ str(pages))
        #f.write(URL+"|")
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(URL2, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        #time.sleep(5)
        no_results=soup.find('div', class_='no-results__message')
        if no_results!=None:
            print("se sale")
            continue
        
        results = soup.find('div', class_='list-card-container')

        #elements = results.find_all('div', class_='posting-card super-highlighted')
        elements = results.select('div[class*="posting-card"]')
        
        #print(elements)
        
        #print(elements)
        for job_elem in elements:
            title_elem = job_elem.find('h2', class_='posting-title')
            
            a_href = title_elem.find('a', href=True)
            #print(a_href)
            if None in (title_elem, a_href):
                print("continua")
                continue
            
            #print(title_elem.text.strip())
        # print(str(counter)+" https://www.inmuebles24.com/"+a_href['href'])
            list_url.append("https://www.inmuebles24.com"+a_href['href'])
            
             
            
        #(len(list_url))        
        for item in list_url:
        #print(item)
            #f.write(item+"|")
            
            f.write("\""+item.lstrip().rstrip()+"\",")
            navega_cada_pagina(item)
            
            
#python3 scrap_uno.py "comprar" "departamento" "narvarte"
 
URL=sys.argv[1]
miarchivo=str(sys.argv[2])
comienzo=int(sys.argv[3])

   
# Asigna formato de ejemplo1
formato1 = "%Y-%m-%d"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\INMUEBLES24_URL\\"
if os.path.exists(path):
    pass
else:
     
    os.mkdir(path)

 

print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)









if os.path.exists(path+"\\"+miarchivo+".csv"):
            print("ya EXISTE ARCHIVO " + str(path+"\\"+miarchivo+".csv"))
           
            data = import_csv(path+"\\"+miarchivo+".csv")
            #last_row = data[-1]
            #print()
            
            #exit() 
            f= open(path+"\\"+miarchivo+".csv","a+") 
            cuerpo(URL)                                                                                                                                                                                  
           
            
else:
            last_row="null"
            print("no existe CREA CSV " + str(path+"\\"+miarchivo+".csv"))
            f= open(path+"\\"+miarchivo+".csv","w+")
                                                                                                                                                                                                

            f.write("\"URL\","+"\"PRECIO\","+"\"TIPO\","+"\"CATEGORIA\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"TERRENO\","+"\"CONSTRUIDOS\","+"\"BAÑOS\","+"\"ESTACIONAMIENTO\","+"\"RECAMARAS\","+"\"MEDIOS BAÑOS\","+"\"ANTIGÜEDAD\","+"\"CALLE\","+"\"COLONIA\","+"\"DELEGACION\","+"\"CIUDAD\","+"\"PUBLICADO\"\n")
            cuerpo(URL)
            
            
            
 
f.close() 



