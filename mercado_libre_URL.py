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
    
   
    #URL=URL.replace("//_","/_")
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='inner-main')
    
    elements = results.find('ol', id='searchResults')
    return elements,soup

def navega_cada_pagina(pagina,colonia):
    URL = pagina
    #URL=URL.replace("//_","/_")
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('h1', class_='item-title__primary')
    
    if results!=None:
       venta(soup,pagina,colonia)
        

    

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


def venta(soup,pagina,colonia):
    try:
        precio = soup.find('span', class_='price-tag-fraction')
        f.write("\""+pagina.lstrip().rstrip()+"\",")
        f.write("\""+precio.text.lstrip().rstrip()+"\",")
        operation="None"
        if "venta" in pagina:
            operation="Venta"
        if "renta" in pagina:
            operation="Renta"
        f.write("\""+operation+"\",")
        
        
    except:
        return False
    
        

    
    file_catego="None"
    if "casa" in pagina:
        file_catego="Casa"
    elif "departamento" in pagina:
        file_catego="Departamento"
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
        
     
    #colonia="None"
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
            #colonia=location[0]
            delegacion=location[1]
            ciudad=location[2]
            items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
            
    except:
        location="None"
        #colonia="None"
        delegacion="None"
        ciudad="None"
        calle="None"
        
        items_data2="\""+str(calle)+"\","+"\""+str(colonia)+"\","+"\""+str(delegacion)+"\","+"\""+str(ciudad)+"\","
    
    
    f.write(normalize(str(items_data2)))
    f.write("\"None\",")
    f.write("\n")
    #exit()


def cuerpo(URL,colonia):
    
    URL_modificada= URL.split("_Desde_") 
    URL=str(URL_modificada[0])+str(colonia)+"_Desde_1"
    
    #exit()
    
    
    try: 
        elements,soup=navega_page(URL)
    except:
        return False

        
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
    
    URL2=URL
    
    URL2=URL2.split("_Desde_")
 
    print("URL2:"+str(URL2))
    
    
    
    for pages in range(1,Total_pages+1) :
        try:
            list_url=list() 
            print("PAGINA"+ str(pages))

            #f.write(URL+"|")
            headers = {'User-Agent': 'Mozilla/5.0'}
            if pages==1:
                URL2=URL2[0].split("_Desde_")
                print("URL2_0:"+str(URL2))
                URL3=str(URL2[0])+"_Desde_"+str(pages)
                
                print(URL3)
               
                page = requests.get(URL3, headers=headers)
                
            else:
                pagina=pages-1
                pagina=(int(pagina)*47)+2
                URL4=str(URL2[0])+"_Desde_"+str(pagina)
                
                print(URL4)
                page = requests.get(URL4, headers=headers)
             
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



                
            for item in list_url:        
                #f.write("\""+item.lstrip().rstrip()+"\",")
                navega_cada_pagina(item,colonia)
        except:
            continue



URL=sys.argv[1]
     
#['algarin','ampliacion-asturias','asturias','asturias-amp','atlampa','buenavista','buenos-aires','centro-de-la-ciudad-de-mexico-area-1','centro-de-la-ciudad-de-mexico-area-2','centro-de-la-ciudad-de-mexico-area-3','centro-de-la-ciudad-de-mexico-area-4','centro-de-la-ciudad-de-mexico-area-5','centro-de-la-ciudad-de-mexico-area-6','centro-de-la-ciudad-de-mexico-area-7','centro-de-la-ciudad-de-mexico-area-8','centro-de-la-ciudad-de-mexico-area-9','centro-de-recepcion-de-depositos-masivos-centro','centro-urbano-benito-juarez','condesa','cuauhtemoc','doctores','esperanza','ex-hipodromo-de-peralvillo','felipe-pescador','guerrero','h-camara-de-senadores','hipodromo-condesa','hipodromo','juarez','maza','morelos','nonoalco-tlatelolco','obrera','otros','paseo-de-la-reforma','paulino-navarro','peralvillo','procuraduria-general-de-la-republica','roma-norte','roma-sur','san-rafael','san-simon-tolnahuac','santa-maria-insurgentes','santa-maria-la-ribera','tabacalera','transito','valle-gomez','vista-alegre']
#['10-de-abril','5-de-mayo','agricultura','ahuehuetes-anahuac','ampliacion-daniel-garza','ampliacion-granada','ampliacion-torre-blanca','america','anahuac','anahuac-i-seccion','anahuac-ii-seccion','anzures','anahuac-ii-secc','argentina-antigua','argentina-poniente','bosque-de-chapultepec','bosque-de-chapultepec-i-seccion','bosque-de-chapultepec-ii-seccion','bosque-de-chapultepec-iii-seccion','bosque-de-las-lomas','chapultepec-morales','cinco-de-mayo','cuauhtemoc-pensil','daniel-garza','daniel-garza-amp','delegacion-politica-miguel-hidalgo','deportivo-pensil','dos-lagos','equipamiento-bosque-de-chapultepec-i-seccion','escandon','escandon-i-secc','escandon-i-seccion','escandon-ii-seccion','francisco-i-madero','granada','granada-amp','huichapan','irrigacion'] 


#['8-de-agosto','acacias','actipan','alamos','albert','ampliacion-napoles','americas-unidas','atenor-salas','centro-urbano-presidente-miguel-aleman','ciudad-de-los-deportes','colonia-del-valle','colonia-narvarte-oriente','credito-constructor','del-carmen','del-lago','del-valle-centro','del-valle-norte','del-valle-sur','emperadores','ermita','extremadura-insurgentes','general-pedro-maria-anaya','gral-pedro-maria-anaya','independencia','insurgentes-mixcoac','insurgentes-san-borja','iztaccihuatl','josefa-ortiz-de-dominguez','letran-valle']
if URL == "https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/cuauhtemoc/_Desde_49":   
    #COLONIAS=['algarin','ampliacion-asturias','asturias','asturias-amp','atlampa','buenavista','buenos-aires','centro-de-la-ciudad-de-mexico-area-1','centro-de-la-ciudad-de-mexico-area-2','centro-de-la-ciudad-de-mexico-area-3','centro-de-la-ciudad-de-mexico-area-4','centro-de-la-ciudad-de-mexico-area-5','centro-de-la-ciudad-de-mexico-area-6','centro-de-la-ciudad-de-mexico-area-7','centro-de-la-ciudad-de-mexico-area-8','centro-de-la-ciudad-de-mexico-area-9','centro-de-recepcion-de-depositos-masivos-centro','centro-urbano-benito-juarez','condesa','cuauhtemoc/','doctores','esperanza','ex-hipodromo-de-peralvillo','felipe-pescador','guerrero','h-camara-de-senadores','hipodromo-condesa','hipodromo','juarez','maza','morelos','nonoalco-tlatelolco','obrera','otros','paseo-de-la-reforma','paulino-navarro','peralvillo','procuraduria-general-de-la-republica','roma-norte','roma-sur','san-rafael','san-simon-tolnahuac','santa-maria-insurgentes','santa-maria-la-ribera','tabacalera','transito','valle-gomez','vista-alegre']
    COLONIAS=['cuauhtemoc/','doctores','esperanza','ex-hipodromo-de-peralvillo','felipe-pescador','guerrero','h-camara-de-senadores','hipodromo-condesa','hipodromo','juarez','maza','morelos','nonoalco-tlatelolco','obrera','otros','paseo-de-la-reforma','paulino-navarro','peralvillo','procuraduria-general-de-la-republica','roma-norte','roma-sur','san-rafael','san-simon-tolnahuac','santa-maria-insurgentes','santa-maria-la-ribera','tabacalera','transito','valle-gomez','vista-alegre']

if URL == "https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/cuauhtemoc/_Desde_49":   
    COLONIAS=['algarin','ampliacion-asturias','asturias','asturias-amp','atlampa','buenavista','buenos-aires','centro-de-la-ciudad-de-mexico-area-1','centro-de-la-ciudad-de-mexico-area-2','centro-de-la-ciudad-de-mexico-area-3','centro-de-la-ciudad-de-mexico-area-4','centro-de-la-ciudad-de-mexico-area-5','centro-de-la-ciudad-de-mexico-area-6','centro-de-la-ciudad-de-mexico-area-7','centro-de-la-ciudad-de-mexico-area-8','centro-de-la-ciudad-de-mexico-area-9','centro-de-recepcion-de-depositos-masivos-centro','centro-urbano-benito-juarez','condesa','cuauhtemoc/','doctores','esperanza','ex-hipodromo-de-peralvillo','felipe-pescador','guerrero','h-camara-de-senadores','hipodromo-condesa','hipodromo','juarez','maza','morelos','nonoalco-tlatelolco','obrera','otros','paseo-de-la-reforma','paulino-navarro','peralvillo','procuraduria-general-de-la-republica','roma-norte','roma-sur','san-rafael','san-simon-tolnahuac','santa-maria-insurgentes','santa-maria-la-ribera','tabacalera','transito','valle-gomez','vista-alegre']




