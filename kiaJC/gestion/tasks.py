from celery import shared_task
from datetime import datetime, timedelta
from .models import Pasajero, Encomienda
from .utils.excel_utils import generar_excel_pasajeros, generar_excel_encomiendas
from .utils.email_utils import enviar_correo_con_archivo

@shared_task
def enviar_reportes_por_viaje():
    hoy   = datetime.now().date()
    manana= hoy + timedelta(days=1)

    # IDA: Galeras→Barranquilla
    p_ida = Pasajero.objects.filter(fecha_viaje=manana, ruta='Galeras a Barranquilla')
    e_ida = Encomienda.objects.filter(fecha_envio=manana, cliente__direccion__in=[
        'Galeras','Since','Sincelejo','Corozal','Betulia','Ovejas'
    ])
    if p_ida.exists() or e_ida.exists():
        f_p = generar_excel_pasajeros(p_ida)
        f_e = generar_excel_encomiendas(e_ida)
        enviar_correo_con_archivo(
            'jorgecortinez71@gmail.com',
            f'IDa {manana} Galeras→Barranquilla',
            'Adjunto lista de pasajeros y encomiendas de ida.',
            f_p
        )
        enviar_correo_con_archivo(
            'jorgecortinez71@gmail.com',
            f'Encomiendas Ida {manana}',
            'Adjunto lista de encomiendas de ida.',
            f_e
        )

    # VUELTA: Barranquilla→Galeras
    p_v   = Pasajero.objects.filter(fecha_viaje=hoy, ruta='Barranquilla a Galeras')
    e_v   = Encomienda.objects.filter(fecha_envio=hoy, cliente__direccion='Barranquilla')
    if p_v.exists() or e_v.exists():
        f_p2 = generar_excel_pasajeros(p_v)
        f_e2 = generar_excel_encomiendas(e_v)
        enviar_correo_con_archivo(
            'jorgecortinez71@gmail.com',
            f'Vuelta {hoy} Barranquilla→Galeras',
            'Adjunto lista de pasajeros de vuelta.',
            f_p2
        )
        enviar_correo_con_archivo(
            'jorgecortinez71@gmail.com',
            f'Encomiendas Vta {hoy}',
            'Adjunto lista de encomiendas de vuelta.',
            f_e2
        )
