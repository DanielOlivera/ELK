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
        return response.hits[0]
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

def main():
    clientes = get_all_clients()

    if not clientes:
        logging.info("No hay clientes registrados.")
        return

    logging.info("Clientes registrados:")
    for cliente in clientes:
        logging.info(f"_id: {cliente.meta.id}, Nombre completo: {cliente.nombre_completo}")

    query = input("Introduce el termino de busqueda (id, nombre): ")
    cliente = search_client(query)

    if cliente is None:
        logging.info(f"No se encontro ningun cliente con el criterio de busqueda proporcionado '{query}'.")
        return

    if check_cliente_baneado(cliente):
        logging.info(f"El cliente '{cliente.meta.id}' está baneado. No se pueden realizar más operaciones.")
        return
    else:
        logging.info(f"El cliente '{cliente.meta.id}' no está baneado. Puede continuar con las operaciones.")
        
    query = input("Introduce el termino de busqueda (titulo, genero, actores, nominaciones_oscar): ")
    pelicula = search_pelicula(query)
    
    if pelicula is None:
        logging.info(f"No se encontró ninguna película con el criterio de búsqueda proporcionado '{query}'.")
    else:
        logging.info(f"Película encontrada:")
        logging.info(f"Título: {pelicula.titulo}")
        logging.info(f"Género: {pelicula.genero}")
        logging.info(f"Actores: {pelicula.actores}")
        logging.info(f"Nominaciones al Oscar: {pelicula.nominaciones_oscar}")

if __name__ == "__main__":
    main()