if URL =="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/benito-juarez/_Desde_49":
    COLONIAS=['8-de-agosto','acacias','actipan','alamos','albert','ampliacion-napoles','americas-unidas','atenor-salas','centro-urbano-presidente-miguel-aleman','ciudad-de-los-deportes','colonia-del-valle','colonia-narvarte-oriente','credito-constructor','del-carmen','del-lago','del-valle-centro','del-valle-norte','del-valle-sur','emperadores','ermita','extremadura-insurgentes','general-pedro-maria-anaya','gral-pedro-maria-anaya','independencia','insurgentes-mixcoac','insurgentes-san-borja','iztaccihuatl','josefa-ortiz-de-dominguez','letran-valle','maria-del-carmen','merced-gomez','miguel-aleman','miravalle','mixcoac','moderna','narvarte','narvarte-oriente','narvarte-poniente','nativitas','ninos-heroes','ninos-heroes-de-chapultepec','nochebuena','nonoalco','napoles','napoles-amp','ocho-de-agosto','otros','periodista','piedad-narvarte','portales','portales-norte','portales-oriente','portales-sur','postal','residencial-emperadores','san-jose-insurgentes','san-juan','san-pedro-de-los-pinos','san-simon-ticumac','santa-cruz-atoyac','santa-maria-nonoalco','tlacoquemecatl','tlacoquemecatl-del-valle','villa-de-cortes','vertiz-narvarte','xoco','zacahuitzco']

if URL =="https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/benito-juarez/_Desde_49":
    COLONIAS=['8-de-agosto','acacias','actipan','alamos','albert','ampliacion-napoles','americas-unidas','atenor-salas','centro-urbano-presidente-miguel-aleman','ciudad-de-los-deportes','colonia-del-valle','colonia-narvarte-oriente','credito-constructor','del-carmen','del-lago','del-valle-centro','del-valle-norte','del-valle-sur','emperadores','ermita','extremadura-insurgentes','general-pedro-maria-anaya','gral-pedro-maria-anaya','independencia','insurgentes-mixcoac','insurgentes-san-borja','iztaccihuatl','josefa-ortiz-de-dominguez','letran-valle','maria-del-carmen','merced-gomez','miguel-aleman','miravalle','mixcoac','moderna','narvarte','narvarte-oriente','narvarte-poniente','nativitas','ninos-heroes','ninos-heroes-de-chapultepec','nochebuena','nonoalco','napoles','napoles-amp','ocho-de-agosto','otros','periodista','piedad-narvarte','portales','portales-norte','portales-oriente','portales-sur','postal','residencial-emperadores','san-jose-insurgentes','san-juan','san-pedro-de-los-pinos','san-simon-ticumac','santa-cruz-atoyac','santa-maria-nonoalco','tlacoquemecatl','tlacoquemecatl-del-valle','villa-de-cortes','vertiz-narvarte','xoco','zacahuitzco']


if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/miguel-hidalgo/_Desde_49":
    COLONIAS=['10-de-abril','5-de-mayo','agricultura','ahuehuetes-anahuac','ampliacion-daniel-garza','ampliacion-granada','ampliacion-torre-blanca','america','anahuac','anahuac-i-seccion','anahuac-ii-seccion','anzures','anahuac-ii-secc','argentina-antigua','argentina-poniente','bosque-de-chapultepec','bosque-de-chapultepec-i-seccion','bosque-de-chapultepec-ii-seccion','bosque-de-chapultepec-iii-seccion','bosque-de-las-lomas','chapultepec-morales','cinco-de-mayo','cuauhtemoc-pensil','daniel-garza','daniel-garza-amp','delegacion-politica-miguel-hidalgo','deportivo-pensil','dos-lagos','equipamiento-bosque-de-chapultepec-i-seccion','escandon','escandon-i-secc','escandon-i-seccion','escandon-ii-seccion','francisco-i-madero','granada','granada-amp','huichapan','irrigacion','lago-sur','legaria','lomas-altas','lomas-de-bezares','lomas-de-chapultepec','lomas-de-chapultepec-8a-secc','lomas-de-chapultepec-i-secc','lomas-de-chapultepec-i-seccion','lomas-de-chapultepec-ii-secc','lomas-de-chapultepec-ii-seccion','lomas-de-chapultepec-iii-secc','lomas-de-chapultepec-iii-seccion','lomas-de-chapultepec-iv-seccion','lomas-de-chapultepec-v-secc','lomas-de-chapultepec-v-seccion','lomas-de-chapultepec-vi-secc','lomas-de-chapultepec-vi-seccion','lomas-de-chapultepec-vii-secc','lomas-de-chapultepec-vii-seccion','lomas-de-chapultepec-viii-secc','lomas-de-chapultepec-viii-seccion','lomas-de-reforma','lomas-de-sotelo','lomas-hermosa','lomas-virreyes','los-manzanos','los-morales','manuel-avila-camacho','mariano-escobedo','modelo-pensil','molino-del-rey','mexico-nuevo','mexico-tacuba','nextitla','nueva-anzures','observatorio','otros','pensil-norte','pensil-sur','periodista','plutarco-elias-calles','polanco','popo','popotla','real-de-las-lomas','reforma-pensil','reforma-social','residencia-oficial-de-los-pinos','san-diego-ocoyoacac','san-joaquin','san-juanico','san-lorenzo-tlaltenango','san-miguel-chapultepec','san-miguel-chapultepec-i-seccion','san-miguel-chapultepec-ii-seccion','santo-tomas','tacuba','tacubaya','tlaxpana','torreblanca','torreblanca-amp','un-hogar-para-nosotros','ventura-perez-de-alva','veronica-anzures'] 
if URL=="https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/miguel-hidalgo/_Desde_49":
    COLONIAS=['10-de-abril','5-de-mayo','agricultura','ahuehuetes-anahuac','ampliacion-daniel-garza','ampliacion-granada','ampliacion-torre-blanca','america','anahuac','anahuac-i-seccion','anahuac-ii-seccion','anzures','anahuac-ii-secc','argentina-antigua','argentina-poniente','bosque-de-chapultepec','bosque-de-chapultepec-i-seccion','bosque-de-chapultepec-ii-seccion','bosque-de-chapultepec-iii-seccion','bosque-de-las-lomas','chapultepec-morales','cinco-de-mayo','cuauhtemoc-pensil','daniel-garza','daniel-garza-amp','delegacion-politica-miguel-hidalgo','deportivo-pensil','dos-lagos','equipamiento-bosque-de-chapultepec-i-seccion','escandon','escandon-i-secc','escandon-i-seccion','escandon-ii-seccion','francisco-i-madero','granada','granada-amp','huichapan','irrigacion','lago-sur','legaria','lomas-altas','lomas-de-bezares','lomas-de-chapultepec','lomas-de-chapultepec-8a-secc','lomas-de-chapultepec-i-secc','lomas-de-chapultepec-i-seccion','lomas-de-chapultepec-ii-secc','lomas-de-chapultepec-ii-seccion','lomas-de-chapultepec-iii-secc','lomas-de-chapultepec-iii-seccion','lomas-de-chapultepec-iv-seccion','lomas-de-chapultepec-v-secc','lomas-de-chapultepec-v-seccion','lomas-de-chapultepec-vi-secc','lomas-de-chapultepec-vi-seccion','lomas-de-chapultepec-vii-secc','lomas-de-chapultepec-vii-seccion','lomas-de-chapultepec-viii-secc','lomas-de-chapultepec-viii-seccion','lomas-de-reforma','lomas-de-sotelo','lomas-hermosa','lomas-virreyes','los-manzanos','los-morales','manuel-avila-camacho','mariano-escobedo','modelo-pensil','molino-del-rey','mexico-nuevo','mexico-tacuba','nextitla','nueva-anzures','observatorio','otros','pensil-norte','pensil-sur','periodista','plutarco-elias-calles','polanco','popo','popotla','real-de-las-lomas','reforma-pensil','reforma-social','residencia-oficial-de-los-pinos','san-diego-ocoyoacac','san-joaquin','san-juanico','san-lorenzo-tlaltenango','san-miguel-chapultepec','san-miguel-chapultepec-i-seccion','san-miguel-chapultepec-ii-seccion','santo-tomas','tacuba','tacubaya','tlaxpana','torreblanca','torreblanca-amp','un-hogar-para-nosotros','ventura-perez-de-alva','veronica-anzures'] 
  
  

