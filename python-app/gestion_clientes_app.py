from elasticsearch_dsl import Document, Date, Keyword, Text, GeoPoint
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from datetime import datetime
import logging
import folium
import os

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

mapas_directory = "mapas"
if not os.path.exists(mapas_directory):
    os.makedirs(mapas_directory)

def validate_date(prompt):
    while True:
        date_string = input(prompt)
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            logging.info("Debes introducir una fecha en el formato AAAA-MM-DD. Intenta de nuevo.")

def validate_email(prompt):
    while True:
        email = input(prompt)
        if '@' in email:
            return email
        else:
            logging.info("Debes introducir una direccion de correo electronico valida. Intenta de nuevo.")

def validate_phone(prompt):
    while True:
        phone = input(prompt)
        if phone.isdigit() and len(phone) == 8:
            return phone
        else:
            logging.info("Debes introducir un numero de celular valido (8 digitos numericos). Intenta de nuevo.")

def validate_geolocation(prompt):
    while True:
        geolocation = input(prompt)
        try:
            lat, lon = map(float, geolocation.split(','))
            return f"{lat},{lon}"
        except ValueError:
            logging.info("Debes introducir la geolocalización en el formato 'lat,lon'. Inténtalo de nuevo.")

def create_map(geolocalizacion):
    geoloc = geolocalizacion.split(',')
    lat = float(geoloc[0])
    lon = float(geoloc[1])
    mapa = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon]).add_to(mapa)
    return mapa

def main():
    
    s = Search(index='index-clientes').sort({'_id': {'order': 'desc'}})
    response = s.execute()

    if response.hits.total.value > 0:
        last_id = int(response.hits[0].meta.id)
    else:
        last_id = -1

    next_id = last_id + 1
    cliente = Cliente(meta={'id': str(next_id)})

    cliente.nombre_completo = input("Introduce el nombre completo del cliente: ")
    cliente.numero_celular = validate_phone("Introduce el numero de celular del cliente: ")
    cliente.correo_electronico = validate_email("Introduce el correo electronico del cliente: ")
    cliente.fecha_nacimiento = validate_date("Introduce la fecha de nacimiento del cliente (formato: AAAA-MM-DD): ")
    cliente.direccion = input("Introduce la direccion del cliente: ")
    cliente.geolocalizacion_direccion = validate_geolocation("Introduce la geolocalizacion de la direccion del cliente (latitud longitud): ")
    cliente.fecha_registro = datetime.now().date()

    cliente.save()
    logging.info(f"Cliente '{cliente.nombre_completo}' registrado correctamente.")

    accion = input("¿Deseas visualizar la ubicacion del cliente en el mapa? (s/n): ")

    if accion.lower() == "s":
        mapa = create_map(cliente.geolocalizacion_direccion)
        html_filename = f"{cliente.meta.id}_{cliente.nombre_completo}_{cliente.numero_celular}.html"
        html_filepath = os.path.join(mapas_directory, html_filename)
        mapa.save(html_filepath)
        logging.info(f"Se ha generado el mapa con la ubicacion del cliente. El archivo se guardo como '{html_filename}'.")

    logging.info("Registro finalizado.")

if __name__ == "__main__":
    main()