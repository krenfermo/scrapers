import requests
from bs4 import BeautifulSoup
import math
import time
import sys
import os

from datetime import datetime
from pathlib import Path


#comprar-departamento-cdmx
#https://www.inmuebles24.com/departamentos-en-venta-pagina-1-q-cdmx.html

#comprar-casa-cdmx
#https://www.inmuebles24.com/casas-o-duplex-o-casa-en-condominio-en-venta-pagina-1-q-cdmx.html

#comprar-casa-en-condominio-cdmx
#https://www.inmuebles24.com/casa-en-condominio-en-venta-pagina-1-q-cdmx.html

#comprar-oficina-cdmx
#https://www.inmuebles24.com/oficinas-en-venta-pagina-1-q-cdmx.html

#comprar-locales-comerciales-cdmx
#https://www.inmuebles24.com/locales-comerciales-en-venta-pagina-1-q-cdmx.html

#comprar-bodegas-comerciales-cdmx
#https://www.inmuebles24.com/bodegas-comerciales-en-venta-pagina-1-q-cdmx.html

#comprar-terrenos-cdmx
#https://www.inmuebles24.com/terrenos-en-venta-pagina-1-q-cdmx.html


#comprar-otros-tipos-de-propiedades-cdmx
#https://www.inmuebles24.com/otros-tipos-de-propiedades-en-venta-pagina-1-q-cdmx.html


def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1

def navega_page(pagina_numero,catego,op,query):
    if len(sys.argv)<=4:
        URL = 'https://www.inmuebles24.com/'+catego+op+'en-'+str(query)+'.html'
    else:
        URL = 'https://www.inmuebles24.com/'+catego+op+'q-'+str(query)+'.html'
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='list-card-container')
    elements = results.select('div[class*="posting-card"]')
    return elements,soup

def navega_cada_pagina(pagina,cate):
    URL = pagina
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='status-development card-container')
    
    if results==None:
        #print("venta")
        venta(soup,pagina,cate)
    else:
        #print("Preventa")
        preventa(soup,pagina,cate)
        

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



def venta(soup,pagina,cate):
    
    precio = soup.find('div', class_='price-items')
    #print(precio.text.lstrip().rstrip())
    
    f.write("\""+precio.text.lstrip().rstrip().replace("MN","")+"\",")
    f.write("\"Venta\",")
    
    if cate in ["casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-"]:
            file_catego="Casas"
    else:
            file_catego=cate
    f.write(file_catego+",")
    nombre = soup.find('li', class_='bread-item current')
    if nombre==None:
        nombre=pagina.rsplit('/', 1)[-1]
        nombre=nombre.split("-")
        size=len(nombre)
        nombre.pop()
        name=""
        for item in nombre:
            name+=item.capitalize()+" " 
        #f.write(name.lstrip().rstrip()+"|")
        f.write("\""+normalize(str(name.lstrip().rstrip()))+"\",")
        #print(nombre.text.lstrip().rstrip())
    else:
        
        #f.write(nombre.text.lstrip().rstrip()+"|")
        nombre=nombre.text.lstrip().rstrip()
        nombre=nombre.replace(",","")
        nombre=nombre.replace("\"","")
        f.write("\""+normalize(str(nombre))+"\",")
        #f.write("\""+nombre.text.lstrip().rstrip()+"\",")
        
    Descripcion = soup.find('div', id='verDatosDescripcion')    
    #print(Descripcion.text)
    #f.write(Descripcion.text+"|")
    Descripcion=Descripcion.text
    Descripcion=Descripcion.replace("\"","")
    f.write("\""+normalize(str(Descripcion))+"\",")
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
        
 
    #print("\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\",")    
    items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\","
    f.write(normalize(str(items_data)).replace("Recamaras","").replace("Recamara","").replace("Banos","").replace("Bano","").replace("Medios","").replace("Medio",""))
        
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
    f.write(normalize(str(items_data2)))
    
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
    f.write("\""+normalize(str(publicado))+"\"\n")




