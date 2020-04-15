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
    
   
    URL=URL.replace("//","/")
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
    URL=URL.replace("//","/")
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
    print(URL)
    #exit()
    
    
    URL=URL.replace("_Desde_","/_Desde_")
    URL=URL.replace("//","/") 
    elements,soup=navega_page(URL)


        
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

for col in COLONIAS:  
    try:      
        cuerpo(URL,col)
    except:
        URL=URL.replace("_Desde_","/_Desde_")
        URL=URL.replace("//","/")
        cuerpo(URL,col)
  
f.close() 



