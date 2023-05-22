from elasticsearch_dsl import Document, Integer, connections, Float
import logging

logging.basicConfig(level=logging.INFO)
connections.create_connection(hosts=['elasticsearch:9200'])

class Costo(Document):
    dias = Integer(multi=True)
    costos = Float(multi=True)

    class Index:
        name = 'index-costos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Costo.init()

class Descuento(Document):
    cantidades = Integer(multi=True)
    porcentajes = Float(multi=True)

    class Index:
        name = 'index-descuentos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

Descuento.init()

def validate_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                logging.info("Debes introducir un numero entero no negativo. Intenta de nuevo.")
        except ValueError:
            logging.info("Debes introducir un numero entero. Intenta de nuevo.")

def validate_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            logging.info("Debes introducir un numero decimal. Intenta de nuevo.")

def create_cost():
    num_dias = validate_integer("Introduce el numero de dias: ")
    dias = list(range(1, num_dias + 1))
    costos = []
    for dia in dias:
        costo = validate_float(f"Introduce el costo para el dia {dia}: ")
        costos.append(costo)
    documento = {
        "dias": dias,
        "costos": costos
    }
    costo_doc = Costo(**documento)
    costo_doc.save()
    logging.info("Costos creados exitosamente.")
    return

def create_discount():
    num_cantidades = validate_integer("Introduce la cantidad de opciones (cantidad de posibles opciones de descuento relacionadas a la cantidad de unidades rentadas) de descuento: ")
    cantidades = []
    porcentajes = []
    for i in range(num_cantidades):
        cantidad = validate_integer(f"Introduce la cantidad necesaria de unidades/peliculas para proceder al descuento: {i+1}: ")
        porcentaje = validate_float(f"Introduce el porcentaje de descuento asociado a la cantidad de unidades/peliculas {cantidad}: ")
        cantidades.append(cantidad)
        porcentajes.append(porcentaje)
    documento = {
        "cantidades": cantidades,
        "porcentajes": porcentajes
    }
    descuento_doc = Descuento(**documento)
    descuento_doc.save()
    logging.info("Descuento creado exitosamente.")
    return

def modify_cost():
    costos = Costo.search().execute()
    if costos.hits.total.value == 0:
        logging.info("No existen lista de renta para modificar.")
        return
    if costos:
        num_elementos_actual = len(costos[0].dias)
    else:
        num_elementos_actual = 0
    if num_elementos_actual == 0:
        logging.info("El rango de renta esta vacio. No se pueden realizar modificaciones.")
        return ###No es realemnte necesario hacer la validacion de si existe o no la lista o si la lista tiene o no elementos en ella (posible caos modificable dentro de main)
    logging.info(f"Rango actual de renta: {num_elementos_actual} dias")
    logging.info(f"Cantidad: {costos[0].dias}, precio: {costos[0].costos}")
    logging.info("")
    opcion = validate_integer("Seleccione una opcion:\n1. Modificar lista actual\n2. Modificar el rango de dias de renta\n3. Salir\nIntroduce el numero de la opcion deseada: ")
    if opcion == 1:
        for costo in costos:
            for i in range(len(costo.dias)):
                costo_nuevo = validate_float(f"Introduce el nuevo costo para el dia {costo.dias[i]}: ")
                costo.costos[i] = costo_nuevo
            costo.save()
        logging.info("Costos de renta para cada dia modificados exitosamente.")      
    elif opcion == 2:
        num_elementos_nuevo = validate_integer("Introduce el nuevo rango de dias de renta: ")
        if num_elementos_nuevo < 1:
            logging.info("El nuevo rango de dias debe ser un número entero positivo mayor o igual a 1.")
            return
        nuevos_dias = list(range(1, num_elementos_nuevo + 1))
        nuevos_costos = []
        for i in range(num_elementos_nuevo):
            nuevo_valor = validate_float(f"Introduce el nuevo valor para el día {i+1}: ")
            nuevos_costos.append(nuevo_valor)
        for costo in costos:
            costo.dias = nuevos_dias
            costo.costos = nuevos_costos
            costo.save()
        logging.info(f"El rango total de dias de renta ha sido modificada a: {num_elementos_nuevo}.")
    elif opcion == 3:
        logging.info("Saliendo del programa.")
        return
    else:
        logging.info("Opción inválida. Saliendo del programa.")


