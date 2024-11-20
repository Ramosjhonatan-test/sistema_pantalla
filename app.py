from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SistemaEducativo'

mysql = MySQL(app)

# Configuración de la clave secreta para la sesión
app.secret_key = 'mi_clave_secreta'  # Asegúrate de cambiar esto en un entorno de producción

@app.route('/')
def index():
    return render_template('index.html', is_admin=False)  # Muestra el login por defecto

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE nombre = %s', (username,))
    user = cursor.fetchone()
    
    # Verifica si las credenciales son correctas
    if user:
        if check_password_hash(user[3], password):  # Verifica el hash de la contraseña
            # Guardamos el nombre de usuario en la sesión
            session['username'] = user[1]
            
            # Si el rol es 'profesor' o 'admin', redirige al formulario de registro de profesores
            if username == 'admin':  # Si el rol es 'profesor' o 'admin'
                return redirect(url_for('register_professor'))  # Redirige al formulario de registro del profesor
            
            # Si el rol es 'estudiante', redirige al panel del estudiante
            elif user[4] == 'estudiante':  # Suponiendo que 'rol' esté en la columna 4
                return redirect(url_for('student_dashboard'))  # Redirige al panel del estudiante
    
    return "Credenciales incorrectas", 401

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])  # Hashing de la contraseña

    # Aquí asignamos el rol como 'estudiante' por defecto
    role = 'estudiante'

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO Usuarios (nombre, correo, contraseña, rol) VALUES (%s, %s, %s, %s)', 
                   (username, email, password, role))
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for('index'))

@app.route('/register_professor', methods=['GET', 'POST'])
def register_professor():
    # Verificar que el usuario es administrador o profesor
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirige al login si no está logueado

    # Si el usuario es admin o profesor, permitimos el registro de un nuevo profesor
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # Hashing de la contraseña
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Usuarios (nombre, correo, contraseña, rol) VALUES (%s, %s, %s, %s)', 
                       (username, email, password, 'profesor'))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('index'))  # Después de registrar al profesor, redirige al inicio
    
    return render_template('register_professor.html')  # Cargar el formulario de registro de profesor

@app.route('/student_dashboard')
def student_dashboard():
    # Verifica si el estudiante está logueado
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirige al login si no está logueado

    username = session['username']
    
    # Aquí puedes agregar más lógica para cargar información relevante para el estudiante
    return render_template('student_dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Elimina el nombre de usuario de la sesión
    return redirect(url_for('index'))  # Redirige al login

if __name__ == "__main__":
    app.run(debug=True)
