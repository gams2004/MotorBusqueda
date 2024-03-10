# MotorBusqueda
Proyecto en Python que extrae del catálogo de cursos de la Pontificia Universidad Javeriana los cursos junto a su información, la indexa y te permite buscar cursos por palabras clave.

Con este proyecto se buscan responder las preguntas:
1. Dada la consulta de una palabra en los cursos de la Universidad, ¿cómo mostrar las URLs
por orden de relevancia?

   R/ A través del uso de la función Compare() podemos determinar la relevancia de cada curso encontrado generando un porcentaje de similitud entre cursos con los intereses del usuario.

2. ¿Qué métrica de similitud se debe definir para comparar dos cursos?

   R/ La métrica de similitud que definimos es a través del uso de vectores TF-IDF, los cuales compararemos con las funciones de seno y coseno, generando el porcentaje de similitud entre cursos.

3. Dado un listado de intereses, por ejemplo [‘musica’, ‘composicion’, ‘instrumento’], el buscador debe retornar los cursos que más se relacionan a los intereses del usuario.

   a) ¿Cómo se define una medida de similitud entre los cursos, y entre los cursos e intereses?

      R/ Esta medida se define utlizando las funciones de seno y coseno, las cuales comparan la similitud de los cursos e intereses en términos de vectores para encontrar sus respectivas similitudes.

   b) ¿Son dos métricas diferentes? ¿puede usar la misma métrica del punto anterior?

      R/ Se puede utilizar la misma métrica pero adecuada al contexto de cada problema. Para comparar dos cursos se tienen en cuenta todas las palabras claves que surgen de su indexación, las cuales se procesan de la forma descrita anteriormente. Sin embargo, para comparar los intereses, es necesario tener en cuenta que se van a tener menos palabras que comparar, lo cual generará una métrica diferente. Teniendo esto en cuenta, se pueden utilizar las mismas métricas pero adecuadas al caso.
