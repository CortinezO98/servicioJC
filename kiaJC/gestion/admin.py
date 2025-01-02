from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *
from datetime import datetime, timedelta


class PasajeroResource(resources.ModelResource):
    class Meta:
        model = Pasajero


class EncomiendaResource(resources.ModelResource):
    class Meta:
        model = Encomienda


class TomorrowFilter(admin.SimpleListFilter):
    """Filtro personalizado para filtrar datos por la fecha del día siguiente."""
    title = _('Fecha del día siguiente')
    parameter_name = 'fecha_dia_siguiente'

    def lookups(self, request, model_admin):
        """Define las opciones del filtro."""
        return [
            ('true', _('Datos del día siguiente')),
        ]

    def queryset(self, request, queryset):
        """Aplica el filtro según la selección."""
        if self.value() == 'true':
            tomorrow = datetime.now().date() + timedelta(days=1)
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje=tomorrow)
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio=tomorrow)
        return queryset


class DateRangeFilter(admin.SimpleListFilter):
    """Filtro personalizado para filtrar datos dentro de un rango de fechas."""
    title = _('Rango de fechas')
    parameter_name = 'rango_fechas'

    def lookups(self, request, model_admin):
        """Define las opciones del filtro para seleccionar un rango de fechas."""
        return [
            ('today', _('Hoy')),
            ('this_week', _('Esta semana')),
            ('this_month', _('Este mes')),
            ('last_week', _('Semana pasada')),
            ('last_month', _('Mes pasado')),
        ]

    def queryset(self, request, queryset):
        """Aplica el filtro de rango de fechas."""
        now = datetime.now()
        if self.value() == 'today':
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje=now.date())  
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio=now.date())  
        elif self.value() == 'this_week':
            start_of_week = now - timedelta(days=now.weekday())
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje__gte=start_of_week)  
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio__gte=start_of_week)  
        elif self.value() == 'this_month':
            start_of_month = now.replace(day=1)
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje__gte=start_of_month)  
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio__gte=start_of_month)  
        elif self.value() == 'last_week':
            start_of_last_week = now - timedelta(days=7 + now.weekday())
            end_of_last_week = now - timedelta(days=1 + now.weekday())
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje_gte=start_of_last_week, fecha_viaje_lte=end_of_last_week)  
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio_gte=start_of_last_week, fecha_envio_lte=end_of_last_week)  
        elif self.value() == 'last_month':
            start_of_last_month = now.replace(day=1) - timedelta(days=1)
            start_of_last_month = start_of_last_month.replace(day=1)
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje__gte=start_of_last_month)  
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio__gte=start_of_last_month)  
        return queryset


@admin.register(Pasajero)
class PasajeroAdmin(ImportExportModelAdmin):
    resource_class = PasajeroResource
    list_display = ('nombre_pasajero', 'origen', 'destino', 'direccion_origen', 'direccion_destino', 'fecha_viaje', 'telefono', 'ruta', 'hora_viaje', 'cantidad_pasajes', 'descripcion')
    list_filter = ('origen', 'destino', 'ruta', TomorrowFilter, DateRangeFilter)
    search_fields = ('nombre_pasajero', 'telefono', 'origen', 'destino', 'fecha_viaje')
    ordering = ('-fecha_viaje',)

    def get_queryset(self, request):
        """Aplica el filtro del día siguiente también al queryset general."""
        qs = super().get_queryset(request)
        if 'fecha_dia_siguiente' in request.GET and request.GET['fecha_dia_siguiente'] == 'true':
            tomorrow = datetime.now().date() + timedelta(days=1)
            return qs.filter(fecha_viaje=tomorrow)
        return qs


@admin.register(Encomienda)
class EncomiendaAdmin(ImportExportModelAdmin):
    resource_class = EncomiendaResource
    list_display = ('nombre_remitente', 'origen', 'destino', 'direccion_origen', 'direccion_destino', 'fecha_envio', 'telefono', 'descripcion')
    list_filter = ('origen', 'destino', TomorrowFilter, DateRangeFilter)
    search_fields = ('nombre_remitente', 'telefono', 'origen', 'destino', 'fecha_envio')
    ordering = ('-fecha_envio',)

    def get_queryset(self, request):
        """Aplica el filtro del día siguiente también al queryset general."""
        qs = super().get_queryset(request)
        if 'fecha_dia_siguiente' in request.GET and request.GET['fecha_dia_siguiente'] == 'true':
            tomorrow = datetime.now().date() + timedelta(days=1)
            return qs.filter(fecha_envio=tomorrow)
        return qs