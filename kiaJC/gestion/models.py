from django.db import models
from datetime import time
 
class Pasajero(models.Model):
    ORIGEN_CHOICES = [
        ('Barranquilla', 'Barranquilla'),
        ('Galeras', 'Galeras'),
        ('Since', 'Since'),
        ('Sincelejo', 'Sincelejo'),
        ('Betulia', 'Betulia'),
        ('Corozal', 'Corozal'),
        ('Ovejas', 'Ovejas'),
    ]
    
    nombre_pasajero = models.CharField(max_length=100)
    direccion_origen = models.CharField(max_length=255)  
    direccion_destino = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField (max_length=100)
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES)
    destino = models.CharField(max_length=50)
    fecha_viaje = models.DateField()
    hora_viaje = models.TimeField()
    descripcion = models.TextField(blank=True)
    cantidad_pasajes = models.PositiveIntegerField(default=1)
    ruta = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        
        if self.origen == 'Barranquilla':
            self.ruta = 'Barranquilla a Galeras'
            self.hora_viaje = time(11, 0)  
        elif self.origen == 'Galeras' or self.origen in ['Sincelejo', 'Betulia', 'Corozal', 'Ovejas','Since']:
            self.ruta = 'Galeras a Barranquilla'
            self.hora_viaje = time(3, 0)  
        else:
            raise ValueError("Origen no válido.")

    
        total_pasajes = Pasajero.objects.filter(
            fecha_viaje=self.fecha_viaje,
            hora_viaje=self.hora_viaje,
            ruta=self.ruta
        ).aggregate(models.Sum('cantidad_pasajes'))['cantidad_pasajes__sum'] or 0

        if total_pasajes + self.cantidad_pasajes > 16:
            raise ValueError(f"No hay cupos disponibles para el viaje {self.ruta} para la fecha {self.fecha_viaje}. Contacte a la empresa para mas informacion(3106022149).")

        super(Pasajero, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_pasajero} ({self.origen} -> {self.destino}, {self.fecha_viaje} {self.hora_viaje})"
    
class Encomienda(models.Model):
    nombre_remitente = models.CharField(max_length=100)
    direccion_origen = models.CharField(max_length=255)  
    direccion_destino = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField (max_length=100)
    origen = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)
    fecha_envio = models.DateField()
    descripcion = models.TextField(blank=True)

 
    def __str__(self):
        return f"Encomienda de {self.nombre_remitente} ({self.origen} -> {self.destino})"
