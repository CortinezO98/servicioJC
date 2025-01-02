from celery import shared_task
from .utils.excel_utils import generar_excel_pasajeros, generar_excel_encomiendas
from .utils.email_utils import enviar_correo_con_archivo

@shared_task
def enviar_listas_programadas():
    archivo_pasajeros = generar_excel_pasajeros()
    archivo_encomiendas = generar_excel_encomiendas()

    destinatario = 'jorgecortinez71@gmail.com'
    asunto = 'Lista de pasajeros y encomiendas para el día siguiente'
    mensaje = 'Adjunto encontrarás la lista de pasajeros y encomiendas para mañana.'

    enviar_correo_con_archivo(destinatario, asunto, mensaje, archivo_pasajeros)
    enviar_correo_con_archivo(destinatario, asunto, mensaje, archivo_encomiendas)