from elasticsearch_dsl import Document, Date, Integer, connections, Float, Text, Search
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
connections.create_connection(hosts=['elasticsearch:9200'])

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

def calcular_status_multas(renta_seleccionada):
    cliente_id = renta_seleccionada.id_cliente
    cliente_nombre = renta_seleccionada.cliente
    # Mostrar todos los registros asociados al cliente en index-rentas
    logging.info(f"Registros de rentas para el cliente {cliente_nombre}:")
    s = Search(index='index-rentas').filter('term', id_cliente=cliente_id)
    response = s.execute()
    for hit in response.hits:
        logging.info(f"Registro ID: {hit.meta.id}, Pelicula/s rentadas {hit.peliculas_prestadas},Fecha de prestamo: {hit.fecha_prestamo}, Fecha de devolucion: {hit.fecha_devolucion}, Importe total: {hit.importe_total}")
    # Preguntar si se desea modificar el status y la multa
    modificar = input("¿Desea modificar el status y la multa? (S/N): ")
    if modificar.upper() != "S":
        return
    fecha_actual = datetime.now().date()
    fecha_devolucion = renta_seleccionada.fecha_devolucion
    dias_retraso = (fecha_actual - datetime.strptime(fecha_devolucion, '%Y-%m-%d').date()).days
    status = ""
    multa = 0
    if dias_retraso < 0:
        status = 'En Curso'
    elif dias_retraso <= 5:
        status = 'En Mora'
        multa = dias_retraso * 10  # Valor de la multa por dia//Añadir index-multa a gestion_prestamo_redntadescuento.py, asi la
                                   # Multa se setea por defecto.
    else:
        status = 'Perdida'
        multa = dias_retraso
        ####
        #Agregar funcionalidad, Restar una unidad al indice index-peliculas, y añadir el regsitro de la perdida a index'substract
        #Agregar funcionalidad, bannear automaticamente al cliente cuyo status en cualquiera de sus registros sea 'Perdida'
        ####
    # Actualizar los campos de status y multa en los registros de rentas
    peliculas_modificadas = []
    for hit in response.hits:
        renta_obj = Renta.get(id=hit.meta.id)
        renta_obj.status = status
        renta_obj.multa = multa
        renta_obj.save()
        peliculas_modificadas.append(renta_obj.peliculas_prestadas)
        logging.info(f"Registro actualizado - Cliente ID: {renta_obj.id_cliente}, Nombre: {renta_obj.cliente}, Pelicula/s: {renta_obj.peliculas_prestadas}, Status: {status}, Multa: {multa}, _id: {renta_obj.meta.id}")
    if peliculas_modificadas:
        logging.info("Registros actualizados correctamente.")
    else:
        logging.info("No se encontraron registros para modificar.")
    
    
def main():
    # Obtener todas las rentas del indice index-rentas
    s = Search(index='index-rentas')
    response = s.execute()
    rentas = [hit for hit in response]
    if not rentas:
        print("No se encontraron rentas en el indice index-rentas.")
        return
    # Mostrar la lista de clientes encontrados
    clientes = set()
    for renta in rentas:
        clientes.add((renta.id_cliente, renta.cliente))
    print("Clientes encontrados:")
    for cliente_id, cliente in clientes:
        print(f"ID: {cliente_id}, Cliente: {cliente}")
    # Solicitar la seleccion de un cliente
    seleccion = input("Seleccione un cliente por su ID: ")
    renta_seleccionada = None
    for renta in rentas:
        if renta.id_cliente == int(seleccion):
            renta_seleccionada = renta
            break
    if not renta_seleccionada:
        print("Cliente invalido. Por favor, seleccione un ID valido.")
        return
    # Cliente seleccionado
    print(f"Cliente seleccionado: ID: {renta_seleccionada.id_cliente}, Cliente: {renta_seleccionada.cliente}")
    # Calcular el estado y las multas de las rentas del cliente seleccionado
    calcular_status_multas(renta_seleccionada)

if __name__ == "__main__":
    main()
