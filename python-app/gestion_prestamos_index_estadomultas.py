from elasticsearch_dsl import Document, Text, Float
from elasticsearch_dsl.connections import connections
import logging

connections.create_connection(hosts=['elasticsearch:9200'])
logging.basicConfig(level=logging.INFO)


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


def main():
    estado_multas = EstadoMultas()
    estado_multas.meta.id = 1
    response = EstadoMultas.search().source(['multas']).execute()
    if response.hits.total.value == 0:
        respuesta = input("No existe un valor para 'multas'. ¿Desea ingresar un valor? (s/n): ")
        if respuesta.lower() == 's':
            nuevo_valor = float(input("Ingrese el valor de 'multas': "))
            estado_multas.multas = nuevo_valor
            logging.info("El valor de 'multas' se ha creado correctamente.")
        elif respuesta.lower() == 'n':
            logging.info("Saliendo del programa.")
            return
        else:
            logging.info("Opcion invalida. Saliendo del programa.")
            return
    else:
        valor_multas = response.hits[0].multas
        logging.info("Ya existe un valor para 'multas': %s", valor_multas)
        respuesta = input("¿Desea modificar el valor de 'multas'? (s/n): ")
        if respuesta.lower() == 's':
            nuevo_valor = float(input("Ingrese el nuevo valor de 'multas': "))
            estado_multas.update(id=1, multas=nuevo_valor)
            logging.info("El valor de 'multas' se ha modificado correctamente.")
        elif respuesta.lower() == 'n':
            logging.info("Saliendo del programa.")
            return
        else:
            logging.info("Opcion invalida. Saliendo del programa.")
            return
    estado_multas.estado = ['Devuelto', 'En curso', 'En Mora', 'Perdido']
    estado_multas.save()
    logging.info("Se han agregado los elementos al campo 'estado' del indice 'index-estadomultas'.")


if __name__ == '__main__':
    main()
