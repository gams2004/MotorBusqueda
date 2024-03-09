from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from Comparador import compare_cursos
from Comparador import encontrar_cursos_similares
import json
import re
import csv
import os
import glob

def compare(curso1, curso2):
    similitud = compare_cursos(curso1, curso2)
    return similitud

# Guarda el índice en un archivo csvs
def guardar_indice_csv(indice, archivo_salida):
    with open(archivo_salida, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="|")
        csv_writer.writerow(["Curso", "Palabra"])

        for palabra, cursos in indice.items():
            for curso in cursos:
                csv_writer.writerow([curso, palabra])
    print("Contenido guardado en el archivo:",archivo_salida)

#Función que relaciona palabras a los cursos a través de un índice
def construir_indice(catalogo):
    indice = {}
    palabras_innecesarias = {"la","le","lo","los","las","el","a","y","de","del","son","es","en","por","para","con","sin","que","quienes","quien","ella","tu","desde","estos","este","estas","o","un","al","como","1","2","3","4","5","8","9","12","13","15","16","18","24","60","70","00","0651","33632","33633","entre","e","d","c","p","m","o","sus","ha","han","si","uno","ser","pueden","sobre","tanto","sin","nos","está","luego","sí","debe","no","más","mas","tener","una","se","dan","dos","as","sido","están","otros","hacia","parte","lugar","hacia","esta","su","tiene","van","sino","solo","toma","hará","dentro","quién","desde","b","h","puede","72","nueve","32","cómo","también","tendrá","in","veinte","quiere","otras","and","the","ante","i","j","k","dejar","gran","través","mismo","haya","unas"}

    for curso in catalogo:
        # Obtener identificador y contenido del curso
        titulo = curso["titulo"]
        descripcion = curso["info"]

        # Combinar título y descripción para buscar palabras
        contenido_curso = f"{titulo} {descripcion}"

        # Tokenizar el contenido en palabras
        palabras = re.findall(r'\b\w+\b', contenido_curso.lower())

        # Construir el índice
        palabras_vistas = set()

        for palabra in palabras:
            if palabra not in palabras_innecesarias:
                if palabra not in palabras_vistas:
                    if palabra not in indice:
                        indice[palabra] = [titulo]
                    else:
                        indice[palabra].append(titulo)
                    palabras_vistas.add(palabra)

    return indice


