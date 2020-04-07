import requests
from bs4 import BeautifulSoup
import math
import time
import sys
import os
import json
from datetime import datetime
from pathlib import Path
from operator import itemgetter
import time
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


def navega_page_toda(URL):
    URL='http://ciudadmx.cdmx.gob.mx:8080/seduvi/'+URL
    #print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
     
    
    #elements = results.find('ol', id='searchResults')
    return soup

def navega_page(URL):
    URL='http://ciudadmx.cdmx.gob.mx:8080/seduvi/'+URL
    #print(URL)
    headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('select')
    
    #elements = results.find('ol', id='searchResults')
    return results,soup

 

     
 
'''

EJECUTAR SCRAP
#python3 scrap_ciudadmx.py "cAlvaroObregon"
'''

opera=sys.argv[1]
 

#DELEGACIONES=['cAlvaroObregon','cAzcapotzalco','cBenitoJuarez','cCoyoacan','cCuajimalpa','cCuauhtemoc',
# 'cGustavoAMadero','cIztacalco','cIztapalapa','cMagdalenaContreras','cMiguelHidalgo','cMilpaAlta',
# 'cTlahuac','cTlalpan','cVenustianoCarranza','cXochimilco']

DELEGACIONES=[opera]

#https://listado.mercadolibre.com.mx/rentar-casa-condesa#D[A:rentar%20casa%20condesa]



    
# Asigna formato de ejemplo1
formato1 = "%d_%m_%Y"
#hoy = datetime.today()  # Asigna fecha-hora
# Aplica formato ejemplo1
#hoy = hoy.strftime(formato1)  

path=str(Path().absolute())+"\\"+str("Delegaciones_CIUDADMX")
print(path)
if os.path.exists(path):
    print("CARPETA YA EXISTIA Y NO LA CREA")
else:
    print("CARPETA CREADA")
    os.mkdir(path)
 
      
