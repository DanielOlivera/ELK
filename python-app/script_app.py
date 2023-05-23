from elasticsearch_dsl import Document, Integer, Float, Text, Keyword, GeoPoint, Date, Search
from elasticsearch_dsl.connections import connections
from datetime import date
import datetime
import random

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


peliculas = [
    {
        "_id": 1,
        "duracion_minutos": 181,
        "genero": "Acción",
        "titulo": "Avengers: Endgame",
        "titulo_alternativo": "Vengadores: Endgame",
        "fecha_lanzamiento": "2019-04-26",
        "nominaciones_oscar": 1,
        "premios_oscar": 1,
        "actores": "Robert Downey Jr., Chris Evans",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 2,
        "duracion_minutos": 128,
        "genero": "Drama",
        "titulo": "La La Land",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2016-12-09",
        "nominaciones_oscar": 14,
        "premios_oscar": 6,
        "actores": "Ryan Gosling, Emma Stone",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 3,
        "duracion_minutos": 180,
        "genero": "Drama",
        "titulo": "The Wolf of Wall Street",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2013-12-25",
        "nominaciones_oscar": 5,
        "premios_oscar": 0,
        "actores": "Leonardo DiCaprio, Jonah Hill",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 4,
        "duracion_minutos": 120,
        "genero": "Acción",
        "titulo": "Mad Max: Fury Road",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2015-05-15",
        "nominaciones_oscar": 10,
        "premios_oscar": 6,
        "actores": "Tom Hardy, Charlize Theron",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 5,
        "duracion_minutos": 156,
        "genero": "Aventura",
        "titulo": "The Revenant",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2015-12-25",
        "nominaciones_oscar": 12,
        "premios_oscar": 3,
        "actores": "Leonardo DiCaprio, Tom Hardy",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 6,
        "duracion_minutos": 120,
        "genero": "Drama",
        "titulo": "The Social Network",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2010-10-01",
        "nominaciones_oscar": 8,
        "premios_oscar": 3,
        "actores": "Jesse Eisenberg, Andrew Garfield",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 7,
        "duracion_minutos": 106,
        "genero": "Drama",
        "titulo": "Whiplash",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2014-10-10",
        "nominaciones_oscar": 5,
        "premios_oscar": 3,
        "actores": "Miles Teller, J.K. Simmons",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 8,
        "duracion_minutos": 165,
        "genero": "Drama",
        "titulo": "Django Unchained",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2012-12-25",
        "nominaciones_oscar": 5,
        "premios_oscar": 2,
        "actores": "Jamie Foxx, Christoph Waltz",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 9,
        "duracion_minutos": 169,
        "genero": "Ciencia ficción",
        "titulo": "Interstellar",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2014-11-07",
        "nominaciones_oscar": 5,
        "premios_oscar": 1,
        "actores": "Matthew McConaughey, Anne Hathaway",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 10,
        "duracion_minutos": 151,
        "genero": "Crimen",
        "titulo": "The Departed",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2006-10-06",
        "nominaciones_oscar": 5,
        "premios_oscar": 4,
        "actores": "Leonardo DiCaprio, Matt Damon",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 11,
        "duracion_minutos": 153,
        "genero": "Bélico",
        "titulo": "Inglourious Basterds",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2009-08-21",
        "nominaciones_oscar": 8,
        "premios_oscar": 1,
        "actores": "Brad Pitt, Christoph Waltz",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 12,
        "duracion_minutos": 165,
        "genero": "Acción",
        "titulo": "The Dark Knight Rises",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2012-07-20",
        "nominaciones_oscar": 8,
        "premios_oscar": 2,
        "actores": "Christian Bale, Tom Hardy",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 13,
        "duracion_minutos": 100,
        "genero": "Comedia",
        "titulo": "The Grand Budapest Hotel",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2014-03-28",
        "nominaciones_oscar": 9,
        "premios_oscar": 4,
        "actores": "Ralph Fiennes, F. Murray Abraham",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 14,
        "duracion_minutos": 91,
        "genero": "Ciencia ficción",
        "titulo": "Eternal Sunshine of the Spotless Mind",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2004-03-19",
        "nominaciones_oscar": 2,
        "premios_oscar": 1,
        "actores": "Jim Carrey, Kate Winslet",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 15,
        "duracion_minutos": 125,
        "genero": "Drama",
        "titulo": "La La Land",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2016-12-09",
        "nominaciones_oscar": 14,
        "premios_oscar": 6,
        "actores": "Ryan Gosling, Emma Stone",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 16,
        "duracion_minutos": 152,
        "genero": "Aventura",
        "titulo": "The Lord of the Rings: The Return of the King",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2003-12-17",
        "nominaciones_oscar": 11,
        "premios_oscar": 11,
        "actores": "Elijah Wood, Ian McKellen",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 17,
        "duracion_minutos": 130,
        "genero": "Aventura",
        "titulo": "The Avengers",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2012-05-04",
        "nominaciones_oscar": 1,
        "premios_oscar": 0,
        "actores": "Robert Downey Jr., Chris Evans",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 18,
        "duracion_minutos": 140,
        "genero": "Acción",
        "titulo": "Mad Max: Fury Road",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2015-05-15",
        "nominaciones_oscar": 10,
        "premios_oscar": 6,
        "actores": "Tom Hardy, Charlize Theron",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 19,
        "duracion_minutos": 130,
        "genero": "Drama",
        "titulo": "Birdman",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2014-10-17",
        "nominaciones_oscar": 9,
        "premios_oscar": 4,
        "actores": "Michael Keaton, Edward Norton",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
         "_id": 20,
        "duracion_minutos": 121,
        "genero": "Drama",
        "titulo": "The Shape of Water",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2017-12-01",
        "nominaciones_oscar": 13,
        "premios_oscar": 4,
        "actores": "Sally Hawkins, Doug Jones",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 21,
        "duracion_minutos": 130,
        "genero": "Aventura",
        "titulo": "Black Panther",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2018-02-16",
        "nominaciones_oscar": 7,
        "premios_oscar": 3,
        "actores": "Chadwick Boseman, Michael B. Jordan",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 22,
        "duracion_minutos": 107,
        "genero": "Drama",
        "titulo": "Moonlight",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2016-10-21",
        "nominaciones_oscar": 8,
        "premios_oscar": 3,
        "actores": "Trevante Rhodes, Mahershala Ali",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 23,
        "duracion_minutos": 105,
        "genero": "Drama",
        "titulo": "Boyhood",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2014-07-11",
        "nominaciones_oscar": 6,
        "premios_oscar": 1,
        "actores": "Ellar Coltrane, Patricia Arquette",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 24,
        "duracion_minutos": 124,
        "genero": "Comedia",
        "titulo": "Juno",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2007-12-05",
        "nominaciones_oscar": 4,
        "premios_oscar": 1,
        "actores": "Elliot Page, Michael Cera",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 25,
        "duracion_minutos": 101,
        "genero": "Drama",
        "titulo": "La La Land",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2016-12-09",
        "nominaciones_oscar": 14,
        "premios_oscar": 6,
        "actores": "Ryan Gosling, Emma Stone",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 26,
        "duracion_minutos": 134,
        "genero": "Drama",
        "titulo": "Her",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2013-12-18",
        "nominaciones_oscar": 5,
        "premios_oscar": 1,
        "actores": "Joaquin Phoenix, Scarlett Johansson",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 27,
        "duracion_minutos": 90,
        "genero": "Drama",
        "titulo": "Cuestión de Fe",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2010-07-01",
        "nominaciones_oscar": 0,
        "premios_oscar": 0,
        "actores": "Jorge Ortiz, Erika Andia",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 28,
        "duracion_minutos": 120,
        "genero": "Comedia",
        "titulo": "El Día que Murió el Silencio",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2018-08-02",
        "nominaciones_oscar": 0,
        "premios_oscar": 0,
        "actores": "Roberto Guilhon, Andrea Camponovo",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 29,
        "duracion_minutos": 95,
        "genero": "Drama",
        "titulo": "Olvidados",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2014-07-02",
        "nominaciones_oscar": 0,
        "premios_oscar": 0,
        "actores": "Damian Gasco, Bernardo Peña",
        "costo_unitario": 9.99,
        "numero_copias": 100
    },
    {
        "_id": 30,
        "duracion_minutos": 110,
        "genero": "Documental",
        "titulo": "Bellas Durmientes",
        "titulo_alternativo": "",
        "fecha_lanzamiento": "2018-02-15",
        "nominaciones_oscar": 0,
        "premios_oscar": 0,
        "actores": "Documental",
        "costo_unitario": 9.99,
        "numero_copias": 100
    }
]