if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/alvaro-obregon/_Desde_49":
   COLONIAS=['19-de-mayo','1a-amp-presidentes','1a-ampliacion-presidentes','1a-secc-canada','1a-seccion-canada','2a-ampliacion-presidentes','2do-reacomodo-tlacuitlapa','8-de-agosto','abraham-m-gonzalez','aguila-real','alcantarilla','alfalfar','alfonso-xiii','altavista','ampliacion-alpes','ampliacion-las-aguilas','ampliacion-piloto-adolfo-lopez-mateos','arcos-centenario','atlamaya','ave-real','axomiatla','axotla','balcones-de-cehuayo','barrio-el-capulin','barrio-norte','batallon-de-san-patricio','bellavista','belem-de-las-flores','belen','bosque','bosques-de-santa-fe','bosques-de-tarango','camino-real-de-tetelpan','campestre','canutillo','canutillo-3a-seccion','carola','canada-del-olivar','chimalistac','colina-del-sur','colinas-de-tarango','colinas-del-sur','colonia-golondrinas','colonia-progreso-tizapan','corpus-christi-2do-reacomodo','corpus-christi-amp','corpus-christy','cove','cuernito-becerra-reacomodo','cuevitas','delegacion-politica-alvaro-obregon','desarrollo-santa-fe','desarrollo-urbano','el-capulin-amp','el-cuernito','el-encino-del-pueblo-tetelpan','el-olivarito','el-paraiso','el-piru','el-rincon','ermita-tizapan','estado-de-hidalgo','estado-de-hidalgo-amp','ex-hacienda-de-guadalupe-chimalistac','flor-de-maria','florida','garcimarrero','golondrinas','golondrinas-1a-seccion','guadalupe-inn','heron-proal','hidalgo','hueytlale','infonavit','isidro-fabela','jardines-del-pedregal','jose-maria-pino-suarez','la-angostura','la-cascada','la-herradura-san-angel','la-joyita-del-pueblo-tetelpan','la-loma','la-loma-sta-fe','la-martinica','la-mexicana','la-otra-banda','la-palmita','las-aguilas','las-aguilas-1a-seccion','las-aguilas-amp','las-aguilas-amp-1er-parque','las-aguilas-amp-3er-parque','las-americas','las-golondrinas-1a-secc','las-haciendas','las-aguilas-2o-parque','las-aguilas-3er-parque','llano-redondo','lomas-axomiatla','lomas-de-axomiatla','lomas-de-becerra','lomas-de-guadalupe','lomas-de-la-era','lomas-de-las-aguilas','lomas-de-los-angeles-de-tetelpan','lomas-de-los-angeles-del-pueblo-tetelpan','lomas-de-los-cedros','lomas-de-plateros','lomas-de-puerta-grande','lomas-de-san-angel-inn','lomas-de-santa-fe','lomas-de-tarango','lomas-de-tarango-reacomodo','lomas-del-capulin','lomas-del-cedro','loreto','los-alpes','los-alpes-amp','los-cedros','maria-g-de-garcia-ruiz','merced-gomez','miguel-hidalgo','minas-de-cristo','mixcoac','molino-de-rosas','molino-de-santo-domingo','ocotillos','ocotillos-del-pueblo-tetelpan','olivar-de-los-padres','olivar-del-conde','olivar-del-conde-1a-secc-amp','olivar-del-conde-1a-seccion','olivar-del-conde-2a-secc','olivar-del-conde-2a-secc-amp','otros','palmas','paraiso','paseo-de-las-lomas','pedregal','pena-blanca-santa-fe','pilares-aguilas','piloto-adolfo-lopez-mateos','ponciano-arriaga','preconcreto','presidentes','profesor-j-arturo-lopez-martinez','progreso-san-angel','progreso-tizapan','pueblo-nuevo','puente-colorado','puerta-grande','puntaxa0dexa0cehuaya','rancho-san-francisco','rancho-san-francisco-pueblo-san-bartolo-ameyalco','reacomodo-valentin-gomez-farias','residencial-de-tarango','rinconada-de-tarango','rincon-centenario','sacramento','san-agustin','san-agustin-del-pueblo-tetelpan','san-angel','san-angel-inn','san-bartolo-ameyalco','san-clemente','san-clemente-norte','san-clemente-sur','san-francisco','san-gabriel','san-jeronimo-aculco','san-jose-del-olivar','san-pedro-de-los-pinos','santa-fe','santa-fe-centro-ciudad','santa-fe-imss','santa-fe-la-loma','santa-fe-pena-blanca','santa-fe-tlayapaca','santa-fe-amp','santa-lucia','santa-lucia-reacomodo','santa-maria-nonoalco','santa-rosa-xochiac','sears-roebuck','tarango','tecalcapa-del-pueblo-tetelpan','tetelpan','tetlalpan','tizampampano','tizampampano-del-pueblo-tetelpan','tizapan','tlacopac','tlacoyaque','tlacuitlapa','tlacuitlapa-1er-reacomodo','tlacuitlapa-2do-reacomodo','tolteca','torres-de-mixcoac','torres-de-potrero','u-h-belem-de-las-flores','unidad-lomas-de-plateros','unidad-santa-fe-imss','unidad-santa-fe-infonavit','valentin-gomez-farias','valentin-gomez-farias-reacomodo','victoria-primera-reacomodo','villa-verdun']       
   
if URL=="https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/alvaro-obregon/_Desde_49":
   COLONIAS=['19-de-mayo','1a-amp-presidentes','1a-ampliacion-presidentes','1a-secc-canada','1a-seccion-canada','2a-ampliacion-presidentes','2do-reacomodo-tlacuitlapa','8-de-agosto','abraham-m-gonzalez','aguila-real','alcantarilla','alfalfar','alfonso-xiii','altavista','ampliacion-alpes','ampliacion-las-aguilas','ampliacion-piloto-adolfo-lopez-mateos','arcos-centenario','atlamaya','ave-real','axomiatla','axotla','balcones-de-cehuayo','barrio-el-capulin','barrio-norte','batallon-de-san-patricio','bellavista','belem-de-las-flores','belen','bosque','bosques-de-santa-fe','bosques-de-tarango','camino-real-de-tetelpan','campestre','canutillo','canutillo-3a-seccion','carola','canada-del-olivar','chimalistac','colina-del-sur','colinas-de-tarango','colinas-del-sur','colonia-golondrinas','colonia-progreso-tizapan','corpus-christi-2do-reacomodo','corpus-christi-amp','corpus-christy','cove','cuernito-becerra-reacomodo','cuevitas','delegacion-politica-alvaro-obregon','desarrollo-santa-fe','desarrollo-urbano','el-capulin-amp','el-cuernito','el-encino-del-pueblo-tetelpan','el-olivarito','el-paraiso','el-piru','el-rincon','ermita-tizapan','estado-de-hidalgo','estado-de-hidalgo-amp','ex-hacienda-de-guadalupe-chimalistac','flor-de-maria','florida','garcimarrero','golondrinas','golondrinas-1a-seccion','guadalupe-inn','heron-proal','hidalgo','hueytlale','infonavit','isidro-fabela','jardines-del-pedregal','jose-maria-pino-suarez','la-angostura','la-cascada','la-herradura-san-angel','la-joyita-del-pueblo-tetelpan','la-loma','la-loma-sta-fe','la-martinica','la-mexicana','la-otra-banda','la-palmita','las-aguilas','las-aguilas-1a-seccion','las-aguilas-amp','las-aguilas-amp-1er-parque','las-aguilas-amp-3er-parque','las-americas','las-golondrinas-1a-secc','las-haciendas','las-aguilas-2o-parque','las-aguilas-3er-parque','llano-redondo','lomas-axomiatla','lomas-de-axomiatla','lomas-de-becerra','lomas-de-guadalupe','lomas-de-la-era','lomas-de-las-aguilas','lomas-de-los-angeles-de-tetelpan','lomas-de-los-angeles-del-pueblo-tetelpan','lomas-de-los-cedros','lomas-de-plateros','lomas-de-puerta-grande','lomas-de-san-angel-inn','lomas-de-santa-fe','lomas-de-tarango','lomas-de-tarango-reacomodo','lomas-del-capulin','lomas-del-cedro','loreto','los-alpes','los-alpes-amp','los-cedros','maria-g-de-garcia-ruiz','merced-gomez','miguel-hidalgo','minas-de-cristo','mixcoac','molino-de-rosas','molino-de-santo-domingo','ocotillos','ocotillos-del-pueblo-tetelpan','olivar-de-los-padres','olivar-del-conde','olivar-del-conde-1a-secc-amp','olivar-del-conde-1a-seccion','olivar-del-conde-2a-secc','olivar-del-conde-2a-secc-amp','otros','palmas','paraiso','paseo-de-las-lomas','pedregal','pena-blanca-santa-fe','pilares-aguilas','piloto-adolfo-lopez-mateos','ponciano-arriaga','preconcreto','presidentes','profesor-j-arturo-lopez-martinez','progreso-san-angel','progreso-tizapan','pueblo-nuevo','puente-colorado','puerta-grande','puntaxa0dexa0cehuaya','rancho-san-francisco','rancho-san-francisco-pueblo-san-bartolo-ameyalco','reacomodo-valentin-gomez-farias','residencial-de-tarango','rinconada-de-tarango','rincon-centenario','sacramento','san-agustin','san-agustin-del-pueblo-tetelpan','san-angel','san-angel-inn','san-bartolo-ameyalco','san-clemente','san-clemente-norte','san-clemente-sur','san-francisco','san-gabriel','san-jeronimo-aculco','san-jose-del-olivar','san-pedro-de-los-pinos','santa-fe','santa-fe-centro-ciudad','santa-fe-imss','santa-fe-la-loma','santa-fe-pena-blanca','santa-fe-tlayapaca','santa-fe-amp','santa-lucia','santa-lucia-reacomodo','santa-maria-nonoalco','santa-rosa-xochiac','sears-roebuck','tarango','tecalcapa-del-pueblo-tetelpan','tetelpan','tetlalpan','tizampampano','tizampampano-del-pueblo-tetelpan','tizapan','tlacopac','tlacoyaque','tlacuitlapa','tlacuitlapa-1er-reacomodo','tlacuitlapa-2do-reacomodo','tolteca','torres-de-mixcoac','torres-de-potrero','u-h-belem-de-las-flores','unidad-lomas-de-plateros','unidad-santa-fe-imss','unidad-santa-fe-infonavit','valentin-gomez-farias','valentin-gomez-farias-reacomodo','victoria-primera-reacomodo','villa-verdun']       
  
 
 
 
