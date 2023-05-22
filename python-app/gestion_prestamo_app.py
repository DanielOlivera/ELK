from elasticsearch_dsl import Document, Date, Keyword, Text, connections, Search, Q, GeoPoint, Integer, Float
from datetime import datetime, timedelta
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

class Renta(Document):
    id_cliente = Integer()
    cliente = Text()
    fecha_prestamo = Date()
    fecha_devolucion = Date()
    importe_total = Text()
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

def get_rental_cost(num_dias):
    s = Search(index='index-costos')
    response = s.execute()
    if response.hits:
        costos = response.hits[0].costos
        if num_dias > len(costos):
            return None, len(costos)  # Devolvemos None y la longitud de costos
        dias = response.hits[0].dias
        if num_dias in dias:
            index = dias.index(num_dias)
            return costos[index], len(dias)  # Devolvemos el costo y la longitud de dias
    return None, 0  # Devolvemos None y 0 si no se encontro el costo o dias

def facturacion(cliente, peliculas_rentadas):
    # Obtener la cantidad de peliculas rentadas
    cantidad_peliculas = len(peliculas_rentadas)
    # Obtener el numero de dias de renta deseado
    while True:
        num_dias = int(input("Ingrese la cantidad de días de renta: "))
        costo, longitud_dias = get_rental_cost(num_dias)
        if costo is None:
            logging.info(f"No es posible rentar por más de {longitud_dias} días. Por favor, elija otro número de días.")
        else:
            break
    # Buscar descuento aplicable segun la cantidad de peliculas rentadas
    descuento = None
    descuentos = get_all_discounts()
    for i in range(len(descuentos['cantidades'])):
        if cantidad_peliculas >= int(descuentos['cantidades'][i]):
            descuento = int(descuentos['porcentajes'][i])
    # Si no se encontro un descuento aplicable, establecer descuento en 0
    if descuento is None:
        descuento = 0
    # Calcular el costo total aplicando el descuento
    costo_total = costo - (costo * (descuento / 100))
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    # Calcular la fecha de devolucion sumando num_dias a la fecha actual
    fecha_devolucion = (datetime.now() + timedelta(days=num_dias)).strftime("%Y-%m-%d")
    logging.info(f"El cliente '{cliente.nombre_completo}'-'{cliente.meta.id}' esta rentando las siguientes peliculas:")
    for pelicula_rentada in peliculas_rentadas:
        logging.info(f"Pelicula: {pelicula_rentada}")
    logging.info(f"Durante {num_dias} dias a partir de la fecha {fecha_actual}")
    logging.info(f"Fecha de devolucion: {fecha_devolucion}")
    logging.info(f"Costo total: {costo_total:.2f} con un descuento del {descuento}%")
    renta(cliente.nombre_completo, fecha_actual, fecha_devolucion, costo_total, peliculas_rentadas)
    guardar_en_historial(cliente, peliculas_rentadas)
    

def renta(cliente, fecha_prestamo, fecha_devolucion, importe_total, peliculas_prestadas):
    # Obtener el último ID del índice renta
    s = Search(index='index-rentas').sort({"_id": {"order": "desc"}})
    response = s.execute()
    if response.hits.total.value > 0:
        last_id = int(response.hits[0].meta.id)
    else:
        last_id = -1
    next_id = last_id + 1
    s_cliente = Search(index='index-clientes').query("match", nombre_completo=cliente)
    response_cliente = s_cliente.execute()
    if response_cliente.hits.total.value > 0:
        id_cliente = response_cliente.hits[0].meta.id
    # Generar el nuevo documento para el índice renta
    status_actual = "En curso"
    multa = 0
    doc = {
        "_id": next_id,
        "id_cliente": id_cliente,
        "cliente": cliente,
        "fecha_prestamo": fecha_prestamo,
        "fecha_devolucion": fecha_devolucion,
        "importe_total": importe_total,
        "peliculas_prestadas": peliculas_prestadas,
        "status":  status_actual, # Establecer el valor del campo "status" como "En Curso"
        "multa" : multa #Como status siempre va a ser En curso para las rentas recientes entonces multa=0
    }
    Renta(meta={'id': doc["_id"]}, **doc).save()
    logging.info("Registro guardado en el historial de renta correctamente.")
    return