for pelicula_data in peliculas:
    existing_pelicula = Pelicula.search().query(
        'match', titulo=pelicula_data['titulo']
    ).execute()

    if existing_pelicula.hits.total.value > 0:
        print(f"La pelicula '{pelicula_data['titulo']}' ya existe en el indice. No se agregara nuevamente.")
        continue

    pelicula = Pelicula(**pelicula_data)
    pelicula.save()
    print(f"La pelicula '{pelicula.titulo}' ha sido agregada al indice.")

print("Proceso completado.")


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


clientes = [
  {
    "_id": 1,
    "nombre_completo": "Carlos Aguilar",
    "numero_celular": "71234567",
    "correo_electronico": "carlos1@gmail.com",
    "fecha_nacimiento": "1990-05-15",
    "direccion": "Calle Murillo 123",
    "geolocalizacion_direccion": "-16.498200,-68.139700",
    "fecha_registro": "2022-01-20"
  },
  {
    "_id": 2,
    "nombre_completo": "Laura Ramirez",
    "numero_celular": "61234567",
    "correo_electronico": "laura2@outlook.com",
    "fecha_nacimiento": "1985-12-10",
    "direccion": "Avenida 16 de Julio 456",
    "geolocalizacion_direccion": "-16.498600,-68.139400",
    "fecha_registro": "2022-02-15"
  },
  {
    "_id": 3,
    "nombre_completo": "Luis Torres",
    "numero_celular": "61234568",
    "correo_electronico": "luis3@gmail.com",
    "fecha_nacimiento": "1992-07-22",
    "direccion": "Calle Illampu 789",
    "geolocalizacion_direccion": "-16.498900,-68.139100",
    "fecha_registro": "2022-03-10"
  },
  {
    "_id": 4,
    "nombre_completo": "Maria Gutierrez",
    "numero_celular": "71234568",
    "correo_electronico": "maria4@outlook.com",
    "fecha_nacimiento": "1993-03-28",
    "direccion": "Avenida Camacho 321",
    "geolocalizacion_direccion": "-16.499200,-68.138800",
    "fecha_registro": "2022-04-25"
  },
  {
    "_id": 5,
    "nombre_completo": "Juan Perez",
    "numero_celular": "71234569",
    "correo_electronico": "juan5@gmail.com",
    "fecha_nacimiento": "1995-09-18",
    "direccion": "Calle Comercio 654",
    "geolocalizacion_direccion": "-16.499500,-68.138500",
    "fecha_registro": "2022-05-15"
  },
  {
    "_id": 6,
    "nombre_completo": "Carolina Lopez",
    "numero_celular": "61234569",
    "correo_electronico": "carolina6@outlook.com",
    "fecha_nacimiento": "1991-11-05",
    "direccion": "Avenida Montes 987",
    "geolocalizacion_direccion": "-16.499800,-68.138200",
    "fecha_registro": "2022-06-10"
  },
  {
    "_id": 7,
    "nombre_completo": "Roberto Castro",
    "numero_celular": "61234570",
    "correo_electronico": "roberto7@gmail.com",
    "fecha_nacimiento": "1988-08-12",
    "direccion": "Calle Yanacocha 321",
    "geolocalizacion_direccion": "-16.500100,-68.137900",
    "fecha_registro": "2022-07-20"
  },
  {
    "_id": 8,
    "nombre_completo": "Fernanda Castro",
    "numero_celular": "61234571",
    "correo_electronico": "fernanda8@outlook.com",
    "fecha_nacimiento": "1995-05-18",
    "direccion": "Avenida Sucre 654",
    "geolocalizacion_direccion": "-16.500400,-68.137600",
    "fecha_registro": "2022-08-15"
  },
  {
    "_id": 9,
    "nombre_completo": "Pedro Mendez",
    "numero_celular": "71234571",
    "correo_electronico": "pedro9@gmail.com",
    "fecha_nacimiento": "1990-02-25",
    "direccion": "Calle Illimani 987",
    "geolocalizacion_direccion": "-16.500700,-68.137300",
    "fecha_registro": "2022-09-10"
  },
  {
    "_id": 10,
    "nombre_completo": "Silvia Herrera",
    "numero_celular": "71234572",
    "correo_electronico": "silvia10@outlook.com",
    "fecha_nacimiento": "1993-07-08",
    "direccion": "Avenida Ballivian 321",
    "geolocalizacion_direccion": "-16.501000,-68.137000",
    "fecha_registro": "2022-10-25"
  },
  {
    "_id": 11,
    "nombre_completo": "Eduardo Rojas",
    "numero_celular": "61234572",
    "correo_electronico": "eduardo11@gmail.com",
    "fecha_nacimiento": "1985-04-15",
    "direccion": "Calle Murillo 654",
    "geolocalizacion_direccion": "-16.501300,-68.136700",
    "fecha_registro": "2022-11-15"
  },
  {
    "_id": 12,
    "nombre_completo": "Ana Montes",
    "numero_celular": "61234573",
    "correo_electronico": "ana12@outlook.com",
    "fecha_nacimiento": "1992-01-22",
    "direccion": "Avenida 16 de Julio 987",
    "geolocalizacion_direccion": "-16.501600,-68.136400",
    "fecha_registro": "2022-12-10"
  },
  {
    "_id": 13,
    "nombre_completo": "Oscar Mendez",
    "numero_celular": "71234573",
    "correo_electronico": "oscar13@gmail.com",
    "fecha_nacimiento": "1988-06-28",
    "direccion": "Calle Illampu 321",
    "geolocalizacion_direccion": "-16.501900,-68.136100",
    "fecha_registro": "2023-01-25"
  },
  {
    "_id": 14,
    "nombre_completo": "Camila Gutierrez",
    "numero_celular": "71234574",
    "correo_electronico": "camila14@outlook.com",
    "fecha_nacimiento": "1991-09-10",
    "direccion": "Avenida Camacho 654",
    "geolocalizacion_direccion": "-16.502200,-68.135800",
    "fecha_registro": "2023-02-15"
  },
  {
    "_id": 15,
    "nombre_completo": "Sebastian Perez",
    "numero_celular": "61234574",
    "correo_electronico": "sebastian15@gmail.com",
    "fecha_nacimiento": "1995-03-18",
    "direccion": "Calle Comercio 987",
    "geolocalizacion_direccion": "-16.502500,-68.135500",
    "fecha_registro": "2023-03-10"
  },
  {
    "_id": 16,
    "nombre_completo": "Natalia Lopez",
    "numero_celular": "61234575",
    "correo_electronico": "natalia16@outlook.com",
    "fecha_nacimiento": "1990-07-05",
    "direccion": "Avenida Montes 321",
    "geolocalizacion_direccion": "-16.502800,-68.135200",
    "fecha_registro": "2023-04-25"
  },
  {
    "_id": 17,
    "nombre_completo": "Miguel Castro",
    "numero_celular": "71234575",
    "correo_electronico": "miguel17@gmail.com",
    "fecha_nacimiento": "1989-02-12",
    "direccion": "Calle Yanacocha 987",
    "geolocalizacion_direccion": "-16.503100,-68.134900",
    "fecha_registro": "2023-05-15"
  },
  {
    "_id": 18,
    "nombre_completo": "Valentina Castro",
    "numero_celular": "61234576",
    "correo_electronico": "valentina18@outlook.com",
    "fecha_nacimiento": "1994-05-28",
    "direccion": "Avenida Sucre 654",
    "geolocalizacion_direccion": "-16.503400,-68.134600",
    "fecha_registro": "2023-06-10"
  },
  {
    "_id": 19,
    "nombre_completo": "Andres Mendez",
    "numero_celular": "61234577",
    "correo_electronico": "andres19@gmail.com",
    "fecha_nacimiento": "1993-08-15",
    "direccion": "Calle Illimani 987",
    "geolocalizacion_direccion": "-16.503700,-68.134300",
    "fecha_registro": "2023-07-20"
  },
  {
    "_id": 20,
    "nombre_completo": "Isabella Herrera",
    "numero_celular": "71234577",
    "correo_electronico": "isabella20@outlook.com",
    "fecha_nacimiento": "1991-12-08",
    "direccion": "Avenida Ballivian 321",
    "geolocalizacion_direccion": "-16.504000,-68.134000",
    "fecha_registro": "2023-08-15"
  }
]

