from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host': 'elasticsearch', 'port': 9200}])

# Crear un índice de prueba
es.indices.create(index='test-index-1', ignore=400)

# Insertar un documento de prueba
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'test010': '123456'
}
res = es.index(index="test-index-1", id=1, body=doc)
print(res['result'])

# Recuperar el documento de prueba
res = es.get(index="test-index-1", id=1)
print(res['_source'])


