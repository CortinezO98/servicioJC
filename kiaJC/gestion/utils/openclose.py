# gestion/utils.py
from datetime import datetime, time, timedelta

def is_trip_open(ruta: str, fecha: datetime.date) -> bool:
    """
    Determina si la ventana de reserva sigue abierta:
    - Galeras→Barranquilla (viaje a 3:00am): corte 21:30 del día anterior.
    - Barranquilla→Galeras (viaje a 11:00am): corte 11:00 del mismo día.
    """
    ahora = datetime.now()
    if ruta == 'Galeras a Barranquilla':
        corte = datetime.combine(fecha - timedelta(days=1), time(21, 30))
    else:  # 'Barranquilla a Galeras'
        corte = datetime.combine(fecha, time(11, 0))
    return ahora <= corte
