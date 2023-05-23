import logging
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['elasticsearch:9200'])

logging.basicConfig(level=logging.INFO)
renta_id = input("Ingrese el ID del prestamo: ")
s = Search(index="index-rentas")
s = s.query("match", _id=renta_id)
response = s.execute()

if response.success() and response.hits.total.value > 0:
    hit = response.hits[0]

    id_cliente = hit.id_cliente
    cliente = hit.cliente
    fecha_prestamo = hit.fecha_prestamo
    fecha_devolucion = hit.fecha_devolucion
    importe_total = hit.importe_total
    peliculas_prestadas = hit.peliculas_prestadas
    status = hit.status
    multa = hit.multa
    
    logging.info(f"ID del prestamo: {renta_id}")
    logging.info(f"ID del cliente: {id_cliente}")
    logging.info(f"Cliente: {cliente}")
    logging.info(f"Fecha de prestamo: {fecha_prestamo}")
    logging.info(f"Fecha de devolucion: {fecha_devolucion}")
    logging.info(f"Importe total: {importe_total}")
    logging.info(f"Multa: {multa}")
    logging.info(f"Peliculas prestadas: {peliculas_prestadas}")
    logging.info(f"Status: {status}")

else:
    logging.info(f"No se encontro el prestamo con ID: {renta_id}")
