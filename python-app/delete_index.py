from elasticsearch_dsl import connections, Index
import logging

# Configuramos logging
logging.basicConfig(level=logging.INFO)

# Crea una conexión al cluster de Elasticsearch
connections.create_connection(hosts=['elasticsearch:9200'])

# Define el índice
index_name = 'test-index-1'
index = Index(index_name)

# Verifica si el índice existe
if index.exists():
    logging.info(f"Borrando índice '{index_name}'.")
    index.delete()
    logging.info(f"Índice '{index_name}' borrado.")
else:
    logging.info(f"No hay nada que borrar, el índice '{index_name}' no existe.")

