from elasticsearch_dsl import Document, Date, Keyword, Text, connections, Search, GeoPoint
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

def validate_date(prompt):
    while True:
        date_string = input(prompt)
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            logging.info("Debes introducir una fecha en el formato AAAA-MM-DD. Intenta de nuevo.")

def validate_phone(prompt):
    while True:
        phone = input(prompt)
        if phone.isdigit() and len(phone) == 8:
            return phone
        else:
            logging.info("Debes introducir un número de celular válido (8 dígitos numéricos). Intenta de nuevo.")

def search_client(query):
    s = Search(index='index-clientes').query("multi_match", query=query, fields=['_id', 'nombre_completo', 'numero_celular'])
    response = s.execute()
    if response.hits:
        return response.hits[0]
    return None

def search_banned_client(cliente_id):
    s = Search(index='index-ban').query('term', cliente_id=cliente_id)
    response = s.execute()
    if response.hits:
        return response.hits[0]
    return None

def ban_client(cliente):
    cliente_ban = search_banned_client(cliente.meta.id)
    if cliente_ban:
        logging.info("El cliente ya está baneado.")
        desbanear = input("¿Desea desbanear al cliente? (s/n): ")
        if desbanear.lower() == "s":
            ClienteBan.get(id=cliente_ban.meta.id).delete()
            logging.info(f"Cliente '{cliente.nombre_completo}' desbaneado exitosamente.")
    else:
        banear = input(f"¿Desea banear al cliente {cliente.nombre_completo}? (s/n): ")
        if banear.lower() == "s":
            motivo = input("Introduce el motivo del baneo: ")
            fecha_baneo = datetime.now().date()
            cliente_ban = ClienteBan(nombre_cliente=cliente.nombre_completo, motivo=motivo, fecha_baneo=fecha_baneo, meta={'id': cliente.meta.id})
            cliente_ban.save()
            logging.info(f"Cliente '{cliente.nombre_completo}' baneado exitosamente.")
        else:
            logging.info(f"No se realizó el baneo del cliente '{cliente.nombre_completo}'.")

def get_all_clients():
    s = Search(index='index-clientes').source(['_id', 'nombre_completo', 'numero_celular'])
    response = s.execute()
    return response.hits

def main():
    clientes = get_all_clients()

    if not clientes:
        logging.info("No hay clientes registrados.")
        return

    logging.info("Clientes registrados:")
    for cliente in clientes:
        logging.info(f"_id: {cliente.meta.id}, Nombre completo: {cliente.nombre_completo}, Numero de celular: {cliente.numero_celular}")

    query = input("Introduce el término de búsqueda (id, nombre, celular): ")
    cliente = search_client(query)

    if cliente is None:
        logging.info(f"No se encontró ningún cliente con el criterio de búsqueda proporcionado '{query}'.")
        return

    ban_client(cliente)

if __name__ == "__main__":
    main()