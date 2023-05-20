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
            logging.info("Debes introducir la geolocalizacion en el formato 'lat,lon'. Intentalo de nuevo.")
                      
def create_map(geolocalizacion):
    geoloc = geolocalizacion.split(',')
    lat = float(geoloc[0])
    lon = float(geoloc[1])
    mapa = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon]).add_to(mapa)
    return mapa

def delete_html_file(cliente):
    html_filename = f"{cliente.meta.id}_{cliente.nombre_completo}_{cliente.numero_celular}.html"
    html_filepath = os.path.join(mapas_directory, html_filename)
    if os.path.exists(html_filepath):
        os.remove(html_filepath)

def save_html_file(cliente):
    geolocalizacion = cliente.geolocalizacion_direccion
    if geolocalizacion:
        mapa = create_map(geolocalizacion)
        html_filename = f"{cliente.meta.id}_{cliente.nombre_completo}_{cliente.numero_celular}.html"
        html_filepath = os.path.join(mapas_directory, html_filename)
        mapa.save(html_filepath)
        logging.info(f"Se ha generado el mapa con la ubicacion del cliente. El archivo se guardo como '{html_filename}'.")
    else:
        logging.info("El cliente no tiene una geolocalizacion definida.")

def search_client(query):
    s = Search(index='index-clientes').query("multi_match",query=query, fields = ['_id', 'nombre_completo', 'numero_celular'])
    response = s.execute()
    if response.hits:
        return response.hits[0]
    return None

def get_all_clients():
    s = Search(index='index-clientes').source(['_id', 'nombre_completo', 'numero_celular'])
    response = s.execute()
    return response.hits

def save_changes(cliente):
    cliente_obj = Cliente.get(id=cliente.meta.id)
    cliente_obj.nombre_completo = cliente.nombre_completo
    cliente_obj.numero_celular = cliente.numero_celular
    cliente_obj.correo_electronico = cliente.correo_electronico
    cliente_obj.fecha_nacimiento = cliente.fecha_nacimiento
    cliente_obj.direccion = cliente.direccion
    cliente_obj.geolocalizacion_direccion = cliente.geolocalizacion_direccion
    cliente_obj.save()
    logging.info(f"Cliente '{cliente_obj.nombre_completo}' actualizado correctamente.")

def main():

    clientes = get_all_clients()

    if not clientes:
        logging.info("No hay clientes registrados.")
        return

    logging.info("Clientes registrados:")
    for cliente in clientes:
        logging.info(f"_id: {cliente.meta.id}, Nombre completo: {cliente.nombre_completo}, Numero de celular: {cliente.numero_celular}")

    query = input("Introduce el termino de busqueda (id, nombre, celular): ")
    cliente = search_client(query)

    if clientes is None:
        logging.info(f"No se encontro ningun cliente con el criterio de busqueda proporcionado '{query}'.")
        return

    logging.info(f"Cliente encontrado:")
    logging.info(f"_id: {cliente.meta.id}")
    logging.info(f"Nombre completo: {cliente.nombre_completo}")
    logging.info(f"Numero de celular: {cliente.numero_celular}")
    logging.info(f"Correo electronico: {cliente.correo_electronico}")
    logging.info(f"Fecha de nacimiento: {cliente.fecha_nacimiento}")
    logging.info(f"Dirección: {cliente.direccion}")
    logging.info(f"Geolocalizacion de la direccion: {cliente.geolocalizacion_direccion}")
    
    geoloc_anterior = cliente.geolocalizacion_direccion
    cliente_anterior = cliente.nombre_completo
    numero_anterior = cliente.numero_celular
    nuevo_nombre = None
    nuevo_celular = None
    nueva_geoloc = None

    modificar_nombre = input("¿Deseas modificar el nombre completo? (s/n): ")
    if modificar_nombre.lower() == "s":
        nuevo_nombre = input("Introduce el nuevo nombre completo: ")
        cliente.nombre_completo = nuevo_nombre

    modificar_celular = input("¿Deseas modificar el numero de celular? (s/n): ")
    if modificar_celular.lower() == "s":
        nuevo_celular = validate_phone("Introduce el nuevo numero de celular: ")
        cliente.numero_celular = nuevo_celular

    modificar_correo = input("¿Deseas modificar el correo electronico? (s/n): ")
    if modificar_correo.lower() == "s":
        nuevo_correo = validate_email("Introduce el nuevo correo electronico: ")
        cliente.correo_electronico = nuevo_correo

    modificar_fecha_nac = input("¿Deseas modificar la fecha de nacimiento? (s/n): ")
    if modificar_fecha_nac.lower() == "s":
        nueva_fecha_nac = validate_date("Introduce la nueva fecha de nacimiento (formato: AAAA-MM-DD): ")
        cliente.fecha_nacimiento = nueva_fecha_nac

    modificar_direccion = input("¿Deseas modificar la direccion? (s/n): ")
    if modificar_direccion.lower() == "s":
        nueva_direccion = input("Introduce la nueva direccion: ")
        cliente.direccion = nueva_direccion

    modificar_geoloc = input("¿Deseas modificar la geolocalizacion de la direccion? (s/n): ")
    if modificar_geoloc.lower() == "s":
        nueva_geoloc = validate_geolocation("Introduce la nueva geolocalizacion de la direccion (latitud longitud): ")
        cliente.geolocalizacion_direccion = nueva_geoloc
        
        if not os.path.exists(os.path.join(mapas_directory, f"{cliente.meta.id}_{cliente_anterior}_{numero_anterior}.html")):
            crear_mapa = input("No se ha generado un mapa HTML para este cliente. ¿Deseas generar uno ahora? (s/n): ")
            if crear_mapa.lower() == "s":
                save_html_file(cliente)
        
        elif cliente.nombre_completo != nuevo_nombre or cliente.numero_celular != nuevo_celular or geoloc_anterior != nueva_geoloc:
            logging.info(f"Modificando mapa del cliente: {cliente.nombre_completo}")
            delete_html_file(cliente)  ###MOD delete_html_file, borra y crea el nuevo cliente.html, solo deberia borrar el cliente anterior a las modificaciones
            save_html_file(cliente)

    save_changes(cliente)

if __name__ == "__main__":
    main()