from elasticsearch_dsl import Document, Keyword, Date, Float, connections
from collections import Counter

connections.create_connection(hosts=['elasticsearch:9200'])

class Renta(Document):
    id_cliente = Keyword()
    cliente = Keyword()
    fecha_prestamo = Date()
    fecha_devolucion = Date()
    importe_total = Float()
    peliculas_prestadas = Keyword()
    status = Keyword()
    multa = Float()

    class Index:
        name = 'index-rentas'

    @staticmethod
    def get_ranking_peliculas_rentadas():
        peliculas_rentadas = []
        s = Renta.search()
        response = s.execute()
        for hit in response.hits:
            peliculas_rentadas.extend(hit.peliculas_prestadas.split(", "))
        contador_peliculas = Counter(peliculas_rentadas)
        ranking = contador_peliculas.most_common(10)
        return ranking


def main():
    ranking_peliculas = Renta.get_ranking_peliculas_rentadas()
    print("Ranking de las 10 peliculas más rentadas:")
    for i, (pelicula, frecuencia) in enumerate(ranking_peliculas, start=1):
        print(f"{i}. Pelicula: {pelicula} - Rentada {frecuencia} veces")

if __name__ == '__main__':
    main()
