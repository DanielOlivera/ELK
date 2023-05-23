#Lib elasticsearch_dsl
from elasticsearch_dsl import connections
import logging

logging.basicConfig(level=logging.INFO)
es = connections.create_connection(hosts=['elasticsearch:9200'])

def get_my_indices():
    all_indices = es.indices.get_alias("*")
    my_indices = {name: info for name, info in all_indices.items() if name.startswith('index-rentas')}
    return my_indices

index = get_my_indices()

if not index:
    logging.info("No se encontraron índices.")
else:
    logging.info(f"Se encontraron los siguientes índices: {', '.join(index)}")

for index_name in index:
    if es.indices.exists(index_name):
        del_index = input(f"¿Deseas borrar el índice '{index_name}'? (s/n): ")
        if del_index.lower() == 's':
            logging.info(f"Borrando índice '{index_name}'.")
            es.indices.delete(index=index_name)
            logging.info(f"Índice '{index_name}' borrado.")
        else:
            logging.info(f"Índice '{index_name}' no se eliminó.")