def preventa(soup,pagina,cate):
  
    precio = soup.find('span', class_='data-price')
    #print(precio.text.lstrip().rstrip())
    #f.write(precio.text.lstrip().rstrip()+"|")
    
    f.write("\""+normalize(str(precio.text.lstrip().rstrip().replace("MN","")))+"\",")
    f.write("\"Preventa\",")
    
    if cate in ["casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-"]:
            file_catego="Casas"
    else:
            file_catego=cate
    f.write(file_catego+",")
    
    nombre = soup.find('li', class_='bread-item current')
    #print(nombre.text.lstrip().rstrip())  
    #f.write(nombre.text.lstrip().rstrip()+"|")  
    nombre=nombre.text.lstrip().rstrip()
    nombre=nombre.replace(",","")
    nombre=nombre.replace("\"","")
    f.write("\""+normalize(str(nombre))+"\",")
    
    Descripcion = soup.find('div', id='verDatosDescripcion')
    #print(Descripcion.text)
    #f.write(Descripcion.text+"|")
    Descripcion=Descripcion.text
    Descripcion=Descripcion.replace("\"","")
    f.write("\""+normalize(str(Descripcion))+"\",")
    
    
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
    f.write(normalize(str(items_data)).replace("Recamaras","").replace("Recamara","").replace("Banos","").replace("Bano","").replace("Medios","").replace("Medio",""))
    
    
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
    f.write(normalize(str(items_data2)))
    

    f.write("\"None\"\n")
    
 


#python3 scrap_uno.py "comprar" "departamento" "narvarte"

#operation=["en-venta-","en-renta-","desarrollos-","oficinas-","en-temporal-vacacional-","en-venta-incluir-comercializa-remates-publisher-"]
#categories=["departamentos-","casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-","oficinas-","locales-comerciales-","bodegas-comerciales-","terrenos-","otros-tipos-de-propiedades-"]

opera=sys.argv[1]
if opera in ["compra","comprar","venta"]:
    operation=["en-venta-"]

if opera in ["renta","rentar"]:
    operation=["en-renta-"]
    
if opera in ["remate","remates"]:
    operation=["en-venta-incluir-comercializa-remates-publisher-"]
      
if opera in ["desarrollo","desarrollos"]:
    operation=["desarrollos-"]
    
if opera in ["temporal"]:
    operation=["en-temporal-vacacional-"]

if opera in ["comercial"]:
    operation=["oficinas-"]      


if len(sys.argv)==3:
    categories=["departamentos-","casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-","oficinas-","locales-comerciales-","bodegas-comerciales-","terrenos-","otros-tipos-de-propiedades-","en-temporal-vacacional-","en-traspaso-"]
    query=sys.argv[2]
    category="TODO"
 
if len(sys.argv)==4:
        
    category=sys.argv[2]

    if category in ["departamento","departamentos"]:
        categories=["departamentos-"]

    if category in ["casa","casas"]:
        categories=["casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-"]
        
    if category in ["oficina","oficinas"]:
        categories=["oficinas-"]

    if category in ["local","local comercial"]:
        categories=["locales-comerciales-"]

    if category in ["bodega","bodega comercial","bodegas","bodegas comerciales"]:
        categories=["bodegas-comerciales-"]
        
    if category in ["terrenos","terreno"]:
        categories=["terrenos-"]     

    if category in ["otros"]:
        categories=["otros-tipos-de-propiedades-"]
        
    if category in ["comprar","compra"]:
        categories=["en-venta-"]
        
    if category in ["renta","rentar"]:
        categories=["en-renta-"]

    if category in ["temporal","vacacional","temporal vacacional"]:
        categories=["en-temporal-vacacional-"]

    if category in ["remate","remates"]:
        categories=["en-traspaso-"]
        
    query=sys.argv[3]
    
   
# Asigna formato de ejemplo1
formato1 = "%d_%m_%Y"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\INMUEBLES24\\"
if os.path.exists(path):
    pass
else:
     
    os.mkdir(path)

    
