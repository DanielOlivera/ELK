import random
import datetime

dia_prestamo = random.randint(1, 31)
fecha_prestamo = datetime.date(2023, 5, dia_prestamo)

diferencia_dias = random.randint(1, 5)
fecha_devolucion = fecha_prestamo + datetime.timedelta(days=diferencia_dias)

if fecha_devolucion.month != fecha_prestamo.month:
    for dia in range(1, fecha_devolucion.day + 1):
        fecha_devolucion = datetime.date(2023, fecha_prestamo.month + 1, dia)

print("Fecha de préstamo:", fecha_prestamo)
print("Dias de renta:", diferencia_dias)
print("Fecha de devolución:", fecha_devolucion)