for cliente_data in clientes:
    existing_cliente = Cliente.search().query(
        'match', nombre_completo=cliente_data['nombre_completo']
    ).execute()

    if existing_cliente.hits.total.value > 0:
        print(f"El cliente '{cliente_data['nombre_completo']}' ya existe en el indice. No se agregara nuevamente.")
        continue

    cliente = Cliente(**cliente_data)
    cliente.save()
    print(f"El cliente '{cliente.nombre_completo}' ha sido agregado al índice.")
    
print("Proceso completado.")


class Renta(Document):
    id_cliente = Integer()
    cliente = Text()
    fecha_prestamo = Date()
    fecha_devolucion = Date()
    importe_total = Float()
    peliculas_prestadas = Text()
    status = Text()
    multa = Integer()

    class Index:
        name = 'index-rentas'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Renta.init()

class EstadoMultas(Document):
    estado = Text()
    multas = Float()

    class Index:
        name = 'index-estadomultas'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

EstadoMultas.init()

class Costo(Document):
    dias = Integer(multi=True)
    costos = Float(multi=True)

    class Index:
        name = 'index-costos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Costo.init()

class Descuento(Document):
    cantidades = Integer(multi=True)
    porcentajes = Float(multi=True)

    class Index:
        name = 'index-descuentos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Descuento.init()

