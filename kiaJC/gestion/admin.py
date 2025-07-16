from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Cliente, Pasajero, Encomienda
from datetime import datetime, timedelta

# --- Resource para Import/Export de Cliente ---
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

# --- Registra Cliente ---
@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    list_display = ('cedula', 'nombre_completo', 'direccion', 'telefono', 'correo_electronico')
    search_fields = ('cedula', 'nombre_completo', 'telefono')
    ordering = ('nombre_completo',)

# --- Resources existentes ---
class PasajeroResource(resources.ModelResource):
    class Meta:
        model = Pasajero

class EncomiendaResource(resources.ModelResource):
    class Meta:
        model = Encomienda

# --- Filtros existentes ---
class TomorrowFilter(admin.SimpleListFilter):
    title = _('Fecha del día siguiente')
    parameter_name = 'fecha_dia_siguiente'
    def lookups(self, request, model_admin):
        return [('true', _('Datos del día siguiente'))]
    def queryset(self, request, queryset):
        if self.value() == 'true':
            tomorrow = datetime.now().date() + timedelta(days=1)
            if isinstance(queryset.model, Pasajero):
                return queryset.filter(fecha_viaje=tomorrow)
            elif isinstance(queryset.model, Encomienda):
                return queryset.filter(fecha_envio=tomorrow)
        return queryset

class DateRangeFilter(admin.SimpleListFilter):
    title = _('Rango de fechas')
    parameter_name = 'rango_fechas'
    def lookups(self, request, model_admin):
        return [
            ('today', _('Hoy')),
            ('this_week', _('Esta semana')),
            ('this_month', _('Este mes')),
            ('last_week', _('Semana pasada')),
            ('last_month', _('Mes pasado')),
        ]
    def queryset(self, request, queryset):
        now = datetime.now()
        if self.value() == 'today':
            return queryset.filter(
                fecha_viaje=now.date()
            ) if isinstance(queryset.model, Pasajero) else queryset.filter(
                fecha_envio=now.date()
            )
        elif self.value() == 'this_week':
            start = now - timedelta(days=now.weekday())
            return queryset.filter(
                fecha_viaje__gte=start
            ) if isinstance(queryset.model, Pasajero) else queryset.filter(
                fecha_envio__gte=start
            )
        elif self.value() == 'this_month':
            start = now.replace(day=1)
            return queryset.filter(
                fecha_viaje__gte=start
            ) if isinstance(queryset.model, Pasajero) else queryset.filter(
                fecha_envio__gte=start
            )
        elif self.value() == 'last_week':
            start = now - timedelta(days=7 + now.weekday())
            end = now - timedelta(days=1 + now.weekday())
            return queryset.filter(
                fecha_viaje__gte=start, fecha_viaje__lte=end
            ) if isinstance(queryset.model, Pasajero) else queryset.filter(
                fecha_envio__gte=start, fecha_envio__lte=end
            )
        elif self.value() == 'last_month':
            start = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
            return queryset.filter(
                fecha_viaje__gte=start
            ) if isinstance(queryset.model, Pasajero) else queryset.filter(
                fecha_envio__gte=start
            )
        return queryset

# --- Admin de Pasajero ---
@admin.register(Pasajero)
class PasajeroAdmin(ImportExportModelAdmin):
    resource_class = PasajeroResource
    list_display = (
        'get_nombre_cliente', 'origen', 'destino', 'get_direccion_cliente',
        'fecha_viaje', 'get_telefono_cliente', 'ruta', 'hora_viaje',
        'cantidad_pasajes', 'descripcion'
    )
    list_filter = ('origen', 'destino', 'ruta', TomorrowFilter, DateRangeFilter)
    search_fields = ('cliente__nombre_completo', 'cliente__telefono', 'origen', 'destino', 'fecha_viaje')
    ordering = ('-fecha_viaje',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('fecha_dia_siguiente') == 'true':
            return qs.filter(fecha_viaje=datetime.now().date() + timedelta(days=1))
        return qs

    def get_nombre_cliente(self, obj):
        return obj.cliente.nombre_completo
    get_nombre_cliente.short_description = 'Pasajero'

    def get_telefono_cliente(self, obj):
        return obj.cliente.telefono
    get_telefono_cliente.short_description = 'Teléfono'

    def get_direccion_cliente(self, obj):
        return obj.cliente.direccion
    get_direccion_cliente.short_description = 'Dirección'

# --- Admin de Encomienda ---
@admin.register(Encomienda)
class EncomiendaAdmin(ImportExportModelAdmin):
    resource_class = EncomiendaResource
    list_display = (
        'get_nombre_cliente', 'origen', 'destino', 'get_direccion_cliente',
        'fecha_envio', 'get_telefono_cliente', 'descripcion'
    )
    list_filter = ('origen', 'destino', TomorrowFilter, DateRangeFilter)
    search_fields = ('cliente__nombre_completo', 'cliente__telefono', 'origen', 'destino', 'fecha_envio')
    ordering = ('-fecha_envio',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('fecha_dia_siguiente') == 'true':
            return qs.filter(fecha_envio=datetime.now().date() + timedelta(days=1))
        return qs

    def get_nombre_cliente(self, obj):
        return obj.cliente.nombre_completo
    get_nombre_cliente.short_description = 'Remitente'

    def get_telefono_cliente(self, obj):
        return obj.cliente.telefono
    get_telefono_cliente.short_description = 'Teléfono'

    def get_direccion_cliente(self, obj):
        return obj.cliente.direccion
    get_direccion_cliente.short_description = 'Dirección'