for deles in DELEGACIONES:
    mi_path = str(deles)+".txt"
    
    if os.path.exists( path+"\\"+mi_path):
    #with open(path+"\\"+mi_path, 'w') as file:
        #path=str(Path().absolute())
        if os.path.exists( path+"\\"+deles+".csv"):
            print("ya EXISTE ARCHIVO " + str(mi_path))
           
            data = import_csv(path+"\\"+deles+".csv")
            last_row = data[-1]
            #print()
            
            #exit() 
            f2= open(path+"\\"+deles+".csv","a+")                                                                                                                                                                                   
           
            #f2.write("\"CUENTA CATASTRAL\","+"\"CALLE Y NUM\","+"\"COLONIA\","+"\"CP\","+"\"SUPERFICE\","+"\"USO DE SUELO\","+"\"NIVELES\","+"\"ALTURA\","+"\"AREA LIBRE\","+"\"M2 MIN.\","+"\"DENSIDAD\","+"\"SUPERFICE MAX.\","+"\"VIVIENDAS PERMITIDAS\"\n")
        else:
            last_row="null"
            print("no existe CREA CSV " + str(mi_path))
            f2= open(path+"\\"+deles+".csv","w+")
                                                                                                                                                                                                

            f2.write("\"URL\","+"\"CUENTA CATASTRAL\","+"\"CALLE Y NUM\","+"\"COLONIA\","+"\"CP\","+"\"SUPERFICE\","+"\"USO DE SUELO\","+"\"NIVELES\","+"\"ALTURA\","+"\"AREA LIBRE\","+"\"M2 MIN.\","+"\"DENSIDAD\","+"\"SUPERFICE MAX.\","+"\"VIVIENDAS PERMITIDAS\"\n")
               

        with open(path+"\\"+mi_path) as file:
            data = json.load(file)
            
            bandera=False
            for client in data:
                #for colonia in client['colonia']:
                #   print('nombre_colonia:', colonia)
                    #print(client['colonia']['nombre_colonia'])
                    #print('') 
                    #print(client)
                    
                    for calles in client['colonia']['calles']:
                        #print(client['colonia']['nombre_colonia'],calles['nombre_calle'])
                        #print(type(calles['nombre_calle']))
                        #exit()
                        #print(calles['nombre_calle'])
                        #print(calles)
                        
                        for numeros in calles['numeros']:  
                        #print(client['colonia']['nombre_colonia'],calles['nombre_calle'],numeros)   
                            #print(numeros)
                            #print(last_row)
                            if last_row!="null":
                                URL='busquedasseduvi/getCuentasCatastral.jsp?delegacion='+str(deles)+'&colonia='+client['colonia']['nombre_colonia']+'&calle='+calles['nombre_calle']+'&numeroCalle='+str(numeros)
                                
                                if last_row[0]==URL or bandera==True:                                  
                                  
                                    try:
                                        
                                        bandera=True  
                                        
                                        URL='busquedasseduvi/getCuentasCatastral.jsp?delegacion='+str(deles)+'&colonia='+client['colonia']['nombre_colonia']+'&calle='+calles['nombre_calle']+'&numeroCalle='+str(numeros)
                                        print(URL)
                                        elements,soup=navega_page(URL)
                                        print(elements.text)
                                    
                                        #print(calles['nombre_calle'].replace("%20"," "),numeros)  
                                        
                                        #print(client['colonia']['nombre_colonia'].replace("%20"," "))   
                                        
                                        URL2='fichasReporte/fichaInformacion.jsp?nombreConexion='+str(deles)+'&cuentaCatastral='+str(elements.text)
                                        soup=navega_page_toda(URL2)
                                        
                                        cp=soup.find('fieldset',style='height:420px;')
                                        cp=str(cp).split('Postal:</td><td>')
                                        cp=cp[1].split('</td>')
                                        #print(fieldset[0])
                                        
                                        super_predio=soup.find('fieldset',style='height:420px;')
                                        super_predio=str(super_predio).split('Predio:</td><td>')
                                        super_predio=super_predio[1].split('</td>')
                                        #print(fieldset2[0])
                                        
                                        tablas=soup.find_all('table',style='width:650px;')
                                        
                                        contenido=tablas[0]
                                        
                                        uso_suelo=str(contenido).split('194px;">')
                                        uso_suelo=uso_suelo[1].split("<br/>") 
                                        #print (uso_suelo[0])
                                        
                                        Niveles=str(contenido).split('152px;">')
                                        Niveles=Niveles[1].split("</td>") 
                                        #print (Niveles[0])
                                        
                                        Altura=str(contenido).split('44px;">')
                                        Altura=Altura[1].split("</td>") 
                                        #print (Altura[0])
                                        
                                        
                                        
                                        Area_libre=str(contenido).split('49px;">')
                                        Area_libre=Area_libre[1].split("</td>") 
                                        #print (Area_libre[0])
                                        
                                        m2_min=str(contenido).split('62px;">')
                                        m2_min=m2_min[1].split("</td>") 
                                        #print (m2_min[0])
                                        
                                        densidad=str(contenido).split('59px;">')
                                        densidad=densidad[1].split("</td>") 
                                        #print (densidad[0])
                                        
                                        superficie=str(contenido).split('91px;">')
                                        superficie=superficie[1].split("</td>") 
                                        #print (superficie[0])
                                        
                                        numero=str(contenido).split('99px;">')
                                        numero=numero[1].split("</td>") 
                                        #print (numero[0])
                                        f2.write("\""+URL+"\",") 
                                        f2.write("\""+elements.text+"\",") 
                                        f2.write("\""+calles['nombre_calle'].replace("%20"," ") +" "+numeros+"\",")
                                        f2.write("\""+client['colonia']['nombre_colonia'].replace("%20"," ")+"\",")
                                        f2.write("\""+cp[0]+"\",")
                                        f2.write("\""+super_predio[0]+"\",")
                                        f2.write("\""+uso_suelo[0]+"\",")
                                        f2.write("\""+Niveles[0]+"\",")
                                        f2.write("\""+Altura[0]+"\",")
                                        f2.write("\""+Area_libre[0]+"\",")
                                        f2.write("\""+m2_min[0]+"\",")
                                        f2.write("\""+densidad[0]+"\",")
                                        f2.write("\""+superficie[0]+"\",")
                                        f2.write("\""+numero[0].lstrip().rstrip()+"\"\n")
                                        #print(tablas[0])
                                    except:
                                        continue
                            else:
                                try:
                                        
                                    bandera=True  
                                    
                                    URL='busquedasseduvi/getCuentasCatastral.jsp?delegacion='+str(deles)+'&colonia='+client['colonia']['nombre_colonia']+'&calle='+calles['nombre_calle']+'&numeroCalle='+str(numeros)
                                    print(URL)
                                    elements,soup=navega_page(URL)
                                    #print(elements.text)
                                
                                    #print(calles['nombre_calle'].replace("%20"," "),numeros)  
                                    
                                    #print(client['colonia']['nombre_colonia'].replace("%20"," "))   
                                    
                                    URL2='fichasReporte/fichaInformacion.jsp?nombreConexion='+str(deles)+'&cuentaCatastral='+str(elements.text)
                                    soup=navega_page_toda(URL2)
                                    
                                    cp=soup.find('fieldset',style='height:420px;')
                                    cp=str(cp).split('Postal:</td><td>')
                                    cp=cp[1].split('</td>')
                                    #print(fieldset[0])
                                    
                                    super_predio=soup.find('fieldset',style='height:420px;')
                                    super_predio=str(super_predio).split('Predio:</td><td>')
                                    super_predio=super_predio[1].split('</td>')
                                    #print(fieldset2[0])
                                    
                                    tablas=soup.find_all('table',style='width:650px;')
                                    
                                    contenido=tablas[0]
                                    
                                    uso_suelo=str(contenido).split('194px;">')
                                    uso_suelo=uso_suelo[1].split("<br/>") 
                                    #print (uso_suelo[0])
                                    
                                    Niveles=str(contenido).split('152px;">')
                                    Niveles=Niveles[1].split("</td>") 
                                    #print (Niveles[0])
                                    
                                    Altura=str(contenido).split('44px;">')
                                    Altura=Altura[1].split("</td>") 
                                    #print (Altura[0])
                                    
                                    
                                    
                                    Area_libre=str(contenido).split('49px;">')
                                    Area_libre=Area_libre[1].split("</td>") 
                                    #print (Area_libre[0])
                                    
                                    m2_min=str(contenido).split('62px;">')
                                    m2_min=m2_min[1].split("</td>") 
                                    #print (m2_min[0])
                                    
                                    densidad=str(contenido).split('59px;">')
                                    densidad=densidad[1].split("</td>") 
                                    #print (densidad[0])
                                    
                                    superficie=str(contenido).split('91px;">')
                                    superficie=superficie[1].split("</td>") 
                                    #print (superficie[0])
                                    
                                    numero=str(contenido).split('99px;">')
                                    numero=numero[1].split("</td>") 
                                    #print (numero[0])
                                    f2.write("\""+URL+"\",") 
                                    f2.write("\""+elements.text+"\",") 
                                    f2.write("\""+calles['nombre_calle'].replace("%20"," ") +" "+numeros+"\",")
                                    f2.write("\""+client['colonia']['nombre_colonia'].replace("%20"," ")+"\",")
                                    f2.write("\""+cp[0]+"\",")
                                    f2.write("\""+super_predio[0]+"\",")
                                    f2.write("\""+uso_suelo[0]+"\",")
                                    f2.write("\""+Niveles[0]+"\",")
                                    f2.write("\""+Altura[0]+"\",")
                                    f2.write("\""+Area_libre[0]+"\",")
                                    f2.write("\""+m2_min[0]+"\",")
                                    f2.write("\""+densidad[0]+"\",")
                                    f2.write("\""+superficie[0]+"\",")
                                    f2.write("\""+numero[0].lstrip().rstrip()+"\"\n")
                                    #print(tablas[0])
                                except:
                                    continue
                                
                    
                        
                
        f2.close() 
    
    else:
    
        URL='busquedasseduvi/getColonias.jsp?delegacion='+deles
        print(URL)       
        elements,soup=navega_page(URL)


        #MiDiccionario = {'colonias' : ''}
        #colonias
        colonias=list()
        colonias2=list()
        
        for column in elements:
                #column=str(column).replace('<br>','')
                #print("XXX"+str(column.text.strip()))
                
                if column['value']!='' and column['value']!='0':
                    #%C1  %F0   ð
                    colonias.append(column['value'].replace(" ","%20").replace("Ð","%D0").replace("Á","%C1").replace("ð","%F0"))


        
        MiDiccionario = {'colonias' : ''}
        MisCalles = {'calles' : ''}
        MisNumeros = {'numeros' : ''}
        
        for item in colonias:
            try:
                #busquedasseduvi/getCalles.jsp?delegacion=cTlalpan&colonia=NARCISO%20MENDOZA
                URL='busquedasseduvi/getCalles.jsp?delegacion='+deles+'&colonia='+item
                print(URL)
                elements,soup=navega_page(URL)
                calles=list()
                calles2=list()
                for calle in elements:
                    if calle['value']!='' and calle['value']!='0':
                        calles.append(calle['value'].replace(" ","%20").replace("Ð","%D0").replace("Á","%C1"))
                                        
                        URL='busquedasseduvi/getNumerosCalle.jsp?delegacion='+deles+'&colonia='+item+'&calle='+calle['value'].replace(" ","%20").replace("Ð","%D0")
                        #print(URL)
                        elements,soup=navega_page(URL)
                        flag=True
                        try:   
                            numeros=list()
                            for num in elements:
                                if num['value']!='' and num['value']!='0':
                                    numeros.append(num['value'].replace(" ","%20").replace("Ð","%D0").replace("Á","%C1").replace("ð","%F0"))
                            #print(elements)
                            
                            #MiDiccionario['colonias'] = colonias
                            
                            #MisNumeros['numeros'] =numeros
                            calles2.append ({'nombre_calle': calle['value'].replace(" ","%20").replace("Ð","%D0").replace("Á","%C1").replace("ð","%F0"),'numeros':numeros})
                            MiDiccionario ['colonias'] = {'nombre_colonia' : item,'calles':calles2}
                            
                            
                            #print(MiDiccionario)
                            #exit()
                        except:
                            flag=False
                            
                #print(calles)
                if flag:
                    colonias2.append({'colonia':MiDiccionario ['colonias']})
                #print(colonias2)
                #exit()
                
            #busquedasseduvi/getNumerosCalle.jsp?delegacion=cTlalpan&colonia=NARCISO%20MENDOZA&calle=PROLONGACION%20DIVISION%20DEL%20NORTE
            except:
                continue
        
        mi_path = str(deles)+".txt"
        with open(path+"\\"+mi_path, 'w') as file:
            json.dump(colonias2, file, indent=4)
            
    
    
        print("termina de actualizar, va a crear CSV ")



    

        #path=str(Path().absolute())
        f= open(path+"\\"+deles+".csv","w+")
                                                                                                                                                                                            

        f.write("\"CUENTA CATASTRAL\","+"\"CALLE Y NUM\","+"\"COLONIA\","+"\"CP\","+"\"SUPERFICE\","+"\"USO DE SUELO\","+"\"NIVELES\","+"\"ALTURA\","+"\"AREA LIBRE\","+"\"M2 MIN.\","+"\"DENSIDAD\","+"\"SUPERFICE MAX.\","+"\"VIVIENDAS PERMITIDAS\"\n")
            

        with open(path+"\\"+mi_path) as file:
            data = json.load(file)
            
        
            for client in data:
                #for colonia in client['colonia']:
                #   print('nombre_colonia:', colonia)
                    #print(client['colonia']['nombre_colonia'])
                    
                    
                    for calles in client['colonia']['calles']:
                        #print(client['colonia']['nombre_colonia'],calles['nombre_calle'])
                        #print(type(calles['nombre_calle']))
                        #exit()
                        #print(calles['nombre_calle'])
                        
                        for numeros in calles['numeros']:  
                        #print(client['colonia']['nombre_colonia'],calles['nombre_calle'],numeros)   
                            try:  
                                URL='busquedasseduvi/getCuentasCatastral.jsp?delegacion='+str(deles)+'&colonia='+client['colonia']['nombre_colonia']+'&calle='+calles['nombre_calle']+'&numeroCalle='+str(numeros)
                                print(URL)
                                elements,soup=navega_page(URL)
                                #print(elements.text)
                            
                                #print(calles['nombre_calle'].replace("%20"," "),numeros)  
                                
                                #print(client['colonia']['nombre_colonia'].replace("%20"," "))   
                                
                                URL2='fichasReporte/fichaInformacion.jsp?nombreConexion='+str(deles)+'&cuentaCatastral='+str(elements.text)
                                soup=navega_page_toda(URL2)
                                
                                cp=soup.find('fieldset',style='height:420px;')
                                cp=str(cp).split('Postal:</td><td>')
                                cp=cp[1].split('</td>')
                                #print(fieldset[0])
                                
                                super_predio=soup.find('fieldset',style='height:420px;')
                                super_predio=str(super_predio).split('Predio:</td><td>')
                                super_predio=super_predio[1].split('</td>')
                                #print(fieldset2[0])
                                
                                tablas=soup.find_all('table',style='width:650px;')
                                
                                contenido=tablas[0]
                                
                                uso_suelo=str(contenido).split('194px;">')
                                uso_suelo=uso_suelo[1].split("<br/>") 
                                #print (uso_suelo[0])
                                
                                Niveles=str(contenido).split('152px;">')
                                Niveles=Niveles[1].split("</td>") 
                                #print (Niveles[0])
                                
                                Altura=str(contenido).split('44px;">')
                                Altura=Altura[1].split("</td>") 
                                #print (Altura[0])
                                
                                
                                
                                Area_libre=str(contenido).split('49px;">')
                                Area_libre=Area_libre[1].split("</td>") 
                                #print (Area_libre[0])
                                
                                m2_min=str(contenido).split('62px;">')
                                m2_min=m2_min[1].split("</td>") 
                                #print (m2_min[0])
                                
                                densidad=str(contenido).split('59px;">')
                                densidad=densidad[1].split("</td>") 
                                #print (densidad[0])
                                
                                superficie=str(contenido).split('91px;">')
                                superficie=superficie[1].split("</td>") 
                                #print (superficie[0])
                                
                                numero=str(contenido).split('99px;">')
                                numero=numero[1].split("</td>") 
                                #print (numero[0])
                                f.write("\""+URL+"\",") 
                                f.write("\""+elements.text+"\",") 
                                f.write("\""+calles['nombre_calle'].replace("%20"," ") +" "+numeros+"\",")
                                f.write("\""+client['colonia']['nombre_colonia'].replace("%20"," ")+"\",")
                                f.write("\""+cp[0]+"\",")
                                f.write("\""+super_predio[0]+"\",")
                                f.write("\""+uso_suelo[0]+"\",")
                                f.write("\""+Niveles[0]+"\",")
                                f.write("\""+Altura[0]+"\",")
                                f.write("\""+Area_libre[0]+"\",")
                                f.write("\""+m2_min[0]+"\",")
                                f.write("\""+densidad[0]+"\",")
                                f.write("\""+superficie[0]+"\",")
                                f.write("\""+numero[0].lstrip().rstrip()+"\"\n")
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                 #print(tablas[0])
                            except:
                                continue
                    
                        
                
        f.close()        
print("TERMINA DELEGACION")
exit()