if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/coyoacan/_Desde_49":
    COLONIAS=['20-de-agosto','acasulco','adolfo-ruiz-cortines','ajusco','alianza-popular-revolucionaria','alianza-popular-revolucionaria-fovissste','altillo-universidad','atlantida','avante','barrio-del-nino-jesus','barrio-la-candelaria','barrio-la-concepcion','barrio-oxtopulco-universidad','barrio-san-francisco-culhuacan-barrio-de-la-magdalena','barrio-san-francisco-culhuacan-barrio-de-san-francisco','barrio-san-francisco-culhuacan-barrio-de-santa-ana','barrio-san-lucas','barrio-santa-catarina','bosques-de-tetlameya','cafetales','campestre-churubusco','campestre-coyoacan','cantil-del-pedregal','carmen-serdan','churubusco','churubusco-country-club','ciudad-jardin','colonia-culhuacan-ctm-seccion-x','colonia-ex-ejido-de-san-pablo-tepetlapa','colonia-ex-ejido-de-santa-ursula-coapa','colonia-ex-hacienda-coapa','colonia-presidentes-ejidales-1a-seccion','colonia-viejo-ejido-de-santa-ursula-coapa','concepcion','copilco','copilco-el-alto','copilco-el-bajo','copilco-universidad','country-club','coyoacan-centro','cuadrante-de-san-francisco','culhuacan-ctm-canal-nacional','culhuacan-ctm-croc','culhuacan-ctm-obrero-secc-10','culhuacan-ctm-obrero-secc-5','culhuacan-ctm-obrero-secc-6','culhuacan-ctm-obrero-secc-7','culhuacan-ctm-obrero-secc-8','culhuacan-ctm-obrero-secc-9','culhuacan-ctm-secc-iii','culhuacan-ctm-seccion-i','culhuacan-ctm-seccion-ii','culhuacan-ctm-seccion-iii','culhuacan-ctm-seccion-ix-a','culhuacan-ctm-seccion-ix-b','culhuacan-ctm-seccion-v','culhuacan-ctm-seccion-vi','culhuacan-ctm-seccion-vii','culhuacan-ctm-seccion-viii','culhuacan-ctm-seccion-x-a','culhuacan-piloto-5','del-carmen','delegacion-politica-coyoacan','educacion','el-caracol','el-centinela','el-hueso-infonavit','el-mirador','el-parque','el-parque-de-coyoacan','el-reloj','el-rosario','el-rosedal','emiliano-zapata','emiliano-zapata-fraccionamiento-popular','ermita-churubusco','espartaco','ex-ejido-san-pablo-tepetlapa','ex-ejido-santa-ursula-coapa','ex-ejido-de-san-francisco-culhuacan','ex-ejido-de-san-pablo-tepetlapa','ex-ejido-de-santa-ursula-coapa','ex-hacienda-coapa','fortin-de-chimalistac','fuentes-de-coyoacan','haciendas-de-coyoacan','hermosillo','insurgentes-cuicuilco','insurgentes-san-angel','integracion-latinoamericana','jardines-de-coyoacan','jardines-del-pedregal-de-san-angel','joyas-del-pedregal','la-candelaria-amp','la-concepcion','la-otra-banda','las-campanas','los-cedros','los-cipreses','los-girasoles','los-girasoles-2','los-girasoles-3','los-olivos','los-reyes','los-robles','los-sauces','nueva-diaz-ordaz','olimpica','otros','oxtopulco-universidad','parque-san-andres','paseos-de-taxquena','pedregal-de-carrasco','pedregal-de-coyoacan','pedregal-de-san-angel','pedregal-de-san-francisco','pedregal-de-santa-ursula','pedregal-de-santo-domingo','pedregal-del-maurel','pedregal-del-sur','petrolera-taxquena','prado-churubusco','prados-de-coyoacan','presidentes-ejidales','presidentes-ejidales-1a-seccion','presidentes-ejidales-2a-seccion','pueblo-de-los-reyes','pueblo-de-san-pablo-tepetlapa','pueblo-de-santa-ursula-coapa','pueblo-la-candelaria','residencial-cafetales','residencial-copilco','rinconada-de-los-reyes','romero-de-terreros','rosedal','san-diego-churubusco','san-francisco-culhuacan-barrio-de-san-francisco','san-mateo','san-pablo-tepetlapa','santa-cecilia','santa-ursula-coapa','stunam','taxquena','tetlameya','tlalpan','torres-de-chimalistac','torres-de-coyoacan','universidad-nacional-autonoma-de-mexico','viejo-ejido-de-santa-ursula-coapa','villa-coyoacan','villa-panamericana','villa-quietud','vistas-del-maurel','viveros-de-coyoacan','xotepingo','xotepingo-101']


if URL=="https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/coyoacan/_Desde_49":
    COLONIAS=['20-de-agosto','acasulco','adolfo-ruiz-cortines','ajusco','alianza-popular-revolucionaria','alianza-popular-revolucionaria-fovissste','altillo-universidad','atlantida','avante','barrio-del-nino-jesus','barrio-la-candelaria','barrio-la-concepcion','barrio-oxtopulco-universidad','barrio-san-francisco-culhuacan-barrio-de-la-magdalena','barrio-san-francisco-culhuacan-barrio-de-san-francisco','barrio-san-francisco-culhuacan-barrio-de-santa-ana','barrio-san-lucas','barrio-santa-catarina','bosques-de-tetlameya','cafetales','campestre-churubusco','campestre-coyoacan','cantil-del-pedregal','carmen-serdan','churubusco','churubusco-country-club','ciudad-jardin','colonia-culhuacan-ctm-seccion-x','colonia-ex-ejido-de-san-pablo-tepetlapa','colonia-ex-ejido-de-santa-ursula-coapa','colonia-ex-hacienda-coapa','colonia-presidentes-ejidales-1a-seccion','colonia-viejo-ejido-de-santa-ursula-coapa','concepcion','copilco','copilco-el-alto','copilco-el-bajo','copilco-universidad','country-club','coyoacan-centro','cuadrante-de-san-francisco','culhuacan-ctm-canal-nacional','culhuacan-ctm-croc','culhuacan-ctm-obrero-secc-10','culhuacan-ctm-obrero-secc-5','culhuacan-ctm-obrero-secc-6','culhuacan-ctm-obrero-secc-7','culhuacan-ctm-obrero-secc-8','culhuacan-ctm-obrero-secc-9','culhuacan-ctm-secc-iii','culhuacan-ctm-seccion-i','culhuacan-ctm-seccion-ii','culhuacan-ctm-seccion-iii','culhuacan-ctm-seccion-ix-a','culhuacan-ctm-seccion-ix-b','culhuacan-ctm-seccion-v','culhuacan-ctm-seccion-vi','culhuacan-ctm-seccion-vii','culhuacan-ctm-seccion-viii','culhuacan-ctm-seccion-x-a','culhuacan-piloto-5','del-carmen','delegacion-politica-coyoacan','educacion','el-caracol','el-centinela','el-hueso-infonavit','el-mirador','el-parque','el-parque-de-coyoacan','el-reloj','el-rosario','el-rosedal','emiliano-zapata','emiliano-zapata-fraccionamiento-popular','ermita-churubusco','espartaco','ex-ejido-san-pablo-tepetlapa','ex-ejido-santa-ursula-coapa','ex-ejido-de-san-francisco-culhuacan','ex-ejido-de-san-pablo-tepetlapa','ex-ejido-de-santa-ursula-coapa','ex-hacienda-coapa','fortin-de-chimalistac','fuentes-de-coyoacan','haciendas-de-coyoacan','hermosillo','insurgentes-cuicuilco','insurgentes-san-angel','integracion-latinoamericana','jardines-de-coyoacan','jardines-del-pedregal-de-san-angel','joyas-del-pedregal','la-candelaria-amp','la-concepcion','la-otra-banda','las-campanas','los-cedros','los-cipreses','los-girasoles','los-girasoles-2','los-girasoles-3','los-olivos','los-reyes','los-robles','los-sauces','nueva-diaz-ordaz','olimpica','otros','oxtopulco-universidad','parque-san-andres','paseos-de-taxquena','pedregal-de-carrasco','pedregal-de-coyoacan','pedregal-de-san-angel','pedregal-de-san-francisco','pedregal-de-santa-ursula','pedregal-de-santo-domingo','pedregal-del-maurel','pedregal-del-sur','petrolera-taxquena','prado-churubusco','prados-de-coyoacan','presidentes-ejidales','presidentes-ejidales-1a-seccion','presidentes-ejidales-2a-seccion','pueblo-de-los-reyes','pueblo-de-san-pablo-tepetlapa','pueblo-de-santa-ursula-coapa','pueblo-la-candelaria','residencial-cafetales','residencial-copilco','rinconada-de-los-reyes','romero-de-terreros','rosedal','san-diego-churubusco','san-francisco-culhuacan-barrio-de-san-francisco','san-mateo','san-pablo-tepetlapa','santa-cecilia','santa-ursula-coapa','stunam','taxquena','tetlameya','tlalpan','torres-de-chimalistac','torres-de-coyoacan','universidad-nacional-autonoma-de-mexico','viejo-ejido-de-santa-ursula-coapa','villa-coyoacan','villa-panamericana','villa-quietud','vistas-del-maurel','viveros-de-coyoacan','xotepingo','xotepingo-101']



 
