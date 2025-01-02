from django.shortcuts import render, redirect
from gestion.models import *
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail

def index(request):
    return render(request,'index.html')


def pasajero(request):
    if request.method == 'POST':
        nombre_pasajero = request.POST['nombre_pasajero']
        direccion_origen = request.POST['direccion_origen']
        direccion_destino = request.POST['direccion_destino']
        telefono = request.POST['telefono']
        correo_electronico = request.POST['correo_electronico']
        origen = request.POST['origen']
        destino = request.POST.get('destino')
        fecha_viaje = request.POST['fecha_viaje']
        descripcion = request.POST.get('descripcion', '')
        cantidad_pasajes = int(request.POST.get('cantidad_pasajes', 1))

        try:
            Pasajero.objects.create(
                nombre_pasajero=nombre_pasajero,
                direccion_origen=direccion_origen,
                direccion_destino=direccion_destino,
                telefono=telefono,
                correo_electronico=correo_electronico,
                origen=origen,
                destino=destino,
                fecha_viaje=fecha_viaje,
                descripcion=descripcion,
                cantidad_pasajes=cantidad_pasajes
            )
            
            cuerpo_correo = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <h2 style="color: #0047AB; text-align: center;">Registro de Pasajero(s) Exitoso</h2>
                    <p style="color: #555;">Gracias por registrar tu cupo. Si necesitas cancelar el registro, comunícate directamente con la empresa (3106022149).</p>
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Nombre:</td>
                            <td style="padding: 8px; color: #555;">{nombre_pasajero}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Dirección de Origen:</td>
                            <td style="padding: 8px; color: #555;">{direccion_origen}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Dirección de Destino:</td>
                            <td style="padding: 8px; color: #555;">{direccion_destino}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Teléfono:</td>
                            <td style="padding: 8px; color: #555;">{telefono}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Correo electrónico:</td>
                            <td style="padding: 8px; color: #555;">{correo_electronico}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Origen:</td>
                            <td style="padding: 8px; color: #555;">{origen}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Destino:</td>
                            <td style="padding: 8px; color: #555;">{destino}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Fecha del viaje:</td>
                            <td style="padding: 8px; color: #555;">{fecha_viaje}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Descripción:</td>
                            <td style="padding: 8px; color: #555;">{descripcion}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Cantidad de pasajes:</td>
                            <td style="padding: 8px; color: #555;">{cantidad_pasajes}</td>
                        </tr>
                    </table>
                    <p style="text-align: center; color: #555;">Gracias por confiar en nosotros. ¡Buen viaje!</p>
                </div>
            """

            send_mail(
                f"Nuevo pasajero registrado: {nombre_pasajero}",
                'Este es un correo automático. Los detalles del pasajero están en el cuerpo del mensaje.',
                'serviciojc57@gmail.com',  
                ['jorgecortinez71@gmail.com',correo_electronico],  
                html_message=cuerpo_correo  
            )

            messages.success(request, 'Pasajero(s) registrado(s) con éxito.')
            return redirect('pasajeros.html')  
        except Exception as e:
            messages.error(request, f'Error al registrar pasajero: {str(e)}')
    
    return render (request, 'pasajeros.html')


def encomiendas(request):
    if request.method == 'POST':
        try:
            nombre_remitente = request.POST['nombre_remitente']
            direccion_origen = request.POST['direccion_origen']
            direccion_destino = request.POST['direccion_destino']
            telefono = request.POST['telefono']
            correo_electronico = request.POST['correo_electronico']
            origen = request.POST['origen']
            destino = request.POST['destino']
            fecha_envio = request.POST['fecha_envio']
            descripcion = request.POST.get('descripcion', '')

            Encomienda.objects.create(
                nombre_remitente=nombre_remitente,
                direccion_origen=direccion_origen,
                direccion_destino=direccion_destino,
                telefono=telefono,
                correo_electronico=correo_electronico,
                origen=origen,
                destino=destino,
                fecha_envio=fecha_envio,
                descripcion=descripcion
            )

            cuerpo_correo = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <h2 style="color: #0047AB; text-align: center;">Registro de Encomienda Exitoso</h2>
                    <p style="color: #555;">Gracias por registrar tu encomienda. Si necesitas cancelar el registro, comunícate directamente con la empresa (3106022149).</p>
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Nombre del remitente:</td>
                            <td style="padding: 8px; color: #555;">{nombre_remitente}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Dirección de Origen:</td>
                            <td style="padding: 8px; color: #555;">{direccion_origen}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Dirección de Destino:</td>
                            <td style="padding: 8px; color: #555;">{direccion_destino}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Teléfono:</td>
                            <td style="padding: 8px; color: #555;">{telefono}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Correo electrónico:</td>
                            <td style="padding: 8px; color: #555;">{correo_electronico}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Origen:</td>
                            <td style="padding: 8px; color: #555;">{origen}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Destino:</td>
                            <td style="padding: 8px; color: #555;">{destino}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Fecha de envío:</td>
                            <td style="padding: 8px; color: #555;">{fecha_envio}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #333;">Descripción:</td>
                            <td style="padding: 8px; color: #555;">{descripcion}</td>
                        </tr>
                    </table>
                    <p style="text-align: center; color: #555;">Gracias por confiar en nosotros. ¡Estamos aquí para ayudarte!</p>
                </div>
            """

            send_mail(
                f"Nueva encomienda registrada: {nombre_remitente}",
                'Este es un correo automático. Los detalles de la encomienda están en el cuerpo del mensaje.',
                'serviciojc57@gmail.com',  
                ['jorgecortinez71@gmail.com',correo_electronico],
                html_message=cuerpo_correo
            )
           

            messages.success(request, 'Encomienda registrada con éxito. ')
            return redirect('encomiendas.html')
        
        except Exception as e:
            messages.error(request, f'Error al registrar encomienda: {str(e)}')

    return render(request, 'encomiendas.html')