def guardar_en_historial(cliente, peliculas_rentadas):
    cliente_nombre = cliente.nombre_completo
    id_cliente = cliente.meta.id

    # Generar el nuevo documento para el índice index-renta-historial
    doc = {
        "cliente_nombre": cliente_nombre,
        "id_cliente": id_cliente,
        "peliculas_prestadas": peliculas_rentadas
    }
    
    RentaHistorial(**doc).save()
    logging.info("Registro guardado en el historial de renta correctamente.")
    return

def main():
    clientes = get_all_clients()
    if not clientes:
        logging.info("No hay clientes registrados.")
        return
    logging.info("Clientes registrados:")
    for cliente in clientes:
        logging.info(f"_id: {cliente.meta.id}, Nombre completo: {cliente.nombre_completo}")
    query = input("Introduce el termino de búsqueda (id, nombre): ")
    cliente = search_client(query)
    if cliente is None:
        logging.info(f"No se encontro ningun cliente con el criterio de busqueda proporcionado '{query}'.")
        return
    if check_cliente_baneado(cliente):
        logging.info(f"El cliente '{cliente.nombre_completo}'-'{cliente.meta.id}' esta baneado. No se pueden realizar mas operaciones.")
        return
    else:
        logging.info(f"El cliente '{cliente.nombre_completo}'-'{cliente.meta.id}' puede continuar con la renta de peliculas.")
    logging.info(f"'{cliente.nombre_completo}'-'{cliente.meta.id}' qué peliculas desea rentar")
    peliculas_rentadas = []
    while True:
        opcion_busqueda = int(input("Selecciona una opción de busqueda:\n1. Titulo\n2. Genero\n3. Actores\n4. Nominaciones al Oscar\n5. Proceder con la renta\n6. Cancelar\nOpcion: "))
        if opcion_busqueda == 1:
            titles = get_all_titles()
            logging.info("Titulos de peliculas disponibles:")
            for i, titulo in enumerate(titles):
                if titulo in peliculas_rentadas:
                    continue
                logging.info(f"{i+1}. Título: {titulo}")   
            if len(peliculas_rentadas) == len(titles):
                logging.info("Ya no hay mas peliculas disponibles en esta categoria.")
                continue
            opcion_pelicula = int(input("Selecciona una pelicula para rentar: "))
            if opcion_pelicula < 1 or opcion_pelicula > len(titles):
                logging.info("Opcion invalida. Intentalo de nuevo.")
                continue
            pelicula_elegida = titles[opcion_pelicula - 1]
            if pelicula_elegida in peliculas_rentadas:
                logging.info(f"La pelicula '{pelicula_elegida}' ya ha sido rentada previamente.")
                continue
            peliculas_rentadas.append(pelicula_elegida)
            logging.info(f"Se ha rentado la pelicula '{pelicula_elegida}' al cliente '{cliente.meta.id}'.")
        elif opcion_busqueda == 2:
            genres = get_all_genres()
            logging.info("Generos de peliculas disponibles:")
            for i, genero in enumerate(genres):
                if genero in peliculas_rentadas:
                    continue
                logging.info(f"{i+1}. Genero: {genero}") 
            if len(peliculas_rentadas) == len(titles):
                logging.info("Ya no hay mas peliculas disponibles en esta categoria.")
                continue
            opcion_genero = int(input("Selecciona un genero: "))
            if opcion_genero < 1 or opcion_genero > len(genres):
                logging.info("Opcion invalida. Intentalo de nuevo.")
                continue
            peliculas = search_movies_by_genre(genres[opcion_genero - 1])
            if not peliculas:
                logging.info(f"No se encontraron peliculas con el genero '{genres[opcion_genero - 1]}'.")
                continue
            logging.info("Peliculas encontradas:")
            for i, pelicula in enumerate(peliculas):
                if pelicula.titulo in peliculas_rentadas:
                    continue
                logging.info(f"{i+1}. Titulo: {pelicula.titulo}")
            opcion_pelicula = int(input("Selecciona una pelicula para rentar: "))
            if opcion_pelicula < 1 or opcion_pelicula > len(peliculas):
                logging.info("Opcion invalida. Intentalo de nuevo.")
                continue
            pelicula_elegida = peliculas[opcion_pelicula - 1]
            if pelicula_elegida.titulo in peliculas_rentadas:
                logging.info(f"La pelicula '{pelicula_elegida.titulo}' ya ha sido rentada previamente.")
                continue
            peliculas_rentadas.append(pelicula_elegida.titulo)
            logging.info(f"Se ha rentado la pelicula '{pelicula_elegida.titulo}' al cliente '{cliente.meta.id}'.")
        elif opcion_busqueda == 3:
            actors = get_all_actors()
            logging.info("Actores de peliculas disponibles:")
            for i, actor_title in enumerate(actors):
                if actor_title['titulo'] in peliculas_rentadas:
                    continue
                logging.info(f"{i+1}. Actor: {actor_title['actor']} - Titulo: {actor_title['titulo']}")
            if len(peliculas_rentadas) == len(titles):
                logging.info("Ya no hay mas peliculas disponibles en esta categoria.")
                continue
            opcion_actor = int(input("Selecciona una pelicula para rentar: "))
            if opcion_actor < 1 or opcion_actor > len(actors):
                logging.info("Opcion invalida. Intentalo de nuevo.")
                continue
            pelicula_elegida = actors[opcion_actor - 1]
            if pelicula_elegida['titulo'] in peliculas_rentadas:
                logging.info(f"La pelicula '{pelicula_elegida['titulo']}' ya ha sido rentada previamente.")
                continue
            peliculas_rentadas.append(pelicula_elegida['titulo'])
            logging.info(f"Se ha rentado la pelicula '{pelicula_elegida['titulo']}' al cliente '{cliente.meta.id}'.")
        elif opcion_busqueda == 4:
            movies = get_all_movies_ordered_by_nominations()
            logging.info("Peliculas ordenadas por numero de nominaciones al Oscar:")
            for i, pelicula in enumerate(movies):
                if pelicula.titulo in peliculas_rentadas:
                    continue
                logging.info(f"{i+1}. Titulo: {pelicula.titulo}, Nominaciones al Oscar: {pelicula.nominaciones_oscar}")
            if len(peliculas_rentadas) == len(titles):
                logging.info("Ya no hay mas peliculas disponibles en esta categoria.")
                continue
            opcion_pelicula = int(input("Selecciona una pelicula para rentar: "))
            if opcion_pelicula < 1 or opcion_pelicula > len(movies):
                logging.info("Opcion invalida. Intentalo de nuevo.")
                continue
            pelicula_elegida = movies[opcion_pelicula - 1]
            if pelicula_elegida.titulo in peliculas_rentadas:
                logging.info(f"La pelicula '{pelicula_elegida.titulo}' ya ha sido rentada previamente.")
                continue
            peliculas_rentadas.append(pelicula_elegida.titulo)
            logging.info(f"Se ha rentado la pelicula '{pelicula_elegida.titulo}' al cliente '{cliente.meta.id}'.")
        elif opcion_busqueda == 5:
            logging.info(f"El cliente '{cliente.nombre_completo}'-'{cliente.meta.id}' ha rentado las siguientes peliculas:")
            for pelicula_rentada in peliculas_rentadas:
                logging.info(f"Pelicula: {pelicula_rentada}")
            facturacion(cliente, peliculas_rentadas)
            logging.info("Saliendo del programa.")
            break
        elif opcion_busqueda == 6:
            return
        else:
            logging.info("Opcion invalida. Intentalo de nuevo.")

if __name__ == "__main__":
    main()