if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/cuajimalpa-de-morelos/_Desde_49":
    COLONIAS=['1-de-mayo','abdias-garcia-soto','adolfo-lopez-mateos','ahuatenco','amado-nervo','ampliacion-el-yaqui','ampliacion-memetla','bosque-de-la-reforma-prolongacion','bosques-de-las-lomas','bosques-de-santa-fe','campestre-palo-alto','chamizal','club-de-golf-bosques','colonia-contadero','colonia-santa-fe-cuajimalpa','contadero','cooperativa-palo-alto','cruz-blanca','cruz-manca','cuajimalpa','cumbres-de-sta-fe','cumbres-reforma','delegacion-politica-cuajimalpa-de-morelos','desarrollo-santa-fe','el-contadero','el-ebano','el-molinito','el-molino','el-tianguillo','el-yaqui','granjas-navidad','granjas-palo-alto','jesus-del-monte','jose-maria-castorena','la-manzanita','la-navidad','la-pila','la-rosita','las-maromas','las-tinajas','locaxco','loma-del-padre','lomas-de-memetla','lomas-de-san-pedro','lomas-de-sta-fe','lomas-de-vista-hermosa','lomas-del-chamizal','lomas-del-chamizal-1a-secc','lomas-del-chamizal-3a-secc','manzanastitla','memetla','nueva-rosita','otros','prados-de-la-montana','puente-grande','rincon-de-las-lomas','san-jose-de-los-cedros','san-jose-de-los-cedros-2a-secc-granja','san-lorenzo-acopilco','san-mateo-tlaltenango','san-pedro','santa-fe-cuajimalpa','santa-rosa-xochiac','tepetongo','villas-de-cuajimalpa','vista-hermosa']
if URL=="https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/cuajimalpa-de-morelos/_Desde_49":
    COLONIAS=['1-de-mayo','abdias-garcia-soto','adolfo-lopez-mateos','ahuatenco','amado-nervo','ampliacion-el-yaqui','ampliacion-memetla','bosque-de-la-reforma-prolongacion','bosques-de-las-lomas','bosques-de-santa-fe','campestre-palo-alto','chamizal','club-de-golf-bosques','colonia-contadero','colonia-santa-fe-cuajimalpa','contadero','cooperativa-palo-alto','cruz-blanca','cruz-manca','cuajimalpa','cumbres-de-sta-fe','cumbres-reforma','delegacion-politica-cuajimalpa-de-morelos','desarrollo-santa-fe','el-contadero','el-ebano','el-molinito','el-molino','el-tianguillo','el-yaqui','granjas-navidad','granjas-palo-alto','jesus-del-monte','jose-maria-castorena','la-manzanita','la-navidad','la-pila','la-rosita','las-maromas','las-tinajas','locaxco','loma-del-padre','lomas-de-memetla','lomas-de-san-pedro','lomas-de-sta-fe','lomas-de-vista-hermosa','lomas-del-chamizal','lomas-del-chamizal-1a-secc','lomas-del-chamizal-3a-secc','manzanastitla','memetla','nueva-rosita','otros','prados-de-la-montana','puente-grande','rincon-de-las-lomas','san-jose-de-los-cedros','san-jose-de-los-cedros-2a-secc-granja','san-lorenzo-acopilco','san-mateo-tlaltenango','san-pedro','santa-fe-cuajimalpa','santa-rosa-xochiac','tepetongo','villas-de-cuajimalpa','vista-hermosa']



 
if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/tlalpan/_Desde_49":
    COLONIAS=['2-de-octubre','agricola-coapa','ampliacion-fuentes-del-pedregal','ampliacion-isidro-fabela','ampliacion-miguel-hidalgo','ampliacion-oriente','arboledas-del-sur','arenal-de-guadalupe','arenal-tepepan','barrio-del-nino-jesus','barrio-el-capulin','barrio-el-truenito','barrio-la-fama','barrio-la-lonja','barrio-san-fernando','belisario-dominguez','belisario-dominguez-seccion-xvi','belvedere-ajusco','bosques-del-pedregal','cantera','cantera-puente-de-piedra','chimalcoyoc','chimali-residencial','chimilli','club-de-golf-mexico','coapa','colinas-del-bosque','colonia-ejidos-de-san-pedro-martir','colonia-fuentes-brotantes','colonia-lomas-del-pedregal-framboyanes','colonia-parque-del-pedregal','colonia-pedregal-de-santa-ursula-xitla','colonia-zacayucan-pena-pobre','cruz-del-farol','cuchilla-de-padierna','cuitlahuac','delegacion-politica-tlalpan','divisadero','dolores-tlali','dr-ignacio-chavez-infonavit','ejidos-de-huipulco','ejidos-de-san-pedro-martir','el-bosque','el-cantil','el-mirador','el-mirador-3a-seccion','el-pedregal','ex-ejido-de-huipulco','exhacienda-coapa','exhacienda-san-juan-de-dios','faroles-del-pedregal','floresta-coyoacan','fuentes-brotantes','fuentes-de-tepepan','fuentes-del-pedregal','gabriel-ramos-millan','granjas-coapa','guadalupe','guadalupe-tlalpan','guadalupita','hacienda-de-san-juan','hacienda-de-san-juan-de-tlalpan-2a-seccion','hacienda-san-juan','hueso-periferico','heroes-de-1910','heroes-de-padierna','insurgentes-cuicuilco','isidro-fabela','issfam','jardines-de-xitle','jardines-del-ajusco','jardines-en-la-montana','jardines-villa-coapa','juventud-unida','la-joya','la-magdalena-petlacalco','la-palma','las-hadas','las-tortolas','lic-emilio-portes-gil-pemex','lomas-altas-de-padierna-sur','lomas-de-cuilotepec','lomas-de-padierna','lomas-de-padierna-sur','lomas-de-tepemecatl','lomas-del-pedregal','lomas-del-pedregal-framboyanes','lomas-hidalgo','los-framboyanes','los-volcanes','magisterial','magisterial-coapa','maria-esther-zuno-de-echeverria','miguel-hidalgo','miguel-hidalgo-1a-seccion','miguel-hidalgo-2a-secc-amp','miguel-hidalgo-2a-seccion','miguel-hidalgo-3a-secc-amp','miguel-hidalgo-3a-seccion','miguel-hidalgo-4a-secc-amp','miguel-hidalgo-4a-seccion','miguel-hidalgo-amp','mirador-del-valle','mirador-i','mirador-ii','narciso-mendoza','narciso-mendoza-villa-coapa','nino-jesus','nueva-oriental-coapa','nueva-rio-blanco','oriental-coapa','otros','paraje-38','paraje-tetenco','parque-del-pedregal','parque-nacional-bosque-del-pedregal','parres-el-guarda','pedregal-de-las-aguilas','pedregal-de-san-nicolas','pedregal-de-san-nicolas-1a-seccion','pedregal-de-san-nicolas-2a-secc','pedregal-de-san-nicolas-3a-secc','pedregal-de-san-nicolas-4a-secc','pedregal-de-san-nicolas-4a-seccion','pedregal-de-santa-ursula-xitla','pedregal-de-topilejo','pedregal-del-lago','pena-pobre','plan-de-ayala','popular-santa-teresa','potrero-acoxpa','prado-coapa','prado-coapa-1a-seccion','prado-coapa-2a-seccion','prado-coapa-3a-secc','prado-coapa-3a-seccion','primavera','pueblo-la-magdalena-petlacalco','rancho-los-colorines','residencial-acoxpa','residencial-hacienda-coapa','residencial-insurgentes','residencial-miramontes','residencial-villa-coapa','retornos-del-pedregal','rinconada-coapa','rinconada-coapa-1a-seccion','rinconada-coapa-2a-secc','rinconada-coapa-2a-seccion','rinconada-las-hadas','rincon-de-san-juan','rincon-del-pedregal','romulo-sanchez-mireles','san-andres-totoltepec','san-bartolo-el-chico','san-buenaventura','san-juan-tepeximilpa','san-lorenzo-huipulco','san-miguel-ajusco','san-miguel-topilejo','san-miguel-xicalco','san-nicolas-2','san-nicolas-totolapan','san-pedro-apostol','san-pedro-martir','santa-ursula-xitla','santo-tomas-ajusco','santisima-trinidad','sauzales-cebadales','tenorios','tepepan','tepetongo','tepeximilpa-amp','tlalcoligia','tlalmille','tlalpan','tlalpan-centro','tlalpuente','toriello-guerra','torres-de-padierna','unidad-habitacional-pemex','valle-de-tepepan','valle-escondido','vergel-coapa','vergel-de-coyoacan','vergel-del-sur','vergel-tlalpan','villa-charra-del-pedregal','villa-coapa','villa-del-puente','villa-del-sur','villa-lazaro-cardenas','villa-olimpica','villa-olimpica-miguel-hidalgo','vistas-del-pedregal','viveros-coatectlan','zacayucan-pena-pobre']
