document.getElementById('registerForm').addEventListener('submit', function(e) {
    var password = document.getElementById('contraseña').value;
    var confirmPassword = document.getElementById('confirmar_contraseña').value;

    if (password !== confirmPassword) {
        e.preventDefault(); // Evita el envío del formulario
        alert('Las contraseñas no coinciden. Por favor, verifica e intenta de nuevo.');
    }
});