def get_all_discounts():
    s = Search(index='index-descuentos')
    response = s.execute()
    if response.hits:
        descuentos = {
            'cantidades': response.hits[0].cantidades,
            'porcentajes': response.hits[0].porcentajes
        }
        return descuentos
    return None

clientes = clientes = [
    {
        "nombre_completo": "Carlos Aguilar",
        "_id": 1
    },
    {
        "nombre_completo": "Laura Ramirez",
        "_id": 2
    },
    {
        "nombre_completo": "Luis Torres",
        "_id": 3
    },
    {
        "nombre_completo": "Maria Gutierrez",
        "_id": 4
    },
    {
        "nombre_completo": "Juan Perez",
        "_id": 5
    },
    {
        "nombre_completo": "Carolina Lopez",
        "_id": 6
    },
    {
        "nombre_completo": "Roberto Castro",
        "_id": 7
    },
    {
        "nombre_completo": "Fernanda Castro",
        "_id": 8
    },
    {
        "nombre_completo": "Pedro Mendez",
        "_id": 9
    },
    {
        "nombre_completo": "Silvia Herrera",
        "_id": 10
    },
    {
        "nombre_completo": "Eduardo Rojas",
        "_id": 11
    },
    {
        "nombre_completo": "Ana Montes",
        "_id": 12
    },
    {
        "nombre_completo": "Oscar Mendez",
        "_id": 13
    },
    {
        "nombre_completo": "Camila Gutierrez",
        "_id": 14
    },
    {
        "nombre_completo": "Sebastian Perez",
        "_id": 15
    },
    {
        "nombre_completo": "Natalia Lopez",
        "_id": 16
    },
    {
        "nombre_completo": "Miguel Castro",
        "_id": 17
    },
    {
        "nombre_completo": "Valentina Castro",
        "_id": 18
    },
    {
        "nombre_completo": "Andres Mendez",
        "_id": 19
    },
    {
        "nombre_completo": "Isabella Herrera",
        "_id": 20
    }
]