if URL=="https://inmuebles.mercadolibre.com.mx/renta/distrito-federal/tlalpan/_Desde_49":
    COLONIAS=['2-de-octubre','agricola-coapa','ampliacion-fuentes-del-pedregal','ampliacion-isidro-fabela','ampliacion-miguel-hidalgo','ampliacion-oriente','arboledas-del-sur','arenal-de-guadalupe','arenal-tepepan','barrio-del-nino-jesus','barrio-el-capulin','barrio-el-truenito','barrio-la-fama','barrio-la-lonja','barrio-san-fernando','belisario-dominguez','belisario-dominguez-seccion-xvi','belvedere-ajusco','bosques-del-pedregal','cantera','cantera-puente-de-piedra','chimalcoyoc','chimali-residencial','chimilli','club-de-golf-mexico','coapa','colinas-del-bosque','colonia-ejidos-de-san-pedro-martir','colonia-fuentes-brotantes','colonia-lomas-del-pedregal-framboyanes','colonia-parque-del-pedregal','colonia-pedregal-de-santa-ursula-xitla','colonia-zacayucan-pena-pobre','cruz-del-farol','cuchilla-de-padierna','cuitlahuac','delegacion-politica-tlalpan','divisadero','dolores-tlali','dr-ignacio-chavez-infonavit','ejidos-de-huipulco','ejidos-de-san-pedro-martir','el-bosque','el-cantil','el-mirador','el-mirador-3a-seccion','el-pedregal','ex-ejido-de-huipulco','exhacienda-coapa','exhacienda-san-juan-de-dios','faroles-del-pedregal','floresta-coyoacan','fuentes-brotantes','fuentes-de-tepepan','fuentes-del-pedregal','gabriel-ramos-millan','granjas-coapa','guadalupe','guadalupe-tlalpan','guadalupita','hacienda-de-san-juan','hacienda-de-san-juan-de-tlalpan-2a-seccion','hacienda-san-juan','hueso-periferico','heroes-de-1910','heroes-de-padierna','insurgentes-cuicuilco','isidro-fabela','issfam','jardines-de-xitle','jardines-del-ajusco','jardines-en-la-montana','jardines-villa-coapa','juventud-unida','la-joya','la-magdalena-petlacalco','la-palma','las-hadas','las-tortolas','lic-emilio-portes-gil-pemex','lomas-altas-de-padierna-sur','lomas-de-cuilotepec','lomas-de-padierna','lomas-de-padierna-sur','lomas-de-tepemecatl','lomas-del-pedregal','lomas-del-pedregal-framboyanes','lomas-hidalgo','los-framboyanes','los-volcanes','magisterial','magisterial-coapa','maria-esther-zuno-de-echeverria','miguel-hidalgo','miguel-hidalgo-1a-seccion','miguel-hidalgo-2a-secc-amp','miguel-hidalgo-2a-seccion','miguel-hidalgo-3a-secc-amp','miguel-hidalgo-3a-seccion','miguel-hidalgo-4a-secc-amp','miguel-hidalgo-4a-seccion','miguel-hidalgo-amp','mirador-del-valle','mirador-i','mirador-ii','narciso-mendoza','narciso-mendoza-villa-coapa','nino-jesus','nueva-oriental-coapa','nueva-rio-blanco','oriental-coapa','otros','paraje-38','paraje-tetenco','parque-del-pedregal','parque-nacional-bosque-del-pedregal','parres-el-guarda','pedregal-de-las-aguilas','pedregal-de-san-nicolas','pedregal-de-san-nicolas-1a-seccion','pedregal-de-san-nicolas-2a-secc','pedregal-de-san-nicolas-3a-secc','pedregal-de-san-nicolas-4a-secc','pedregal-de-san-nicolas-4a-seccion','pedregal-de-santa-ursula-xitla','pedregal-de-topilejo','pedregal-del-lago','pena-pobre','plan-de-ayala','popular-santa-teresa','potrero-acoxpa','prado-coapa','prado-coapa-1a-seccion','prado-coapa-2a-seccion','prado-coapa-3a-secc','prado-coapa-3a-seccion','primavera','pueblo-la-magdalena-petlacalco','rancho-los-colorines','residencial-acoxpa','residencial-hacienda-coapa','residencial-insurgentes','residencial-miramontes','residencial-villa-coapa','retornos-del-pedregal','rinconada-coapa','rinconada-coapa-1a-seccion','rinconada-coapa-2a-secc','rinconada-coapa-2a-seccion','rinconada-las-hadas','rincon-de-san-juan','rincon-del-pedregal','romulo-sanchez-mireles','san-andres-totoltepec','san-bartolo-el-chico','san-buenaventura','san-juan-tepeximilpa','san-lorenzo-huipulco','san-miguel-ajusco','san-miguel-topilejo','san-miguel-xicalco','san-nicolas-2','san-nicolas-totolapan','san-pedro-apostol','san-pedro-martir','santa-ursula-xitla','santo-tomas-ajusco','santisima-trinidad','sauzales-cebadales','tenorios','tepepan','tepetongo','tepeximilpa-amp','tlalcoligia','tlalmille','tlalpan','tlalpan-centro','tlalpuente','toriello-guerra','torres-de-padierna','unidad-habitacional-pemex','valle-de-tepepan','valle-escondido','vergel-coapa','vergel-de-coyoacan','vergel-del-sur','vergel-tlalpan','villa-charra-del-pedregal','villa-coapa','villa-del-puente','villa-del-sur','villa-lazaro-cardenas','villa-olimpica','villa-olimpica-miguel-hidalgo','vistas-del-pedregal','viveros-coatectlan','zacayucan-pena-pobre']



 

