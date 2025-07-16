from django.db import models
from django.core.exceptions import ValidationError
from datetime import time

class Cliente(models.Model):
    cedula = models.CharField(max_length=15, unique=True)
    nombre_completo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField()

    def __str__(self):
        return f"{self.cedula} - {self.nombre_completo}"


class Pasajero(models.Model):
    ORIGEN_CHOICES = [
        ('Barranquilla', 'Barranquilla'),
        ('Galeras', 'Galeras'),
        ('Since', 'Sincé'),
        ('Sincelejo', 'Sincelejo'),
        ('Betulia', 'Betulia'),
        ('Corozal', 'Corozal'),
        ('Ovejas', 'Ovejas'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES)
    destino = models.CharField(max_length=50)
    fecha_viaje = models.DateField()
    hora_viaje = models.TimeField()
    descripcion = models.TextField(blank=True)
    cantidad_pasajes = models.PositiveIntegerField(default=1)
    ruta = models.CharField(max_length=50)

    def clean(self):
        if Pasajero.objects.filter(
            cliente=self.cliente,
            fecha_viaje=self.fecha_viaje,
            ruta=self.ruta
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Ya has reservado un cupo para esta fecha y ruta.")

    def save(self, *args, **kwargs):
        self.clean()
        if self.origen == 'Barranquilla':
            self.ruta = 'Barranquilla a Galeras'
            self.hora_viaje = time(11, 0)
        elif self.origen in ['Galeras', 'Sincelejo', 'Since', 'Betulia', 'Corozal', 'Ovejas']:
            self.ruta = 'Galeras a Barranquilla'
            self.hora_viaje = time(3, 0)
        else:
            raise ValidationError("Origen no válido.")

        total_pasajes = Pasajero.objects.filter(
            fecha_viaje=self.fecha_viaje,
            hora_viaje=self.hora_viaje,
            ruta=self.ruta
        ).aggregate(models.Sum('cantidad_pasajes'))['cantidad_pasajes__sum'] or 0

        if total_pasajes + self.cantidad_pasajes > 16:
            raise ValidationError(f"No hay cupos disponibles para el viaje {self.ruta} en esta fecha.")

        super(Pasajero, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente.nombre_completo} ({self.ruta} - {self.fecha_viaje})"


class Encomienda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion_destino = models.CharField(max_length=255)
    origen = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)
    fecha_envio = models.DateField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Encomienda de {self.cliente.nombre_completo} ({self.origen} -> {self.destino})"