peliculas =  [
    {
        "titulo": "Avengers: Endgame",
        "_id": 1
    },
    {
        "titulo": "La La Land",
        "_id": 2
    },
    {
        "titulo": "The Wolf of Wall Street",
        "_id": 3
    },
    {
        "titulo": "Mad Max: Fury Road",
        "_id": 4
    },
    {
        "titulo": "The Revenant",
        "_id": 5
    },
    {
        "titulo": "The Social Network",
        "_id": 6
    },
    {
        "titulo": "Whiplash",
        "_id": 7
    },
    {
        "titulo": "Django Unchained",
        "_id": 8
    },
    {
        "titulo": "Interstellar",
        "_id": 9
    },
    {
        "titulo": "The Departed",
        "_id": 10
    },
    {
        "titulo": "Inglourious Basterds",
        "_id": 11
    },
    {
        "titulo": "The Dark Knight Rises",
        "_id": 12
    },
    {
        "titulo": "The Grand Budapest Hotel",
        "_id": 13
    },
    {
        "titulo": "Eternal Sunshine of the Spotless Mind",
        "_id": 14
    },
    {
        "titulo": "La La Land", 
        "_id": 15
    },
    {
        "titulo": "The Lord of the Rings: The Return of the King",
        "_id": 16
    },
    {
        "titulo": "The Avengers",
        "_id": 17
    },
    {
        "titulo": "Mad Max: Fury Road",
        "_id": 18
    },
    {
        "titulo": "Birdman",
        "_id": 19
    },
    {
        "titulo": "The Shape of Water",
        "_id": 20
    },
    {
        "titulo": "Black Panther",
        "_id": 21
    },
    {
        "titulo": "Moonlight",
        "_id": 22
    },
    {
        "titulo": "Boyhood",
        "_id": 23
    },
    {
        "titulo": "Juno",
        "_id": 24
    },
    {
        "titulo": "La La Land",
        "_id": 25
    },
    {
        "titulo": "Her",
        "_id": 26
    },
    {
        "titulo": "Cuestión de Fe",
        "_id": 27
    },
    {
        "titulo": "El Día que Murió el Silencio",
        "_id": 28
    },
    {
        "titulo": "Olvidados",
        "_id": 29
    },
    {
        "titulo": "Bellas Durmientes",
        "_id": 30
    }
]