if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/gustavo-a-madero/_Desde_49":
    COLONIAS=['15-de-agosto','25-de-julio','7-de-noviembre','acueducto-de-guadalupe','acueducto-de-ticoman-1044','ahuehuetes','ampliacion-casas-aleman','ampliacion-emiliano-zapata','ampliacion-gabriel-hernandez','ampliacion-guadalupe-proletaria','ampliacion-progreso-nacional','ampliacion-providencia','ampliacion-san-juan-de-aragon','aragon','aragon-inguaran','aragon-la-villa','atzacoalco','atzacoalco-ctm','barrio-candelaria-ticoman','bondojito','ctm-aragon','ctm-atzacoalco','ctm-el-risco','campestre-aragon','casas-aleman-amp','castillo-chico','cerro-prieto','chalma-de-guadalupe','churubusco-tepeyac','colonia-ampliacion-emiliano-zapata','colonia-ampliacion-guadalupe-proletaria','colonia-ctm-aragon','colonia-lindavista-norte','colonia-lindavista-sur','colonia-lindavista-vallejo-ii-seccion','colonia-villa-gustavo-a-madero','constitucion-de-la-republica','cuautepec-de-madero','cuchilla-del-tesoro','cuchilla-la-joya','defensores-de-la-republica','del-bosque','del-obrero','delegacion-politica-gustavo-a-madero','dinamita','dm-nacional','eduardo-molina','el-arbolillo','el-arbolillo-ctm','el-arbolillo-ii-croc','el-arbolillo-iii-croc','el-coyol','el-milagro','el-olivo','el-risco-ctm','emiliano-zapata','estanzuela','estrella','exescuela-de-tiro','faja-de-oro','fernando-casas-aleman','forestal-i','gertrudis-sanchez-1a-seccion','gertrudis-sanchez-2a-secc','gertrudis-sanchez-2a-seccion','gertrudis-sanchez-3a-seccion','granjas-modernas','guadalupe','guadalupe-insurgentes','guadalupe-proletaria','guadalupe-tepeyac','guadalupe-ticoman','guadalupe-victoria','gustavo-a-madero','heroe-de-nacozari','heroes-de-cerro-prieto','heroes-de-chapultepec','industrial','industrial-vallejo','jorge-negrete','jose-maria-morelos-y-pavon-2','juan-de-dios-batiz','juan-gonzalez-romero','la-candelaria-ticoman','la-casilda','la-escalera','la-esmeralda','la-joya','la-joyita','la-laguna-ticoman','la-malinche','la-pastora','la-patera-vallejo','la-pradera','la-pradera-1a-seccion','la-purisima-ticoman','lindavista','lindavista-norte','lindavista-sur','lindavista-vallejo','lindavista-vallejo-i-seccion','lindavista-vallejo-iii-seccion','loma-de-la-palma','loma-la-palma','lomas-de-cuautepec','luis-donaldo-colosio','magdalena-de-las-salinas','malinche','martin-carrera','maximino-avila-camacho','montevideo','martires-de-rio-blanco','narciso-bassols','nueva-atzacoalco','nueva-industrial-vallejo','nueva-tenochtitlan','nueva-vallejo','otros','panamericana','planetario-lindavista','progreso-nacional','progreso-nacional-amp','providencia','pueblo-santiago-atzacoalco','residencial-acueducto-de-guadalupe','residencial-la-escalera','residencial-zacatenco','salvador-diaz-miron','san-bartolo-atepehuacan','san-felipe-de-jesus','san-jose-de-la-escalera','san-jose-ticoman','san-juan-de-aragon','san-juan-de-aragon-2a-secc','san-juan-de-aragon-3a-secc','san-juan-de-aragon-4a-secc','san-juan-de-aragon-5a-secc','san-juan-de-aragon-6a-secc','san-juan-de-aragon-7a-secc','san-juan-de-aragon-amp','san-juan-de-aragon-ctm','san-juan-de-aragon-ejidos-1a-secc','san-juan-de-aragon-ejidos-2a-secc','san-juan-de-aragon-i-seccion','san-juan-de-aragon-ii-seccion','san-juan-de-aragon-iii-seccion','san-juan-de-aragon-iv-seccion','san-juan-de-aragon-v-seccion','san-juan-de-aragon-vi-seccion','san-juan-de-aragon-vii-seccion','san-juan-y-guadalupe-ticoman','san-pedro-el-chico','san-pedro-zacatenco','santa-isabel-tola','santa-maria-ticoman','santa-rosa','santiago-atepetlac','siete-maravillas','tablas-de-san-agustin','tepeyac-insurgentes','ticoman','tlacamaca','torres-lindavista','tres-estrellas','triunfo-de-la-republica','valle-del-tepeyac','vallejo','vallejo-poniente','vasco-de-quiroga','villa-de-aragon','villa-gustavo-a-madero','villahermosa','zacatenco','zona-escolar','zona-escolar-oriente']
if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/gustavo-a-madero/_Desde_49":
    COLONIAS=['15-de-agosto','25-de-julio','7-de-noviembre','acueducto-de-guadalupe','acueducto-de-ticoman-1044','ahuehuetes','ampliacion-casas-aleman','ampliacion-emiliano-zapata','ampliacion-gabriel-hernandez','ampliacion-guadalupe-proletaria','ampliacion-progreso-nacional','ampliacion-providencia','ampliacion-san-juan-de-aragon','aragon','aragon-inguaran','aragon-la-villa','atzacoalco','atzacoalco-ctm','barrio-candelaria-ticoman','bondojito','ctm-aragon','ctm-atzacoalco','ctm-el-risco','campestre-aragon','casas-aleman-amp','castillo-chico','cerro-prieto','chalma-de-guadalupe','churubusco-tepeyac','colonia-ampliacion-emiliano-zapata','colonia-ampliacion-guadalupe-proletaria','colonia-ctm-aragon','colonia-lindavista-norte','colonia-lindavista-sur','colonia-lindavista-vallejo-ii-seccion','colonia-villa-gustavo-a-madero','constitucion-de-la-republica','cuautepec-de-madero','cuchilla-del-tesoro','cuchilla-la-joya','defensores-de-la-republica','del-bosque','del-obrero','delegacion-politica-gustavo-a-madero','dinamita','dm-nacional','eduardo-molina','el-arbolillo','el-arbolillo-ctm','el-arbolillo-ii-croc','el-arbolillo-iii-croc','el-coyol','el-milagro','el-olivo','el-risco-ctm','emiliano-zapata','estanzuela','estrella','exescuela-de-tiro','faja-de-oro','fernando-casas-aleman','forestal-i','gertrudis-sanchez-1a-seccion','gertrudis-sanchez-2a-secc','gertrudis-sanchez-2a-seccion','gertrudis-sanchez-3a-seccion','granjas-modernas','guadalupe','guadalupe-insurgentes','guadalupe-proletaria','guadalupe-tepeyac','guadalupe-ticoman','guadalupe-victoria','gustavo-a-madero','heroe-de-nacozari','heroes-de-cerro-prieto','heroes-de-chapultepec','industrial','industrial-vallejo','jorge-negrete','jose-maria-morelos-y-pavon-2','juan-de-dios-batiz','juan-gonzalez-romero','la-candelaria-ticoman','la-casilda','la-escalera','la-esmeralda','la-joya','la-joyita','la-laguna-ticoman','la-malinche','la-pastora','la-patera-vallejo','la-pradera','la-pradera-1a-seccion','la-purisima-ticoman','lindavista','lindavista-norte','lindavista-sur','lindavista-vallejo','lindavista-vallejo-i-seccion','lindavista-vallejo-iii-seccion','loma-de-la-palma','loma-la-palma','lomas-de-cuautepec','luis-donaldo-colosio','magdalena-de-las-salinas','malinche','martin-carrera','maximino-avila-camacho','montevideo','martires-de-rio-blanco','narciso-bassols','nueva-atzacoalco','nueva-industrial-vallejo','nueva-tenochtitlan','nueva-vallejo','otros','panamericana','planetario-lindavista','progreso-nacional','progreso-nacional-amp','providencia','pueblo-santiago-atzacoalco','residencial-acueducto-de-guadalupe','residencial-la-escalera','residencial-zacatenco','salvador-diaz-miron','san-bartolo-atepehuacan','san-felipe-de-jesus','san-jose-de-la-escalera','san-jose-ticoman','san-juan-de-aragon','san-juan-de-aragon-2a-secc','san-juan-de-aragon-3a-secc','san-juan-de-aragon-4a-secc','san-juan-de-aragon-5a-secc','san-juan-de-aragon-6a-secc','san-juan-de-aragon-7a-secc','san-juan-de-aragon-amp','san-juan-de-aragon-ctm','san-juan-de-aragon-ejidos-1a-secc','san-juan-de-aragon-ejidos-2a-secc','san-juan-de-aragon-i-seccion','san-juan-de-aragon-ii-seccion','san-juan-de-aragon-iii-seccion','san-juan-de-aragon-iv-seccion','san-juan-de-aragon-v-seccion','san-juan-de-aragon-vi-seccion','san-juan-de-aragon-vii-seccion','san-juan-y-guadalupe-ticoman','san-pedro-el-chico','san-pedro-zacatenco','santa-isabel-tola','santa-maria-ticoman','santa-rosa','santiago-atepetlac','siete-maravillas','tablas-de-san-agustin','tepeyac-insurgentes','ticoman','tlacamaca','torres-lindavista','tres-estrellas','triunfo-de-la-republica','valle-del-tepeyac','vallejo','vallejo-poniente','vasco-de-quiroga','villa-de-aragon','villa-gustavo-a-madero','villahermosa','zacatenco','zona-escolar','zona-escolar-oriente']



