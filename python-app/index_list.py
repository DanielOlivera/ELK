from elasticsearch_dsl import Document, Date, Keyword, Text, GeoPoint, Integer, Float
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['elasticsearch:9200'])

'''--------------INDEX PELICULA--------------'''

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

'''--------------INDEX CLIENTE--------------'''

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

'''--------------INDEX RENTA--------------'''

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

'''--------------INDEX BAN--------------'''

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

'''--------------INDEX COSTO--------------'''

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

'''--------------INDEX DESCUENTO--------------'''

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

'''--------------INDEX REGISTRORESTA--------------'''

class RegistroResta(Document):
    titulo = Text(fields={'raw': Keyword()})
    motivo = Text(fields={'raw': Keyword()})
    cantidad_resta = Integer()
    fecha_registro = Date()

    class Index:
        name = 'index-substract'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
        
RegistroResta.init()

'''--------------INDEX RENTAHISTORIAL--------------'''

class RentaHistorial(Document):
    cliente_nombre = Text()
    peliculas_prestadas = Text()

    class Index:
        name = 'index-renta-historial'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
        
RentaHistorial.init()

'''--------------INDEX ESTADOMULTAS--------------'''

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