def modify_discount():
    descuentos = Descuento.search().execute()
    if descuentos.hits.total.value == 0:
        logging.info("No existe un descuento para modificar.")
        return
    if descuentos:
        num_elementos_actual = len(descuentos[0].cantidades)
    else:
        num_elementos_actual = 0

    if num_elementos_actual == 0:
        logging.info("La lista 'unidades/peliculas descuento asociado' está vacía. No se pueden realizar modificaciones.")
        return ###No es realemnte necesario hacer la validacion de si existe o no la lista o si la lista tiene o no elementos en ella (posible caso modificable dentro de main)
    logging.info(f"Cantidad actual de opciones de descuento: {num_elementos_actual}")
    logging.info(f"Cantidad de unidades/peliculas: {descuentos[0].cantidades}, Porcentaje asociado: {descuentos[0].porcentajes}")
    logging.info("")
    opcion = validate_integer("Seleccione una opción:\n1. Modificar lista actual\n2. Modificar rango de unidades/peliculas para su descuento asociado\n3. Salir\nIntroduce el numero de la opcion deseada: ")
    if opcion == 1:
        for descuento in descuentos:
            for i in range(len(descuento.cantidades)):
                cantidad_modificar = descuento.cantidades[i]-1
                porcentaje_modificar = validate_float(f"Introduce el nuevo porcentaje de descuento para las unidades/peliculas {cantidad_modificar}: ")
                descuento.porcentajes[i] = porcentaje_modificar
            descuento.save()
        logging.info("Descuentos por unidades/peliculas modificados exitosamente!!!")          
    elif opcion == 2:
        num_elementos_nuevo = validate_integer("Introduce el nuevo rango de elementos para 'unidades/porcentaje descuento asociado': ")
        if num_elementos_nuevo < 1:
            logging.info("La nueva cantidad de elementos en 'unidades/porcentaje descuento asociado' debe ser un numero entero positivo mayor o igual a 1.")
            return
        nuevas_cantidades = []
        nuevos_porcentajes = []
        for i in range(num_elementos_nuevo):
            cantidad_modificar = validate_integer(f"Introduce el valor para la cantidad necesaria para el descuento en unidades/peliculas: ")
            porcentaje_modificar = validate_float(f"Introduce el porcentaje de descuento para la cantidad asociada {cantidad_modificar}: ")
            nuevas_cantidades.append(cantidad_modificar)
            nuevos_porcentajes.append(porcentaje_modificar)
        for descuento in descuentos:
            descuento.cantidades = nuevas_cantidades
            descuento.porcentajes = nuevos_porcentajes
            descuento.save()
        logging.info(f"Los rangos han sido modificados a {num_elementos_nuevo} posibles descuentos por cierta cantidad de unidades/peliculas rentadas.")
    elif opcion == 3:
        logging.info("Saliendo del programa.")
        return
    else:
        logging.info("Opcion invalida. Saliendo del programa.")

def main():
    costos_existen = Costo.search().execute().hits.total.value > 0
    descuentos_existen = Descuento.search().execute().hits.total.value > 0

    if costos_existen and descuentos_existen:
        while True:
            logging.info("Seleccione una opcion:")
            logging.info("1. Modificar lista de precios")
            logging.info("2. Modificar lista de descuentos")
            logging.info("3. Salir")
            opcion = validate_integer("Introduce el numero de la opcion deseada: ")

            if opcion == 1:
                modify_cost()
            elif opcion == 2:
                modify_discount()
            elif opcion == 3:
                logging.info("Saliendo del programa.")
                break
            else:
                logging.info("Opcion invalida. Intentalo de nuevo.")

    elif not costos_existen:
        salir = False
        logging.info("No existe una lista de precios. ¿desea crear una lista?.")
        while not salir:
            logging.info("Seleccione una opcion:")
            logging.info("1. Crear costos")
            logging.info("2. Salir")
            opcion = validate_integer("Introduce el numero de la opcion deseada: ")

            if opcion == 1:
                create_cost()
                salir = True
            elif opcion == 2:
                logging.info("Saliendo del programa.")
                break
            else:
                logging.info("Opcion invalida. Intentalo de nuevo.")

    elif not descuentos_existen:
        salir = False
        logging.info("No existe una lista de descuentos. ¿desea crear una lista?.")
        while not salir:
            logging.info("Seleccione una opcion:")
            logging.info("1. Crear descuento")
            logging.info("2. Salir")
            opcion = validate_integer("Introduce el numero de la opcion deseada: ")

            if opcion == 1:
                create_discount()
                salir = True
            elif opcion == 2:
                logging.info("Saliendo del programa.")
                break
            else:
                logging.info("Opcion invalida. Intentalo de nuevo.")
    else:
        return

if __name__ == "__main__":
    main()