from elasticsearch_dsl import Document, Date, Keyword, Text, connections, Search, Q, GeoPoint, Integer, Float
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
connections.create_connection(hosts=['elasticsearch:9200'])

class Cliente(Document):
    nombre_completo = Text(fields={'raw': Keyword()})
    numero_celular = Keyword()
    correo_electronico = Keyword()
    fecha_nacimiento = Date()
    direccion = Text(fields={'raw': Keyword()})
    geolocalizacion_direccion = GeoPoint()
    fecha_registro = Date()

    class Index:
        name = 'index-clientes'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Cliente.init()

class ClienteBan(Document):
    nombre_cliente = Text(fields={'raw': Keyword()})
    motivo = Text(fields={'raw': Keyword()})
    fecha_baneo = Date()

    class Index:
        name = 'index-ban'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

ClienteBan.init()

class Pelicula(Document):
    duracion_minutos = Integer()
    genero = Text(fields={'raw': Keyword()})
    titulo = Text(fields={'raw': Keyword()})
    titulo_alternativo = Text(fields={'raw': Keyword()})
    fecha_lanzamiento = Date()
    nominaciones_oscar = Integer()
    premios_oscar = Integer()
    actores = Text(fields={'raw': Keyword()})
    costo_unitario = Float()
    numero_copias = Integer()

    class Index:
        name = 'index-peliculas'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Pelicula.init()

def search_client(query):
    s = Search(index='index-clientes').query("multi_match", query=query, fields=['_id', 'nombre_completo'])
    response = s.execute()
    if response.hits:
        return response.hits[0]
    return None

def get_all_clients():
    s = Search(index='index-clientes').source(['_id', 'nombre_completo'])
    response = s.execute()
    return response.hits

def search_pelicula(query):
    s = Search(index='index-peliculas').query(
        Q('multi_match', query=query, fields=['titulo', 'genero', 'actores', 'nominaciones_oscar'])
    )
    response = s.execute()
    if response.hits:
        return response.hits
    return None

def check_cliente_baneado(cliente):
    s = Search(index='index-ban').query(
        Q('term', nombre_cliente=cliente.meta.id) |
        Q('term', _id=cliente.meta.id)
    )
    response = s.execute()
    if response.hits:
        return True
    return False

def search_pelicula(query):
    s = Search(index='index-peliculas').query("multi_match", query=query, fields=['titulo', 'genero', 'actores', 'nominaciones_oscar'])
    response = s.execute()
    if response.hits:
        return response.hits
    return []

def get_all_titles():
    s = Search(index='index-peliculas').source(['titulo'])
    response = s.execute()
    return [hit.titulo for hit in response.hits]

def get_all_genres():
    s = Search(index='index-peliculas').source(['genero'])
    response = s.execute()
    genres = []
    for hit in response.hits:
        if hit.genero not in genres:
            genres.append(hit.genero)
    return genres

def search_movies_by_genre(genre):
    s = Search(index='index-peliculas').query("match", genero=genre)
    response = s.execute()
    if response.hits:
        return response.hits
    return []

def get_all_actors():
    s = Search(index='index-peliculas').source(['actores', 'titulo'])
    response = s.execute()
    actors = []
    for hit in response.hits:
        actor_title = {'actor': hit.actores, 'titulo': hit.titulo}
        if actor_title not in actors:
            actors.append(actor_title)
    return actors

def get_all_movies_ordered_by_nominations():
    s = Search(index='index-peliculas').sort({'nominaciones_oscar': {'order': 'desc'}})
    response = s.execute()
    return response.hits