if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/iztapalapa/_Desde_49":
    COLONIAS=['12-de-diciembre','aculco','albarrada','alborada','alvaro-obregon','ampliacion-el-santuario','ampliacion-el-triunfo','ampliacion-emiliano-zapata','ampliacion-los-reyes','ampliacion-paraje-san-juan','ampliacion-san-miguel','ampliacion-sinatel','apatlaco','ano-de-juarez','banjidal','barrio-san-antonio-culhuacan','barrio-san-lucas','bellavista','benito-juarez','buenavista','cabeza-de-juarez','cabeza-de-juarez-5','cacama','campestre-potrero','carlos-hank-gonzalez','casa-blanca','central-de-abasto','cerro-de-la-estrella','cerro-estrella','chinampac-de-juarez','citlalli','colonial-iztapalapa','consejo-agrarista-mexicano','constitucion-de-1917','cuchilla-del-moral','culhuacan','desarrollo-urbano-quetzalcoatl','diasa','dr-alfonso-ortiz-tirado','ejercito-constitucionalista','ejercito-de-agua-prieta','ejercito-de-oriente','ejercito-de-oriente-zona-penon','el-eden','el-manto','el-mirador','el-molino','el-molino-tezonco','el-paraiso','el-prado','el-retono','el-rodeo','el-rosario','el-santuario','el-santuario-amp','el-sifon','el-triunfo','el-triunfo-amp','el-vergel','ermita-iztapalapa','ermita-zaragoza','escuadron-201','estado-de-veracruz','estrella-culhuacan','estrella-del-sur','eva-samano-de-lopez-mateos','exhacienda-san-nicolas-tolentino','francisco-villa','fuego-nuevo','fuentes-de-zaragoza','fuerte-de-loreto','granjas-de-san-antonio','granjas-esmeralda','granjas-estrella','guadalupe-del-moral','heroes-de-churubusco','ignacio-zaragoza','insurgentes','iztapalapa-centro','iztlahuacan','jacarandas','jardines-de-churubusco','jardines-de-san-lorenzo-tezonco','jose-lopez-portillo','jose-maria-morelos-y-pavon','juan-escutia','justo-sierra','la-asuncion','la-colmena','la-era','la-esperanza','la-mora-grande','la-polvorilla','la-regadera','la-viga','las-americas','las-penas','leyes-de-reforma','leyes-de-reforma-1a-seccion','leyes-de-reforma-2a-seccion','leyes-de-reforma-3a-seccion','lomas-de-la-estancia','lomas-de-san-lorenzo','lomas-el-manto','lomas-estrella','lomas-estrella-1a-secc','lomas-estrella-2a-secc','lomas-estrella-amp','los-cipreses','los-mirasoles','los-reyes-culhuacan','los-angeles','los-angeles-apanoaya','magdalena-atlazolpa','margarita-maza-de-juarez','mexicaltzingo','miguel-de-la-madrid-hurtado','minerva','mixcoatl','monte-alban','morelos-2','nueva-rosita','otros','palmitas','paraje-san-juan','paraje-san-juan-amp','paraje-san-juan-cerro','paraje-zacatepec','paseos-de-churubusco','paseos-de-churubusco-fovissste','prados-iztapalapa','presidentes-de-mexico','progresista','pueblo-culhuacan','real-del-moral','reforma-politica','ricardo-flores-magon','san-andres-tetepilco','san-antonio','san-antonio-culhuacan','san-ignacio','san-jose-aculco','san-jose-buenavista','san-juan-estrella','san-juan-xalpa','san-juanico-nextipac','san-lorenzo','san-lorenzo-tezonco','san-lorenzo-tezonco-fovissste','san-lorenzo-xicotencatl','san-lucas','san-marcos','san-miguel','san-miguel-amp','san-miguel-teotongo','san-miguel-teotongo-seccion-capilla','san-miguel-teotongo-seccion-puente','san-nicolas-tolentino','san-pablo','san-pablo-1a-secc','san-pedro','san-sebastian-tecoloxtitla','santa-barbara','santa-cruz-meyehualco','santa-isabel-industrial','santa-martha-acatitla','santa-martha-acatitla-norte','santa-martha-acatitla-sur','santa-maria-aztahuacan','santa-maria-tomatlan','santiago-acahualtepec','santiago-acahualtepec-2a-ampliacion','sector-popular','sideral','sifon','sinatel','solidaridad','tepalcates','triangulo-de-las-agujas','unidad-ejercito-constitucionalista','unidad-modelo','unidad-vicente-guerrero','valle-de-san-lorenzo','valle-del-sur','vicente-guerrero','voceadores-de-mexico','xalpa','zacahuitzco']
if URL=="https://inmuebles.mercadolibre.com.mx/venta/distrito-federal/iztapalapa/_Desde_49":
    COLONIAS=['12-de-diciembre','aculco','albarrada','alborada','alvaro-obregon','ampliacion-el-santuario','ampliacion-el-triunfo','ampliacion-emiliano-zapata','ampliacion-los-reyes','ampliacion-paraje-san-juan','ampliacion-san-miguel','ampliacion-sinatel','apatlaco','ano-de-juarez','banjidal','barrio-san-antonio-culhuacan','barrio-san-lucas','bellavista','benito-juarez','buenavista','cabeza-de-juarez','cabeza-de-juarez-5','cacama','campestre-potrero','carlos-hank-gonzalez','casa-blanca','central-de-abasto','cerro-de-la-estrella','cerro-estrella','chinampac-de-juarez','citlalli','colonial-iztapalapa','consejo-agrarista-mexicano','constitucion-de-1917','cuchilla-del-moral','culhuacan','desarrollo-urbano-quetzalcoatl','diasa','dr-alfonso-ortiz-tirado','ejercito-constitucionalista','ejercito-de-agua-prieta','ejercito-de-oriente','ejercito-de-oriente-zona-penon','el-eden','el-manto','el-mirador','el-molino','el-molino-tezonco','el-paraiso','el-prado','el-retono','el-rodeo','el-rosario','el-santuario','el-santuario-amp','el-sifon','el-triunfo','el-triunfo-amp','el-vergel','ermita-iztapalapa','ermita-zaragoza','escuadron-201','estado-de-veracruz','estrella-culhuacan','estrella-del-sur','eva-samano-de-lopez-mateos','exhacienda-san-nicolas-tolentino','francisco-villa','fuego-nuevo','fuentes-de-zaragoza','fuerte-de-loreto','granjas-de-san-antonio','granjas-esmeralda','granjas-estrella','guadalupe-del-moral','heroes-de-churubusco','ignacio-zaragoza','insurgentes','iztapalapa-centro','iztlahuacan','jacarandas','jardines-de-churubusco','jardines-de-san-lorenzo-tezonco','jose-lopez-portillo','jose-maria-morelos-y-pavon','juan-escutia','justo-sierra','la-asuncion','la-colmena','la-era','la-esperanza','la-mora-grande','la-polvorilla','la-regadera','la-viga','las-americas','las-penas','leyes-de-reforma','leyes-de-reforma-1a-seccion','leyes-de-reforma-2a-seccion','leyes-de-reforma-3a-seccion','lomas-de-la-estancia','lomas-de-san-lorenzo','lomas-el-manto','lomas-estrella','lomas-estrella-1a-secc','lomas-estrella-2a-secc','lomas-estrella-amp','los-cipreses','los-mirasoles','los-reyes-culhuacan','los-angeles','los-angeles-apanoaya','magdalena-atlazolpa','margarita-maza-de-juarez','mexicaltzingo','miguel-de-la-madrid-hurtado','minerva','mixcoatl','monte-alban','morelos-2','nueva-rosita','otros','palmitas','paraje-san-juan','paraje-san-juan-amp','paraje-san-juan-cerro','paraje-zacatepec','paseos-de-churubusco','paseos-de-churubusco-fovissste','prados-iztapalapa','presidentes-de-mexico','progresista','pueblo-culhuacan','real-del-moral','reforma-politica','ricardo-flores-magon','san-andres-tetepilco','san-antonio','san-antonio-culhuacan','san-ignacio','san-jose-aculco','san-jose-buenavista','san-juan-estrella','san-juan-xalpa','san-juanico-nextipac','san-lorenzo','san-lorenzo-tezonco','san-lorenzo-tezonco-fovissste','san-lorenzo-xicotencatl','san-lucas','san-marcos','san-miguel','san-miguel-amp','san-miguel-teotongo','san-miguel-teotongo-seccion-capilla','san-miguel-teotongo-seccion-puente','san-nicolas-tolentino','san-pablo','san-pablo-1a-secc','san-pedro','san-sebastian-tecoloxtitla','santa-barbara','santa-cruz-meyehualco','santa-isabel-industrial','santa-martha-acatitla','santa-martha-acatitla-norte','santa-martha-acatitla-sur','santa-maria-aztahuacan','santa-maria-tomatlan','santiago-acahualtepec','santiago-acahualtepec-2a-ampliacion','sector-popular','sideral','sifon','sinatel','solidaridad','tepalcates','triangulo-de-las-agujas','unidad-ejercito-constitucionalista','unidad-modelo','unidad-vicente-guerrero','valle-de-san-lorenzo','valle-del-sur','vicente-guerrero','voceadores-de-mexico','xalpa','zacahuitzco']







#
#
#

# Asigna formato de ejemplo1
formato1 = "%Y-%m-%d %H_%M_%S"
hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
hoy = hoy.strftime(formato1)  
#print("File      Path:", Path(__file__).absolute())
#print("Directory Path:", Path().absolute())  
path=str(Path().absolute())+"\\MERCADO_LIBRE_URL\\"
if os.path.exists(path):
    pass
else:
     
    os.mkdir(path)

    
path=str(Path().absolute())+"\\MERCADO_LIBRE_URL\\"+"URL_"+hoy

print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)

f= open(path+"\\"+"URL_"+hoy+".csv","w+")
        								                                                                                                                                			
f.write("\"URL\","+"\"PRECIO\","+"\"TIPO\","+"\"CATEGORIA\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"TERRENO\","+"\"CONSTRUIDOS\","+"\"BAÑOS\","+"\"ESTACIONAMIENTO\","+"\"RECAMARAS\","+"\"MEDIOS BAÑOS\","+"\"ANTIGÜEDAD\","+"\"CALLE\","+"\"COLONIA\","+"\"DELEGACION\","+"\"CIUDAD\","+"\"PUBLICADO\"\n")
contador=1
for col in COLONIAS: 
    print(contador) 
    contador+=1
    try:      
        cuerpo(URL,col)
    except:
         
        URL=URL.replace("_Desde_","/_Desde_")
        URL=URL.replace("//_","/_")
        
        cuerpo(URL,col)
  
f.close() 