rentas = []
next_id = 0

for _ in range(40):
    
    cliente = random.choice(clientes)
    num_peliculas_prestadas = random.randint(1, 5)
    peliculas_prestadas = random.sample(peliculas, num_peliculas_prestadas)
    peliculas_prestadas = ", ".join([f"{pelicula['titulo']}" for pelicula in peliculas_prestadas])
    dia_prestamo = random.randint(1, 22) ### MODIFICAR ESTO
    fecha_prestamo = datetime.date(2023, 5, dia_prestamo)
    diferencia_dias = random.randint(1, 5)
    fecha_devolucion = fecha_prestamo + datetime.timedelta(days=diferencia_dias)
    if fecha_devolucion.month != fecha_prestamo.month:
        for dia in range(1, fecha_devolucion.day + 1):
            fecha_devolucion = datetime.date(2023, fecha_prestamo.month + 1, dia)
    fecha_prestamo_formatted = fecha_prestamo.strftime("%Y-%m-%d")
    fecha_devolucion_formatted = fecha_devolucion.strftime("%Y-%m-%d")
     
    date_now = date.today()
    diferencia_dias_calc = (date_now - fecha_prestamo).days
    print(diferencia_dias_calc)
    
    estado = EstadoMultas.search().source(['estado']).execute()
    estados_posibles = [hit.estado for hit in estado.hits]
    #status = random.choice(estados_posibles[0])

    descuento = None
    descuentos = get_all_discounts()
    for i in range(len(descuentos['cantidades'])):
        if num_peliculas_prestadas >= int(descuentos['cantidades'][i]):
            descuento = int(descuentos['porcentajes'][i])
    if descuento is None:
        descuento = 0
    
    costo = Costo.search().source(['dias','costos']).execute()
    dias = costo.hits[0].dias
    costos = costo.hits[0].costos
    importe_total=0
    
    if diferencia_dias_calc <= 5:
        status = estados_posibles[0][1]
        if diferencia_dias_calc in dias:
            if diferencia_dias_calc in dias:
                posicion = dias.index(int(diferencia_dias_calc))
                costo_renta = costos[posicion]
            importe_total = (costo_renta - (costo_renta * (descuento / 100)))*num_peliculas_prestadas
            print("En Curso")
            Renta.importe_total = importe_total

  
    elif diferencia_dias_calc > 5 and diferencia_dias_calc <= 10:
        status = random.choice([estados_posibles[0][0], estados_posibles[0][2]])
        if status == 'Devuelto': #Mejorar Logica
            print("Devuelto") #Mejorar Logica
            Renta.importe_total = 1111 #Mejorar Logica
        elif status == 'En Mora': #Mejorar Logica
            print("En Mora") #Mejorar Logica
            Renta.importe_total = 2222 #Mejorar Logica
        

    elif diferencia_dias_calc > 10:
        status = random.choice([estados_posibles[0][0], estados_posibles[0][3]])
        if status == 'Devuelto': #Mejorar Logica
            print("Devuelto") #Mejorar Logica
            Renta.importe_total = 1111 #Mejorar Logica
        elif status == 'Perdido': #Mejorar Logica
            print("Perdido") #Mejorar Logica
            Renta.importe_total = 3333 #Mejorar Logica
            
    multa = 0

    renta = Renta(
        id_cliente=cliente["_id"],
        cliente=cliente["nombre_completo"],
        fecha_prestamo=fecha_prestamo,
        fecha_devolucion=fecha_devolucion,
        importe_total=importe_total,
        peliculas_prestadas=peliculas_prestadas,
        status=status,
        multa=multa
    )  
    
    print(f"El cliente '{renta.cliente}' rento las siguientes peliculas '{renta.peliculas_prestadas}'")
    print(f"Fecha de renta '{renta.fecha_prestamo}', durante: '{diferencia_dias}' dias, hasta el: '{renta.fecha_devolucion}'")
   
    rentas.append(renta)

for renta in rentas:
    renta.save()