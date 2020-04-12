import requests
from bs4 import BeautifulSoup
import math
import time
import sys
import os

from datetime import datetime
from pathlib import Path


def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1

def navega_page(URL):
    
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='inner-main')
    
    elements = results.find('ol', id='searchResults')
    return elements,soup

def navega_cada_pagina(pagina,op,cate):
    URL = pagina
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('h1', class_='item-title__primary')
    
    if results!=None:
       venta(soup,pagina,op,cate)
        

    

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


def venta(soup,pagina,op,cate):
    try:
        precio = soup.find('span', class_='price-tag-fraction')
        f.write("\""+pagina.lstrip().rstrip()+"\",")
        f.write("\""+precio.text.lstrip().rstrip()+"\",")
        #f.write("\"None\",")
        f.write("\""+op.replace("-","")+"\",")
    except:
        return False
    
    file_catego=cate
    f.write("\""+file_catego+"\",")
    
    
    #f.write("\"None\",")
 
    nombre = soup.find('header', class_='item-title')
    
    
    nombre=nombre.text.lstrip().rstrip()
    nombre=nombre.replace(",","")
    nombre=nombre.replace("\"","")
    f.write("\""+normalize(str(nombre))+"\",")
    #f.write("\""+nombre.text.lstrip().rstrip()+"\",")
    
    try:    
        Descripcion = soup.find('div', class_='item-description__text')    
        Descripcion=Descripcion.find('p')
   
        Descripcion= Descripcion.text
    except:
        Descripcion="None"
    
   
     
    Descripcion=Descripcion.replace("\"","")
    f.write("\""+normalize(str(Descripcion))+"\",")
    #f.write("\""+Descripcion.text+"\",")
    
    status = soup.find('ul', class_='specs-list')
    try:
        columns = status.find_all('li', class_='specs-item')
    except:
        pass
    terreno="None"
    construidos="None"
    banios="None"
    estacionamientos="None"
    Recamaras="None"
     
    try:
        for column in columns:
            #column=str(column).replace('<br>','')
            #print("XXX"+str(column.text.strip()))
            dato=column.find('strong').text +" "+column.find('span').text
            #print(dato)
            
            
            #f.write(str(dato)+"|")
            
            if "total" in str(dato):
                terreno=str(dato).split("m")            
                terreno=terreno[0].split(" ")
                terreno= str(terreno[-2].lstrip().rstrip())
                
        
            if "construida" in str(dato):          
                
                
                construidos=str(dato).split("m")            
                construidos=construidos[0].split(" ")
                construidos= str(construidos[-2].lstrip().rstrip())
                
                    
            if "Baño" in str(dato):         
                banios=str(dato).replace("Baños","").replace("Baño","")
            
            
            if "Estacionamiento" in str(dato):
                estacionamientos=str(dato).replace("Estacionamientos","").replace("Estacionamiento","")
            
            
            if "Recámaras" in str(dato):
                Recamaras=str(dato).replace("Recámaras","").replace("Recámara","")
            
    except:
        pass
         
     
    items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str("None")+"\","+"\""+str("None")+"\","
    f.write(normalize(str(items_data)))
        
     
    colonia="None"
    delegacion="None"
    ciudad="None"   
    try:    
        location=soup.find('div',class_='seller-location')
        #print(location.text.lstrip().rstrip())   
        
        #f.write(location.text.lstrip().rstrip()+"|")
        calle=location.find('h2',class_='map-address').text
        location=location.text.lstrip().rstrip()
        location=location.replace("\"","")
        
        location=location.split(",")
        #print(location)
        items_data2="\"None\",\"None\",\"None\",\"None\","
        if (len(location)==3):
        #calle=location[0]
            colonia=location[0]
            delegacion=location[1]
            ciudad=location[2]
            items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
            
    except:
        location="None"
        colonia="None"
        delegacion="None"
        ciudad="None"
        calle="None"
        
        items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
    
    
    f.write(normalize(str(items_data2)))
    f.write("\"None\",")
    f.write("\n")
    #exit()


 
#python3 mercado_libre_UNO.py "comprar narvarte"
#python3 mercado_libre_UNO.py "comprar" "departamento" "narvarte"


    
#if len(sys.argv==1):
    #opera=sys.argv[1]
    #cuadro=opera.replace(" ","%20")
    #operation=opera.replace(" ","-")
    ##MODIFICAR MERCADO LIBRE PARA LAS CATEGORIAS Y LOS OPERACIONES
    #https://inmuebles.mercadolibre.com.mx/casas/venta/distrito-federal/benito-juarez   
    #https://inmuebles.mercadolibre.com.mx/departamentos/venta/distrito-federal/benito-juarez
    #https://inmuebles.mercadolibre.com.mx/terrenos/venta/distrito-federal/benito-juarez
    #https://inmuebles.mercadolibre.com.mx/oficinas/venta/distrito-federal/benito-juarez
    #https://inmuebles.mercadolibre.com.mx/locales-comerciales/venta/distrito-federal/benito-juarez
    #https://inmuebles.mercadolibre.com.mx/bodegas/venta/distrito-federal/benito-juarez
    

