from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

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
        if len(cursos_info)  == n*10:
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
    numero_paginas = 4
    dictionary = "info_cursos.json"
    BD_mapeo = "datos_mapeo.csv"
    go(numero_paginas,dictionary,BD_mapeo)