def main():
    clientes = get_all_clients()

    if not clientes:
        logging.info("No hay clientes registrados.")
        return

    logging.info("Clientes registrados:")
    for cliente in clientes:
        logging.info(f"_id: {cliente.meta.id}, Nombre completo: {cliente.nombre_completo}")

    query = input("Introduce el término de búsqueda (id, nombre): ")
    cliente = search_client(query)

    if cliente is None:
        logging.info(f"No se encontró ningún cliente con el criterio de búsqueda proporcionado '{query}'.")
        return

    if check_cliente_baneado(cliente):
        logging.info(f"El cliente '{cliente.meta.id}' está baneado. No se pueden realizar más operaciones.")
        return
    else:
        logging.info(f"El cliente '{cliente.meta.id}' no está baneado. Puede continuar con las operaciones.")
    
    opcion_busqueda = int(input("Selecciona una opción de búsqueda:\n1. Título\n2. Género\n3. Actores\n4. Nominaciones al Oscar\nOpción: "))

    if opcion_busqueda == 1:
        titles = get_all_titles()
        logging.info("Títulos de películas disponibles:")
        for i, titulo in enumerate(titles):
            logging.info(f"{i+1}. Título: {titulo}")
        
        opcion_pelicula = int(input("Selecciona una película para rentar: "))
        
        if opcion_pelicula < 1 or opcion_pelicula > len(titles):
            logging.info("Opción inválida. Saliendo del programa.")
            return
        
        pelicula_elegida = titles[opcion_pelicula - 1]
        logging.info(f"Se ha rentado la película '{pelicula_elegida}' al cliente '{cliente.meta.id}'.")
    
    elif opcion_busqueda == 2:
        genres = get_all_genres()
        logging.info("Géneros de películas disponibles:")
        for i, genero in enumerate(genres):
            logging.info(f"{i+1}. Género: {genero}")
        
        opcion_genero = int(input("Selecciona un género: "))
        
        if opcion_genero < 1 or opcion_genero > len(genres):
            logging.info("Opción inválida. Saliendo del programa.")
            return
        
        peliculas = search_movies_by_genre(genres[opcion_genero - 1])
        
        if not peliculas:
            logging.info(f"No se encontraron películas con el género '{genres[opcion_genero - 1]}'.")
            return
        
        logging.info("Películas encontradas:")
        for i, pelicula in enumerate(peliculas):
            logging.info(f"{i+1}. Título: {pelicula.titulo}")
        
        opcion_pelicula = int(input("Selecciona una película para rentar: "))
        
        if opcion_pelicula < 1 or opcion_pelicula > len(peliculas):
            logging.info("Opción inválida. Saliendo del programa.")
            return
        
        pelicula_elegida = peliculas[opcion_pelicula - 1]
        logging.info(f"Se ha rentado la película '{pelicula_elegida.titulo}' al cliente '{cliente.meta.id}'.")


    
    elif opcion_busqueda == 3:
        actors = get_all_actors()
        logging.info("Actores de películas disponibles:")
        for i, actor_title in enumerate(actors):
            logging.info(f"{i+1}. Actor: {actor_title['actor']} - Título: {actor_title['titulo']}")
        
        opcion_pelicula = int(input("Selecciona una película para rentar: "))
        
        if opcion_pelicula < 1 or opcion_pelicula > len(actors):
            logging.info("Opción inválida. Saliendo del programa.")
            return
        
        pelicula_elegida = actors[opcion_pelicula - 1]
        logging.info(f"Se ha rentado la película '{pelicula_elegida['titulo']}' al cliente '{cliente.meta.id}'.")

    
    elif opcion_busqueda == 4:
        movies = get_all_movies_ordered_by_nominations()
        logging.info("Películas ordenadas por número de nominaciones al Oscar:")
        for i, pelicula in enumerate(movies):
            logging.info(f"{i+1}. Título: {pelicula.titulo}, Nominaciones al Oscar: {pelicula.nominaciones_oscar}")
        
        opcion_pelicula = int(input("Selecciona una película para rentar: "))
        
        if opcion_pelicula < 1 or opcion_pelicula > len(movies):
            logging.info("Opción inválida. Saliendo del programa.")
            return
        
        pelicula_elegida = movies[opcion_pelicula - 1]
        logging.info(f"Se ha rentado la película '{pelicula_elegida.titulo}' al cliente '{cliente.meta.id}'.")
    
    else:
        logging.info("Opción inválida. Saliendo del programa.")

if __name__ == "__main__":
    main()
