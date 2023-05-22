#Lib elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host': 'elasticsearch', 'port': 9200}])
es.indices.create(index='index-caratula', ignore=400)

doc = {
    'autor': 'Daniel Olivera',
    'text': 'MCDv4 - Elasticsearch',
    'test': 101
}

res = es.index(index="index-caratula", id=0, body=doc)
print(res['result'])

res = es.get(index="index-caratula", id=0)
print(res['_source'])

###no usar lib elasticsearch
