import openpyxl
from django.utils.timezone import now, timedelta
from ..models import Pasajero, Encomienda

def generar_excel_pasajeros(ruta):
    fecha_manana = now().date() + timedelta(days=1)
    pasajeros = Pasajero.objects.filter(fecha_viaje=fecha_manana, ruta=ruta)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Pasajeros'
    ws.append(['Nombre', 'Teléfono', 'Dirección de Origen', 'Dirección de Destino', 'Origen', 'Destino', 'Ruta', 'Fecha de Viaje', 'Cantidad de Pasajeros', 'Descripción'])

    for pasajero in pasajeros:
        ws.append([
            pasajero.nombre_pasajero, pasajero.telefono, pasajero.direccion_origen,
            pasajero.direccion_destino, pasajero.origen, pasajero.destino,
            pasajero.ruta, pasajero.fecha_viaje, pasajero.cantidad_pasajes,
            pasajero.descripcion
        ])

    archivo_path = f'lista_pasajeros_{ruta}_{fecha_manana}.xlsx'
    wb.save(archivo_path)
    return archivo_path

def generar_excel_encomiendas(ruta):
    fecha_manana = now().date() + timedelta(days=1)
    encomiendas = Encomienda.objects.filter(fecha_envio=fecha_manana, ruta=ruta)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Encomiendas'
    ws.append(['Nombre Remitente', 'Dirección de Origen', 'Dirección de Destino', 'Teléfono', 'Correo Electrónico', 'Origen', 'Destino', 'Fecha de Envío', 'Descripción'])

    for encomienda in encomiendas:
        ws.append([
            encomienda.nombre_remitente, encomienda.direccion_origen, encomienda.direccion_destino,
            encomienda.telefono, encomienda.correo_electronico, encomienda.origen,
            encomienda.destino, encomienda.fecha_envio, encomienda.descripcion
        ])

    archivo_path = f'lista_encomiendas_{ruta}_{fecha_manana}.xlsx'
    wb.save(archivo_path)
    return archivo_path
