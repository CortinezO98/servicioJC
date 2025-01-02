from django.core.mail import EmailMessage

def enviar_correo_con_archivo(asunto, mensaje, archivo_path):
    email = EmailMessage(asunto, mensaje, 'serviciojc57@gmail.com', ['jorgecortinez71@gmail.com'])
    email.attach_file(archivo_path)
    email.send()