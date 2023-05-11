import time
from elasticsearch import Elasticsearch


# Esperar a que Elasticsearch esté listo
time.sleep(30)

es = Elasticsearch(hosts=[{'host': 'elasticsearch', 'port': 9200}])

# Crear un índice de prueba
es.indices.create(index='test-index', ignore=400)

# Insertar un documento de prueba
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.'
}
res = es.index(index="test-index", id=1, body=doc)
print(res['result'])

# Recuperar el documento de prueba
res = es.get(index="test-index", id=1)
print(res['_source'])
