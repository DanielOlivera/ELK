from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Float, Search
from elasticsearch_dsl.connections import connections
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
connections.create_connection(hosts=['elasticsearch:9200'])

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

class RegistroResta(Document):
    cantidad_resta = Integer()
    motivo = Text(fields={'raw': Keyword()})
    fecha_registro = Date()

    class Index:
        name = 'index-substract'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

RegistroResta.init()

def validate_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            logging.info("Debes introducir un numero entero. Intenta de nuevo.")
            
def validate_action(prompt):
    while True:
        accion = input(prompt).lower()
        if accion == "a" or accion == "r" or accion == "x":
            return accion
        logging.info("Accion no valida. Introduce 'a' para añadir copias o 'r' para restar copias (x para cancelar operacion). Intenta de nuevo.")

def add_copies(pelicula):
    num_copias = validate_integer("Introduce el número de copias a añadir: ")
    pelicula_obj = Pelicula.get(id=pelicula.meta.id)
    pelicula_obj.numero_copias += num_copias
    pelicula_obj.save()
    logging.info(f"Se añadieron {num_copias} copias a la pelicula '{pelicula_obj.titulo}'.")
   
def subtract_copies(pelicula):
    num_copias = validate_integer("Introduce el numero de copias a restar: ")
    razon_resta = input("Introduce la razon de la resta de copias: ")
    
    pelicula_obj = Pelicula.get(id=pelicula.meta.id)
    pelicula_obj.numero_copias -= num_copias
    pelicula_obj.save()
    
    ###Aumentar al nuevo DOC la pelicula a la que se le resto unidades
    
    registro_resta = RegistroResta(cantidad_resta=num_copias, motivo=razon_resta, fecha_registro=datetime.now())
    registro_resta.save()
    
    logging.info(f"Se restaron {num_copias} copias de la pelicula '{pelicula_obj.titulo}' por la siguiente razon: {razon_resta}.")

def get_movie(query):
    s = Search(index='index-peliculas').query("multi_match", query=query, fields=['titulo', '_id'])
    response = s.execute()
    if response.hits:
        return response.hits[0]
    return None

def get_all_movies():
    s = Search(index='index-peliculas').source(['_id', 'titulo', 'numero_copias'])
    response = s.execute()
    return response.hits

def main():
    
    peliculas = get_all_movies()

    if not peliculas:
        logging.info("No hay peliculas registradas en el indice 'index-peliculas'.")
        return

    logging.info("Películas registradas en el indice 'index-peliculas':")
    for pelicula in peliculas:
        logging.info(f"_id: {pelicula.meta.id}, Titulo: {pelicula.titulo}, Numero de Copias: {pelicula.numero_copias}")
    
    query = input("Introduce el titulo o _id de la pelicula: ")
    pelicula = get_movie(query)

    if pelicula is None:
        logging.info(f"No se encontro ninguna pelicula con el titulo '{query}'.")
        return

    logging.info(f"Se encontro la pelicula '{pelicula.titulo}' con {pelicula.numero_copias} copias.")

    accion = validate_action("¿Deseas añadir o restar copias? (a/r/x): ")

    if accion.lower() == "a":
        add_copies(pelicula)
    elif accion.lower() == "r":
        subtract_copies(pelicula)
    elif accion.lower() == "x":
        logging.info("Operacion cancelada. Saliendo del programa.")
    else:
        logging.info("Accion no valida. Saliendo del programa.")

if __name__ == "__main__":
    main()
