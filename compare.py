import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import glob
import json

def compare_cursos(curso1, curso2):
    
    # Tomar el primer archivo CSV encontrado
    archivos_csv = glob.glob('*.csv')
    if not archivos_csv:
        raise FileNotFoundError("No se encontraron archivos CSV en la carpeta.")
    archivo_csv = archivos_csv[0]

    # Lee el archivo CSV especificando el separador y manejando comillas
    df = pd.read_csv(archivo_csv)
    
    # Combinar las palabras por curso
    cursos_palabras = df.groupby('Curso')['Palabra'].apply(lambda x: ' '.join(x)).reset_index()

    # Crear un vectorizador TF-IDF
    vectorizador = TfidfVectorizer()

    # Ajustar y transformar los datos con el vectorizador
    matriz_tfidf = vectorizador.fit_transform(cursos_palabras['Palabra'])

    # Obtener los índices de los cursos
    indices_cursos = cursos_palabras.set_index('Curso').index

    # Verificar si los cursos ingresados existen en el conjunto de datos
    if curso1 not in indices_cursos or curso2 not in indices_cursos:
        return "Uno o ambos cursos no se encuentran en el conjunto de datos."

    # Obtener los vectores TF-IDF para los cursos ingresados
    vector_curso1 = matriz_tfidf[indices_cursos.get_loc(curso1)].toarray()
    vector_curso2 = matriz_tfidf[indices_cursos.get_loc(curso2)].toarray()

    # Calcular la similitud del coseno entre los vectores
    similitud = cosine_similarity(vector_curso1, vector_curso2)[0][0]

    return similitud

