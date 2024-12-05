from flask import Flask, jsonify,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import time
import threading

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
            elif user[4] == 'estudiante':  # Suponiendo que 'rol' esté en la columna 
                global asistencia_activa
                if asistencia_activa:
                    usuario_id = user[0]
                    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    cursor = mysql.connection.cursor()
                    # Verifica si el usuario ya tiene asistencia registrada en la sesión actual
                    cursor.execute('SELECT * FROM asistencia WHERE usuario_id = %s AND DATE(fecha) = CURDATE()', (usuario_id,))
                    asistencia = cursor.fetchone()

                    if not asistencia:
                    # Inserta una nueva entrada de asistencia
                        cursor.execute('INSERT INTO asistencia (usuario_id, fecha, presente) VALUES (%s, %s, %s)',
                           (usuario_id, fecha_actual, 1))
                        mysql.connection.commit()

                    cursor.close()
                return redirect(url_for('student_dashboard'))  # Redirige al panel del estudiante
            elif user[4] == 'profesor':
                return redirect(url_for('p_dashboard'))
    
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

@app.route('/p_dashboard')
def p_dashboard():
    # Verifica si el estudiante está logueado
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirige al login si no está logueado

    username = session['username']
    
    # Aquí puedes agregar más lógica para cargar información relevante para el estudiante
    return render_template('profesor_dashboard.html', username=username)

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

@app.route('/update_activity', methods=['POST'])
def update_activity():

    status = request.json.get('active')  # Recibimos el estado (activo o inactivo)
    username = session['username']  # Obtenemos el nombre de usuario del estudiante desde la sesión

    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE Usuarios SET activo = %s WHERE nombre = %s AND rol = "estudiante"', (status, username))
    mysql.connection.commit()
    cursor.close()

    return {'message': 'Estado actualizado correctamente'}, 200


@app.route('/get_activity_status', methods=['GET'])
def get_activity_status():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT nombre, activo FROM Usuarios WHERE rol = "estudiante"')
    students = cursor.fetchall()  # Esto devuelve una lista de tuplas (nombre, activo)
    cursor.close()
    
    # Devolver el estado de los estudiantes como JSON
    return {'students': students}, 200

    
@app.route('/asistencia_profesor', methods=['GET'])
def asistencia_profesor():
    profesor_id = request.args.get('profesor_id')
    cursor = mysql.connection.cursor()

    # Obtén todos los estudiantes y su estado de asistencia para hoy
    cursor.execute("""
        SELECT U.id, U.nombre, 
               CASE WHEN A.presente == 1 THEN 'Presente' ELSE 'Ausente' END AS estado
        FROM usuarios U
        LEFT JOIN asistencia A 
        ON U.id = A.usuario_id AND DATE(A.fecha) = CURDATE()
        WHERE U.rol = 'estudiante'
    """)
    estudiantes = cursor.fetchall()
    cursor.close()

    return jsonify(estudiantes), 200

asistencia_activa = False

@app.route('/iniciar_asistencia', methods=['POST'])
def iniciar_asistencia():
    global asistencia_activa
    if not asistencia_activa:
        data = request.json
        tiempo_minutos = int(data['tiempo'])  # Tiempo en minutos

        # Inicia la asistencia automática
        asistencia_activa = True
        detener_asistencia_automatica(tiempo_minutos)

        return jsonify({"message": f"Asistencia automática iniciada por {tiempo_minutos} minutos"}), 200
    else:
        return jsonify({"message": "La asistencia automática ya está activa"}), 400


def detener_asistencia_automatica(tiempo_minutos):
    def detener():
        global asistencia_activa
        time.sleep(tiempo_minutos * 60)  # Esperar el tiempo configurado
        asistencia_activa = False
        print("La asistencia automática ha finalizado automáticamente.")

    # Ejecuta en un hilo separado para no bloquear la aplicación
    hilo = threading.Thread(target=detener)
    hilo.start()
    
@app.route('/marcar_asistencia', methods=['POST'])
def marcar_asistencia():
    global asistencia_activa
    if asistencia_activa:
        data = request.json
        usuario_id = data['usuario_id']
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = mysql.connection.cursor()
        # Verifica si el usuario ya tiene asistencia registrada en la sesión actual
        cursor.execute('SELECT * FROM asistencia WHERE usuario_id = %s AND DATE(fecha) = CURDATE()', (usuario_id,))
        asistencia = cursor.fetchone()

        if not asistencia:
            # Inserta una nueva entrada de asistencia
            cursor.execute('INSERT INTO asistencia (usuario_id, fecha, presente) VALUES (%s, %s, %s)',
                           (usuario_id, fecha_actual, 1))
            mysql.connection.commit()

        cursor.close()
        return jsonify({"message": "Asistencia marcada con éxito"}), 200

    return jsonify({"message": "Asistencia automática no está activa"}), 400
    

if __name__ == "__main__":
    app.run(debug=True)
