let isActive = 1; // 1: activo, 0: inactivo
let timeout; // Para manejar el tiempo de inactividad

// Función para actualizar el estado en la base de datos
function updateUserStatus(status) {
    isActive = status;

    // Envía el estado al servidor usando fetch
    fetch('/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: isActive })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Estado actualizado:', data);
    })
    .catch(error => {
        console.error('Error al actualizar estado:', error);
    });
}

// Detectar si la pestaña está activa o no
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        updateUserStatus(1); // Activo
    } else {
        updateUserStatus(0); // Inactivo
    }
});

// Detectar actividad del usuario
function resetInactivityTimer() {
    updateUserStatus(1); // Activo
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        updateUserStatus(0); // Inactivo después de 5 minutos sin interacción
    }, 300000); // 300000ms = 5 minutos
}

// Escuchar eventos de interacción
window.addEventListener('mousemove', resetInactivityTimer);
window.addEventListener('keydown', resetInactivityTimer);

// Inicializar el temporizador de inactividad
resetInactivityTimer();