#Función para guardar la estructura html de la página en un archivo txt
def guardar_en_archivo(html_content, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(html_content)
    print(f'Contenido guardado en el archivo: {nombre_archivo}')

#Función que rastrea e indexa la información de la página, guardándo el índice en un archivo txt
def go(n:int, dictionary:str, output:str):

    if n > 38:
        print("El número de páginas solicitado es mayor al número de páginas disponibles")
        print("Paginas disponibles: 38")
        return
    
    if n < 1:
        print("El número de páginas a rastrear debe ser mayor a 0")
        return

    url = "https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"

    # Configura el servicio y el driver de Chrome
    driver = webdriver.Chrome()

    # Abre la URL proporcionada
    driver.get(url)

    # Obtener el HTML completo de la página
    html_content = driver.page_source

    # Pasar el HTML completo a BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    cursos_info = []  # Lista para almacenar los datos de los cursos
    cursos_info_final=[]

    archivo_json = dictionary

    for curso in soup.find_all('li', class_="item-programa ais-Hits-item col-12 m-0 p-0 border-0 shadow-none"):
        titulo = curso.find('b', class_='card-title').text.strip() if curso.find('b',class_='card-title') else 'Título no encontrado'
        enlace = curso.find('a')['href'] if curso.find('a') else 'Enlace no encontrado'
        cursos_info.append({'titulo': titulo, 'enlace': enlace.strip()})
        if len(cursos_info)  >= n*10:
            break

    for curso in cursos_info:
        if (curso.get('enlace'))[0] == "/":
            obtener_elementos_curso(driver,"https://educacionvirtual.javeriana.edu.co"+curso.get('enlace'),curso.get('titulo') ,cursos_info_final)
        else:
            if (curso.get('enlace')).startswith("https://"):
                obtener_elementos_curso(driver,curso.get('enlace'),curso.get('titulo') ,cursos_info_final)
            else:
                obtener_elementos_curso(driver, "https://educacionvirtual.javeriana.edu.co/" + curso.get('enlace'),curso.get('titulo'), cursos_info_final)

    # Guardar en formato JSON
    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(cursos_info_final, archivo, ensure_ascii=False, indent=2)

    print(len(cursos_info))
    print(len(cursos_info_final))

    # Guardar el HTML completo en un archivo
    guardar_en_archivo(html_content, "pagina_completa.txt")

    with open(archivo_json, "r", encoding="utf-8") as archivo:
        catalogo = json.load(archivo)
    
    # Construir el índice
    indice = construir_indice(catalogo)

    # Guardar el índice en un archivo csv
    guardar_indice_csv(indice, output)

    # Cierra el navegador
    driver.quit()

#Función que extrae los datos de un curso dado 
def obtener_elementos_curso(driver,url_curso, titulo,cursos_info_final):
    print(url_curso)
    driver.get(url_curso)
    html_content_curso = driver.page_source
    soup_curso = BeautifulSoup(html_content_curso, 'html.parser')
    descripcion = soup_curso.find('div',class_="course-wrapper-content col-12 col-md-8")
    if descripcion is  None:
        descripcion = soup_curso.find('div', class_="course-wrapper-content course-wrapper-content---top col-12 col-md-8")
    presentacion= descripcion.find('div',class_="course-wrapper-seccion course-wrapper-content--presentation")
    propuesta_valor=descripcion.find('div',class_="course-wrapper-seccion course-wrapper-content--proposal")
    info_español = descripcion.find('div',class_="course-wrapper-seccion seccion-collapsible course-wrapper-content--methodology")
    info_objetivos = descripcion.find('div',class_="course-wrapper-content--objectives-general")

    if presentacion is not None:
        cursos_info_final.append({'titulo': titulo, 'enlace': url_curso,'info':presentacion.text})

    elif propuesta_valor is not None:
        cursos_info_final.append({'titulo': titulo, 'enlace': url_curso,'info':propuesta_valor.text})

    elif info_español is not None:
        cursos_info_final.append({'titulo': titulo, 'enlace': url_curso, 'info': info_español.text})

    elif info_objetivos is not None:
        cursos_info_final.append({'titulo': titulo, 'enlace': url_curso, 'info': info_objetivos.text})

    else:
        print("--uwu--")


if __name__ == "__main__":
    os.system("cls") 
    flag = True
    while  flag:
        op = int(input("Crawler Python\nBIENVENIDO\nSelecciona la opción deseada\n1.Extraer información catálogo de cursos\n2.Comparar cursos\n3. Buscar cursos por intereses\n4. Salir\n"))
        if op == 1:
            os.system("cls") 
            numero_paginas = int(input("Ingrese el número de páginas del catálogo a rastrear\n"))
            dictionary = input("Ingrese el nombre del diccionario de datos (sin la extensión)\n") + ".json"
            BD_mapeo = input("Ingrese el nombre del archivo csv de salida (sin la extensión)\n") + ".csv"
            go(numero_paginas,dictionary,BD_mapeo)

        elif op == 2:
            os.system("cls") 
            curso1 = input("Ingrese el nombre del primer curso a comparar\n")
            curso2 = input("Ingrese el nombre del segundo curso a comparar\n")
            similitud = compare(curso1,curso2)
            print(f"Similitud entre {curso1} y {curso2}: {similitud:.3f}\n")

        elif op == 3:
            os.system("cls") 
            intereses = (input("Ingresa tus intereses separados por espacios\n").split())
            resultados=encontrar_cursos_similares(intereses)
            for puesto, resultado in enumerate(resultados, start=1):
                if (resultado[1]!=0):
                    print(f"{puesto}.{resultado[0]}, similitud: {resultado[1]:.3f}, enlace: {resultado[2]}")
            print("\n")
        elif op == 4:
            os.system("cls") 
            print("Gracias por usar nuestro programa")
            flag = False

        elif op == 5:
            # Tomar el primer archivo CSV encontrado
            archivos_json = glob.glob('*.json')
            if not archivos_json:
                raise FileNotFoundError("No se encontraron archivos JSON en la carpeta.")
            archivo_json = archivos_json[0]
            # Leer el archivo JSON
            with open(archivo_json, "r", encoding="utf-8") as archivo:
                datos_leidos = json.load(archivo)

            # Ahora, datos_leidos contiene la información leída del archivo JSON
            print(datos_leidos)

        else:
            os.system("cls") 
            print("Opción incorrecta")
        