import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import glob
import json

def encontrar_cursos_similares(palabras):
    # Tomar el primer archivo CSV encontrado
    archivos_csv = glob.glob('*.csv')
    if not archivos_csv:
        raise FileNotFoundError("No se encontraron archivos CSV en la carpeta.")
    archivo_csv = archivos_csv[0]

    # Leer el archivo CSV especificando el separador y manejando comillas
    df = pd.read_csv(archivo_csv, sep='|')
    
    # Tomar el primer archivo JSON encontrado
    archivos_json = glob.glob('*.json')
    if not archivos_json:
        raise FileNotFoundError("No se encontraron archivos JSON en la carpeta.")
    archivo_json = archivos_json[0]

    # Leer el archivo JSON
    with open(archivo_json, "r", encoding="utf-8") as archivo:
        datos_leidos = json.load(archivo)

    # Combinar las palabras por curso
    cursos_palabras = df.groupby('Curso')['Palabra'].apply(lambda x: ' '.join(x)).reset_index()

    # Crear un vectorizador TF-IDF
    vectorizador = TfidfVectorizer()

    # Ajustar y transformar los datos con el vectorizador
    matriz_tfidf = vectorizador.fit_transform(cursos_palabras['Palabra'])

    # Obtener los índices de los cursos
    indices_cursos = cursos_palabras.set_index('Curso').index

    # Crear un vector TF-IDF para las palabras ingresadas
    vector_palabras = vectorizador.transform([' '.join(palabras)]).toarray()

    # Calcular la similitud del coseno entre el vector de palabras ingresadas y los vectores de los cursos
    similitudes = cosine_similarity(vector_palabras, matriz_tfidf)[0]

    # Obtener las parejas (curso, similitud) ordenadas por similitud en orden descendente
    parejas_similitud = list(zip(cursos_palabras['Curso'][1:], similitudes[1:]))
    parejas_similitud = sorted(parejas_similitud, key=lambda x: x[1], reverse=True)

    # Tomar el top 5 de similitud
    top_5_similitud = parejas_similitud[:5]

    # Obtener los enlaces de los cursos correspondientes al top 5
    top_5_con_enlaces = [(curso, similitud, next(item['enlace'] for item in datos_leidos if item['titulo'] == curso)) for curso, similitud in top_5_similitud]

    # Guardar las consultas en un archivo SQL
    with open("consultas.sql", "w") as archivo_sql:
        for palabra in palabras:
            consulta = f"SELECT Curso FROM datos_modelo WHERE Palabra='{palabra}'\n"
            archivo_sql.write(consulta)

    return top_5_con_enlaces