path=str(Path().absolute())+"\\INMUEBLES24\\"+str(opera)+"_"+str(category)+"_"+str(query)+"_"+hoy

print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)



f= open(path+"\\"+opera+"_"+category+".csv","w+")
        								                                                                                                                                			

f.write("\"URL\","+"\"PRECIO\","+"\"TIPO\","+"\"CATEGORIA\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"TERRENO\","+"\"CONSTRUIDOS\","+"\"BAÑOS\","+"\"ESTACIONAMIENTO\","+"\"RECAMARAS\","+"\"MEDIOS BAÑOS\","+"\"ANTIGÜEDAD\","+"\"CALLE\","+"\"COLONIA\","+"\"DELEGACION\","+"\"CIUDAD\","+"\"PUBLICADO\"\n")
        
#operation=["en-venta-","en-renta-","desarrollos-","oficinas-","en-temporal-vacacional-","en-venta-incluir-comercializa-remates-publisher-"]
for op in operation:
    #if op in ["en-venta-","en-renta-","desarrollos-","en-venta-incluir-comercializa-remates-publisher-"]:
        #categories=["departamentos-","casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-","oficinas-","locales-comerciales-","bodegas-comerciales-","terrenos-","otros-tipos-de-propiedades-"]
    #if op in ["oficinas-"]:
        #categories=["en-venta","en-renta","en-temporal-vacacional-","en-traspaso-","desarrollos-"]
    #if op in ["en-temporal-vacacional--"]:
        #categories=["duplex-o-casa-en-condominio-o-casas-","departamentos-","villa-","casa-en-condominio-","quinta-","otros-tipos-de-propiedades-"]
        
    for cate in categories:
        '''
        if cate=="bodegas-comerciales-" and op=="desarrollos-":
            continue
        if cate=="desarrollos-" and op=="oficinas-":
            continue
        print (cate+" "+op)
        
        if cate=="casas-o-duplex-o-casa-en-condominio-" or op=="duplex-o-casa-en-condominio-o-casas-":
            file_catego="casas-"
        else:
            file_catego=cate
        file_op=""
        if op=="en-temporal-vacacional-":
            file_op="temporal"
        if op=="en-venta-incluir-comercializa-remates-publisher-":
            file_op="remates"
        if file_op=="":
            file_op=op
        ''' 
            
            
        #print(path+"\\"+file_op+file_catego+".csv")    
        counter=1
        #print(op)
        
        if op in ["desarrollos-","oficinas-"]:
            elements,soup=navega_page(str(counter),op+"o-",cate,query)
        else:    
            elements,soup=navega_page(str(counter),cate,op,query)

        no_results=soup.find('div', class_='no-results__message')
        if no_results!=None:
            continue
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


        print(Total_pages)

        
        
        for pages in range(1,Total_pages+1) :
            list_url=list()
            print(len(sys.argv))
            if len(sys.argv)<=4:
                if op in ["desarrollos-","oficinas-"]:
                    URL = 'https://www.inmuebles24.com/'+op+"o-"+cate+'pagina-'+str(pages)+'-en-'+str(query)+'.html'
                else:    
                    URL = 'https://www.inmuebles24.com/'+cate+op+'pagina-'+str(pages)+'-en-'+str(query)+'.html'
            else:
                if op in ["desarrollos-","oficinas-"]:
                    URL = 'https://www.inmuebles24.com/'+op+"o-"+cate+'pagina-'+str(pages)+'-q-'+str(query)+'.html'
                else:    
                    URL = 'https://www.inmuebles24.com/'+cate+op+'pagina-'+str(pages)+'-q-'+str(query)+'.html'  
                
            print(str(pages)+ "  "+URL)
            #f.write(URL+"|")
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(URL, headers=headers)
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
                
                counter+=1
                
            #(len(list_url))        
            for item in list_url:
            #print(item)
                #f.write(item+"|")
              
                f.write("\""+item.lstrip().rstrip()+"\",")
                navega_cada_pagina(item,cate)
f.close() 



