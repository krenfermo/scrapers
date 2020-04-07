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

def navega_cada_pagina(pagina):
    URL = pagina
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('h1', class_='item-title__primary')
    
    if results!=None:
       venta(soup)
        




def venta(soup):
    
    precio = soup.find('span', class_='price-tag-fraction')
    #print(precio.text.lstrip().rstrip())
    f.write("\""+precio.text.lstrip().rstrip()+"\",")
    f.write("\"None\",")
 
    f.write("\"None\",")
 
    nombre = soup.find('header', class_='item-title')
    
    
    nombre=nombre.text.lstrip().rstrip()
    nombre=nombre.replace(",","")
    nombre=nombre.replace("\"","")
    f.write("\""+nombre+"\",")
    #f.write("\""+nombre.text.lstrip().rstrip()+"\",")
    
    try:    
        Descripcion = soup.find('div', class_='item-description__text')    
        Descripcion=Descripcion.find('p')
   
        Descripcion= Descripcion.text
    except:
        Descripcion="None"
    
   
     
    Descripcion=Descripcion.replace("\"","")
    f.write("\""+Descripcion+"\",")
    #f.write("\""+Descripcion.text+"\",")
    
    status = soup.find('ul', class_='specs-list')
    columns = status.find_all('li', class_='specs-item')
    terreno="None"
    construidos="None"
    banios="None"
    estacionamientos="None"
    Recamaras="None"
     
    
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
        

         
     
    items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str("None")+"\","+"\""+str("None")+"\","
    f.write(items_data)
        
     
    colonia="None"
    delegacion="None"
    ciudad="None"   
    try:    
        location=soup.find('div',class_='seller-location')
        print(location.text.lstrip().rstrip())   
        
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
    
    
    f.write(items_data2)
    f.write("\"None\",")
    f.write("\n")
    #exit()



 
    
 

#python3 mercado_libre_UNO.py "comprar departamento narvarte"

 
opera=sys.argv[1]
cuadro=opera.replace(" ","%20")
operation=opera.replace(" ","-")
URL='https://listado.mercadolibre.com.mx/'+operation+'#D[A:'+cuadro+']'
print(URL)
#https://listado.mercadolibre.com.mx/rentar-casa-condesa#D[A:rentar%20casa%20condesa]



    
# Asigna formato de ejemplo1
formato1 = "%d_%m_%Y"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\"+str("MERCADO")+str(opera)+"_"+hoy
print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)

f= open(path+"\\"+operation+".csv","w+")
        								                                                                                                                                			
f.write("\"URL\","+"\"PRECIO\","+"\"TIPO\","+"\"CATEGORIA\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"TERRENO\","+"\"CONSTRUIDOS\","+"\"BAÑOS\","+"\"ESTACIONAMIENTO\","+"\"RECAMARAS\","+"\"MEDIOS BAÑOS\","+"\"ANTIGÜEDAD\","+"\"CALLE\","+"\"COLONIA\","+"\"DELEGACION\","+"\"CIUDAD\","+"\"PUBLICADO\"\n")

        

        
elements,soup=navega_page(URL)

#no_results=soup.find('div', class_='no-results__message')
        
#if no_results!=None:
    
Total_pages = soup.find('div', class_='quantity-results')
print(Total_pages.text)
 
Total_pages=str(Total_pages.text).split()
        #print(Total_pages)
Total_pages=str(Total_pages[0]) 
        #print(Total_pages)
Total_pages=int(Total_pages)/48
        #print(Total_pages)
Total_pages=my_round(Total_pages+0.5)


print(Total_pages)



#exit();        
list_url=list()       

for pages in range(1,Total_pages+1) :
    
 
    #f.write(URL+"|")
    headers = {'User-Agent': 'Mozilla/5.0'}
    if pages==1:
        page = requests.get(URL, headers=headers)
    else:
        pagina=pages-1
        pagina=(int(pagina)*47)+2
        URL='https://listado.mercadolibre.com.mx/'+operation+'_Desde_'+str(pagina)
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
    f.write("\""+item.lstrip().rstrip()+"\",")
    navega_cada_pagina(item)
f.close() 



