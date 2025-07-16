from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from gestion.models import *
from datetime import datetime
from gestion.utils.openclose import is_trip_open

def index(request):
    return render(request, 'index.html')

def buscar_cliente(request):
    cedula = request.GET.get('cedula', '').strip()
    try:
        cliente = Cliente.objects.get(cedula=cedula)
        return JsonResponse({
            'exists': True,
            'nombre_completo': cliente.nombre_completo,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'correo_electronico': cliente.correo_electronico
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'exists': False})

def viaje_abierto(request):
    ruta = request.GET.get('ruta', '')
    fecha_str = request.GET.get('fecha', '')
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        abierto = is_trip_open(ruta, fecha)
    except Exception:
        abierto = False
    return JsonResponse({'open': abierto})

# Registro de pasajeros
def pasajero(request):
    if request.method == 'POST':
        # 1) recoger datos
        cedula           = request.POST.get('cedula', '').strip()
        nombre_pasajero  = request.POST.get('nombre_pasajero', '').strip()
        direccion_origen = request.POST.get('direccion_origen', '').strip()
        direccion_destino= request.POST.get('direccion_destino', '').strip()
        telefono         = request.POST.get('telefono', '').strip()
        correo_electronico = request.POST.get('correo_electronico', '').strip()
        origen           = request.POST.get('origen', '').strip()
        destino          = request.POST.get('destino', '').strip()
        fecha_viaje      = request.POST.get('fecha_viaje', '').strip()
        descripcion      = request.POST.get('descripcion', '').strip()
        cantidad_pasajes = int(request.POST.get('cantidad_pasajes', 1))

        # 2) validar ventana de reserva
        ruta = 'Barranquilla a Galeras' if origen == 'Barranquilla' else 'Galeras a Barranquilla'
        fecha_obj = datetime.strptime(fecha_viaje, '%Y-%m-%d').date()
        if not is_trip_open(ruta, fecha_obj):
            messages.error(request, f"Reservas cerradas para {ruta} el {fecha_viaje}.")
            return render(request, 'pasajeros.html')

        try:
            # 3) buscar o crear cliente
            cliente, creado = Cliente.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombre_completo': nombre_pasajero,
                    'direccion': direccion_origen,
                    'telefono': telefono,
                    'correo_electronico': correo_electronico
                }
            )
            if not creado:
                cliente.nombre_completo  = nombre_pasajero
                cliente.direccion         = direccion_origen
                cliente.telefono          = telefono
                cliente.correo_electronico= correo_electronico
                cliente.save()

            # 4) crear pasajero
            Pasajero.objects.create(
                cliente=cliente,
                origen=origen,
                destino=destino,
                fecha_viaje=fecha_viaje,
                descripcion=descripcion,
                cantidad_pasajes=cantidad_pasajes
            )

            # Enviar correo
            cuerpo_correo = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <h2 style="color: #0047AB; text-align: center;">Registro de Pasajero(s) Exitoso</h2>
                    <p style="color: #555;">Gracias por registrar tu cupo. Si necesitas cancelar el registro, comunícate directamente con la empresa (3106022149).</p>
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                        <tr><td style="padding: 8px; font-weight: bold;">Nombre:</td><td>{nombre_pasajero}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Dirección de Origen:</td><td>{direccion_origen}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Dirección de Destino:</td><td>{direccion_destino}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Teléfono:</td><td>{telefono}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Correo electrónico:</td><td>{correo_electronico}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Origen:</td><td>{origen}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Destino:</td><td>{destino}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Fecha del viaje:</td><td>{fecha_viaje}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Descripción:</td><td>{descripcion}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Cantidad de pasajes:</td><td>{cantidad_pasajes}</td></tr>
                    </table>
                    <p style="text-align: center;">Gracias por confiar en nosotros. ¡Buen viaje!</p>
                </div>
            """

            send_mail(
                f"Nuevo pasajero registrado: {nombre_pasajero}",
                'Este es un correo automático. Los detalles del pasajero están en el cuerpo del mensaje.',
                'serviciojc57@gmail.com',
                ['jorgecortinez71@gmail.com', correo_electronico],
                html_message=cuerpo_correo
            )

            messages.success(request, 'Pasajero(s) registrado(s) con éxito.')
            return redirect('pasajeros.html')
        except Exception as e:
            messages.error(request, f'Error al registrar pasajero: {str(e)}')

    return render(request, 'pasajeros.html')

# Registro de encomiendas
def encomiendas(request):
    if request.method == 'POST':
        cedula           = request.POST.get('cedula', '').strip()
        nombre_remitente = request.POST.get('nombre_remitente', '').strip()
        direccion_origen = request.POST.get('direccion_origen', '').strip()
        direccion_destino= request.POST.get('direccion_destino', '').strip()
        telefono         = request.POST.get('telefono', '').strip()
        correo_electronico = request.POST.get('correo_electronico', '').strip()
        origen           = request.POST.get('origen', '').strip()
        destino          = request.POST.get('destino', '').strip()
        fecha_envio      = request.POST.get('fecha_envio', '').strip()
        descripcion      = request.POST.get('descripcion', '').strip()

        # (opcional) validar ventana de reserva aquí

        try:
            cliente, creado = Cliente.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombre_completo': nombre_remitente,
                    'direccion': direccion_origen,
                    'telefono': telefono,
                    'correo_electronico': correo_electronico
                }
            )
            if not creado:
                cliente.nombre_completo  = nombre_remitente
                cliente.direccion         = direccion_origen
                cliente.telefono          = telefono
                cliente.correo_electronico= correo_electronico
                cliente.save()

            Encomienda.objects.create(
                cliente=cliente,
                origen=origen,
                destino=destino,
                fecha_envio=fecha_envio,
                descripcion=descripcion
            )

            # Enviar correo
            cuerpo_correo = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <h2 style="color: #0047AB; text-align: center;">Registro de Encomienda Exitoso</h2>
                    <p style="color: #555;">Gracias por registrar tu encomienda. Si necesitas cancelar el registro, comunícate directamente con la empresa (3106022149).</p>
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                        <tr><td style="padding: 8px; font-weight: bold;">Nombre del remitente:</td><td>{nombre_remitente}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Dirección de Origen:</td><td>{direccion_origen}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Dirección de Destino:</td><td>{direccion_destino}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Teléfono:</td><td>{telefono}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Correo electrónico:</td><td>{correo_electronico}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Origen:</td><td>{origen}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Destino:</td><td>{destino}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Fecha de envío:</td><td>{fecha_envio}</td></tr>
                        <tr><td style="padding: 8px; font-weight: bold;">Descripción:</td><td>{descripcion}</td></tr>
                    </table>
                    <p style="text-align: center;">Gracias por confiar en nosotros. ¡Estamos aquí para ayudarte!</p>
                </div>
            """

            send_mail(
                f"Nueva encomienda registrada: {nombre_remitente}",
                'Este es un correo automático. Los detalles de la encomienda están en el cuerpo del mensaje.',
                'serviciojc57@gmail.com',
                ['jorgecortinez71@gmail.com', correo_electronico],
                html_message=cuerpo_correo
            )

            messages.success(request, 'Encomienda registrada con éxito.')
            return redirect('encomiendas.html')
        except Exception as e:
            messages.error(request, f'Error al registrar encomienda: {str(e)}')

    return render(request, 'encomiendas.html')
