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

def navega_page(pagina_numero,catego,op,query):
    URL = 'https://www.propiedades.com/'+str(query)+'/'+catego+op+"?pagina="+str(pagina_numero)
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='content-result cont-search-list')
    #elements = results.select('div[class*="posting-card"]')
    return soup


 


def navega_cada_pagina(pagina,op,cate):
    URL = pagina
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    OPERACION(soup,pagina,op,cate)
     
        




def OPERACION(soup,pagina,op,cate):
    try:
        precio = soup.find('span', class_='price')
    #print(precio.text.lstrip().rstrip())
        f.write("\""+pagina.lstrip().rstrip()+"\",")
        f.write("\""+precio.text.lstrip().rstrip()+"\",")
        f.write("\""+op.replace("-","")+"\",")
    except:
        return False
    
    if cate in ["casas-en-condominio"]:
            file_catego="casas"
    else:
            file_catego=cate
    f.write(file_catego+",")
    
    
    nombre = soup.find('h1', class_='title-gallery').find('em')
       
        #f.write(nombre.text.lstrip().rstrip()+"|")
    nombre=nombre
    nombre=nombre.text.lstrip().rstrip()
    nombre=nombre.replace(",","")
    nombre=nombre.replace("\"","")
    f.write("\""+nombre+"\",")
  
        
    Descripcion = soup.find('div', class_='subsection-content').find_all('p')    
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
            Descripcion=str(item.text)
            a="Este porcentaje muestra el valor de la propiedad con respecto a la tendencia de los precios de la zona."
            b="Aunque haya un precio medio en una colonia, cada vivienda cuenta con particularidades que podrían incrementar o disminuir el valor."
            c="El porcentaje se ofrece solo como una guía y podría no reflejar el valor particular de la propiedad."
            
            Descripcion=Descripcion.replace(a,"").replace(b,"").replace(c,"").replace("!","").replace("¡","").replace("\"","")
            #print(Descripcion)
            try:
                f.write("\""+str(Descripcion)+"\",")
            except:
                bandera=True    
            break
    
    
    if bandera   :
        Descripcion="None"
        f.write("\""+Descripcion+"\",")
   
    
    status = soup.find('ul', class_='carac-large')
    columns = status.find_all('li')
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
        
 
    #print("\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\",")    
    items_data="\""+str(terreno)+"\","+"\""+str(construidos)+"\","+"\""+str(banios)+"\","+"\""+str(estacionamientos)+"\","+"\""+str(Recamaras)+"\","+"\""+str(Medios)+"\","+"\""+str(Antiguedad)+"\","
    f.write(items_data)
 
    calle="None"
    colonia="None"
    delegacion="None"
    ciudad="None"   
        
    location=soup.find('h1',class_='title-gallery').find_all('span')
     
    
    #location=location.split(",")
    #print(location)
    items_data2="\""+str(calle)+"\","+"\""+str(location[0]).replace("\n","").replace("<span>","").replace("</span>","").replace(",","")+"\","+"\""+str(location[2]).replace("\n","").replace("<span>","").replace("</span>","").replace(",","").replace("\"","").replace("<span itemprop=addressLocality","").replace(">","")+"\","+"\""+str(location[5]).replace("\n","").replace("<span>","").replace("</span>","").replace(",","").replace("\"","").replace("<span itemprop=addressRegion","").replace(">","")+"\","
    f.write(items_data2)
     
    #f.write("\""+location+"\",")
    publicado=soup.find('p',class_='info-update')
 
    
    if publicado!=None:
        
        publicado=publicado.text
    else:
        publicado="None"
    #print (publicado)
    publicado=publicado.replace("Propiedad actualizada el:","").lstrip().rstrip()
    f.write("\""+publicado+"\"\n")
    #exit()
    




#python3 scrap_uno.py "comprar" "departamento" "narvarte"

#operation=["en-venta-","en-renta-","desarrollos-","oficinas-","en-temporal-vacacional-","en-venta-incluir-comercializa-remates-publisher-"]
#categories=["departamentos-","casas-o-duplex-o-casa-en-condominio-","casa-en-condominio-","oficinas-","locales-comerciales-","bodegas-comerciales-","terrenos-","otros-tipos-de-propiedades-"]

opera=sys.argv[1]
if opera in ["compra","comprar","venta"]:
    operation=["-venta"]

if opera in ["renta","rentar"]:
    operation=["-renta"]
        

       
category=sys.argv[2]


if category in ["desarrollo","desarrollos"]:
    categories=["desarrollos"]

if category in ["departamento","departamentos"]:
    categories=["departamentos"]

if category in ["casa","casas"]:
    categories=["casas"]
    
if category in ["rancho","ranchos"]:
    categories=["ranchos"]


if category in ["terreno habitacional","terrenos habitacionales"]:
    categories=["terrenos-habitacionales"]
    
if category in ["casas en condominio","condominio"]:
    categories=["casas-en-condominio"]     






if category in ["oficina","oficinas"]:
    categories=["oficinas"]

if category in ["bodega"]:
    categories=["bodegas-comerciales"]

if category in ["terrenos comerciales","terreno comercial"]:
    categories=["terrenos-comerciales"]
    
if category in ["edificio","edificios"]:
    categories=["edificios"]
    
if category in ["local","locales"]:
    categories=["locales"]
    
#





query=sys.argv[3]
if query is None:
    exit
    
# Asigna formato de ejemplo1
formato1 = "%d_%m_%Y"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\PROPIEDADES_COM\\"
if os.path.exists(path):
    pass
else:
     
    os.mkdir(path)
    
path=str(Path().absolute())+"\\PROPIEDADES_COM\\"+str(opera)+"_"+str(category)+"_"+str(query)+"_"+hoy
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
        
           
        soup=navega_page(str(counter),cate,op,query)
        
        no_results=soup.find('div', class_='content-errors')
        if no_results!=None:
            continue
        Total_pages = soup.find('div', class_='title-result')
       
        Total_pages=Total_pages.find('span').text
        print(str(Total_pages)+" resultados")
        Total_pages=int(Total_pages)/42
        #print(Total_pages)
        Total_pages=my_round(Total_pages+0.5)


        print(str(Total_pages) + " paginas" )
         

        
        
        for pages in range(1,Total_pages+1) :
            list_url=list()
 
 
            print("PAGINA:"+ str(pages))
            soup =  navega_page(pages,cate,op,query)
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
                
                counter+=1
         
            for item in list_url:
            
                        
                
                navega_cada_pagina(item,op,cate)

f.close() 



