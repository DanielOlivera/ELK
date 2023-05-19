from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Float
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
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
pelicula = Pelicula()

def validate_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            logging.info("Debes introducir un numero entero. Intentalo de nuevo.")

def validate_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            logging.info("Debes introducir un numero. Intentalo de nuevo.")

def validate_date(prompt):
    while True:
        date_string = input(prompt)
        try:
            return datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            logging.info("Debes introducir una fecha en el formato AAAA-MM-DD. Intentalo de nuevo.")


def main():           
    
    s = Search(index='index-peliculas').sort({'_id': {'order': 'desc'}})
    response = s.execute()

    if response.hits.total.value > 0:
        last_id = int(response.hits[0].meta.id)
    else:
        last_id = -1

    next_id = last_id + 1
    pelicula = Pelicula(meta={'id': str(next_id)})

    pelicula.duracion_minutos = validate_integer("Introduce la duracion de la pelicula en minutos: ")
    pelicula.genero = input("Introduce el genero de la pelicula: ")
    pelicula.titulo = input("Introduce el titulo de la pelicula: ")
    pelicula.titulo_alternativo = input("Introduce el titulo alternativo de la pelicula: ")
    pelicula.fecha_lanzamiento = validate_date("Introduce la fecha de lanzamiento de la pelicula (formato: AAAA-MM-DD): ")
    pelicula.nominaciones_oscar = validate_integer("Introduce el numero de nominaciones al Oscar de la pelicula: ")
    pelicula.premios_oscar = validate_integer("Introduce el numero de premios Oscar que la pelicula ha ganado: ")
    pelicula.actores = input("Introduce los actores principales de la pelicula: ")
    pelicula.costo_unitario = validate_float("Introduce el costo unitario de la pelicula: ")
    pelicula.numero_copias = validate_integer("Introduce el numero de copias de la pelicula: ")

    pelicula.save()
    logging.info(f"Pelicula '{pelicula.titulo}' almacenada correctamente.")
    
if __name__ == "__main__":
    main()