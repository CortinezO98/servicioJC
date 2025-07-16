// static/js/buscar_cliente.js

document.addEventListener('DOMContentLoaded', () => {
  const cedInput = document.getElementById('cedula');
  cedInput.addEventListener('blur', buscarCliente);
});

function buscarCliente() {
  const ced = document.getElementById('cedula').value.trim();
  if (!ced) return;

  // usa la URL por nombre de Django y garantiza que incluye la / final
  const url = `{% url 'buscar_cliente' %}?cedula=${encodeURIComponent(ced)}`;

  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => {
      if (data.exists) {
        // asegúrate de que estos IDs existan en tu form
        document.getElementById('nombre_pasajero').value   = data.nombre_completo;
        document.getElementById('direccion_origen').value  = data.direccion;
        document.getElementById('telefono').value          = data.telefono;
        document.getElementById('correo_electronico').value= data.correo_electronico;
      } else {
        ['nombre_pasajero','direccion_origen','telefono','correo_electronico']
          .forEach(id => document.getElementById(id).value = '');
      }
    })
    .catch(err => console.error('Error buscando cliente:', err));
}