opera=sys.argv[1]
if opera in ["compra","comprar","venta"]:
    operation=["venta/"]

if opera in ["renta","rentar"]:
    operation=["renta/"]
    

if len(sys.argv)==3:
    print("BUSCA EN TODOS LOS TIPOS DE LAS PROPIEDADES")
    categories=["casas/","departamentos/","terrenos/","oficinas/","edificios/","locales-comerciales/","bodegas/"]
    query=sys.argv[2].replace(" ","-")
    category="TODO"
    
if len(sys.argv)==4 or len(sys.argv)==5:      
    category=sys.argv[2]
    categories=""

    if category in ["departamento","departamentos"]:
        categories=["departamentos/"]

    if category in ["casa","casas"]:
        categories=["casas/"]


    if category in ["terreno","terrenos"]:
        categories=["terrenos/"]
        
     
    if category in ["oficina","oficinas"]:
        categories=["oficinas/"]

    if category in ["bodega"]:
        categories=["bodegas/"]

 
        
    if category in ["edificio","edificios"]:
        categories=["edificios/"]
        
    if category in ["local","locales"]:
        categories=["locales-comerciales/"]
        
    query=sys.argv[3].replace(" ","-")
    print("llega")
    if categories=="":
        categories=["casas/","departamentos/","terrenos/","oficinas/","edificios/","locales-comerciales/","bodegas/"]
    
        
   # catego opera   query   
   #/casas/venta/comprar-colonia-del-valle
   
     
 
    
print("args: "+ str(len(sys.argv)))
   
# Asigna formato de ejemplo1
formato1 = "%d_%m_%Y"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\MERCADO_LIBRE\\"
if os.path.exists(path):
    pass
else:
     
    os.mkdir(path)

    
path=str(Path().absolute())+"\\MERCADO_LIBRE\\"+str(opera)+"_"+str(category)+"_"+str(query)+"_"+hoy

print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)

f= open(path+"\\"+opera+"_"+category+".csv","w+")
        								                                                                                                                                			
f.write("\"URL\","+"\"PRECIO\","+"\"TIPO\","+"\"CATEGORIA\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"TERRENO\","+"\"CONSTRUIDOS\","+"\"BAÑOS\","+"\"ESTACIONAMIENTO\","+"\"RECAMARAS\","+"\"MEDIOS BAÑOS\","+"\"ANTIGÜEDAD\","+"\"CALLE\","+"\"COLONIA\","+"\"DELEGACION\","+"\"CIUDAD\","+"\"PUBLICADO\"\n")

        

       

for op in operation:
   
    for cate in categories: 
        print("OPERACION: " +str(op)+ " CATEGORIA: "+ str(cate))
        if len(sys.argv)<5:  
            URL='https://inmuebles.mercadolibre.com.mx/'+str(cate)+str(op)+'distrito-federal/'+str(query)

        if len(sys.argv)==5: 
            URL='https://inmuebles.mercadolibre.com.mx/'+str(cate)+str(op)+'distrito-federal/'+str(query)+"/"+str(sys.argv[4].replace(" ","-"))+"/"
           
        elements,soup=navega_page(URL)

        #no_results=soup.find('div', class_='no-results__message')
                
        #if no_results!=None:
            
        Total_pages = soup.find('div', class_='quantity-results')
        print(Total_pages.text)
        
        Total_pages=str(Total_pages.text).split()
                #print(Total_pages)
        Total_pages=str(Total_pages[0]).replace(",","") 
                #print(Total_pages)
        Total_pages=int(Total_pages)/48
                #print(Total_pages)
        Total_pages=my_round(Total_pages+0.5)


        print(str(Total_pages) + "paginas")



        #exit();        
              
         #/casas/venta/distrito-federal/benito-juarez_Desde_49
        for pages in range(1,Total_pages+1) :
            list_url=list() 
            print("PAGINA"+ str(pages))
        
            #f.write(URL+"|")
            headers = {'User-Agent': 'Mozilla/5.0'}
            if pages==1:
                page = requests.get(URL, headers=headers)
                print(URL)
            else:
                pagina=pages-1
                pagina=(int(pagina)*47)+2
                URL='https://inmuebles.mercadolibre.com.mx/'+str(cate)+str(op)+'distrito-federal/'+str(query)+'_Desde_'+str(pagina)
                print(URL)
                page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            #time.sleep(5)
        
            
            results = soup.find('div', class_='inner-main')
            
            elements = results.find('ol', id='searchResults')
            
            elements=elements.find_all('div', class_='images-viewer')
            #for item in elements:
                #print(item['item-url'])
            #print(elements)
            
            #print(elements)
            for job_elem in elements:
                title_elem = job_elem.find('img')['alt']
                #print(title_elem)
            
                a_href = job_elem['item-url']
                #print(a_href)
                
                
                if None in (title_elem, a_href):
                    print("continua")
                    continue
                if "articulo.mercadolibre" in a_href:
                    pass
                else:
                    list_url.append(a_href)
        
    
#print(len(list_url))
 
             
            for item in list_url:        
                #f.write("\""+item.lstrip().rstrip()+"\",")
                navega_cada_pagina(item,op,cate)
f.close() 



