from elasticsearch_dsl import Document, Integer, Date, Float, connections, Text
from collections import Counter

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

    def get_historial_peliculas_prestadas(self):
        peliculas_rentadas = []
        s = Renta.search().filter('term', id_cliente=self.id_cliente)
        response = s.execute()
        for hit in response.hits:
            peliculas_rentadas.extend(hit.peliculas_prestadas.split(", "))
        contador_peliculas = Counter(peliculas_rentadas)
        return contador_peliculas

    def fetch_cliente(self):
        s = Renta.search().filter('term', id_cliente=self.id_cliente).source(['cliente'])
        response = s.execute()
        self.cliente = response.hits[0].cliente

def main():
    id_cliente = input("Ingrese el ID del cliente: ")
    renta = Renta(id_cliente=id_cliente)
    renta.fetch_cliente()
    nombre_cliente = renta.cliente
    historial_peliculas = renta.get_historial_peliculas_prestadas()
    print(f"Historial de peliculas prestadas para el cliente {id_cliente}-{nombre_cliente}:")
    for pelicula, frecuencia in historial_peliculas.items():
        print(f"Pelicula: {pelicula} - Rentada {frecuencia} veces")

if __name__ == '__main__':
    main()
