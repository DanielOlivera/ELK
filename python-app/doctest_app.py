from elasticsearch_dsl import Document, Keyword
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

connections.create_connection(hosts=['elasticsearch:9200'])

class Test(Document):
    numero_celular = Keyword()
    correo_electronico = Keyword()

    class Index:
        name = 'index-doctest'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Test.init()
test = Test.init()

def main():

    test = Test(numero_celular='123456789', correo_electronico='test@example.com')
    test.save()

    s = Search(index='index-doctest')
    response = s.execute()

    for hit in response:
        print(hit.numero_celular, hit.correo_electronico)

if __name__ == "__main__":
    main()
