from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_requiredColaborador, login_requiredCliente

from config import config

app=Flask(__name__)

#Actualiza el proyecto al realizar modificaciones en el HTML en la carpeta templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Conexión a la base de datos medinate el conector de mysql y también se conecta a la base de datos en línea
def connectionBD():
    db = mysql.connector.connect(
        host="proyectocs50.mysql.database.azure.com",
        user="localhost",
        password="cjs-1234",
        database="proyectocs50"
    )
    return db

#Esta es una forma de almacenar la información del usuario en el servidor para luego ser utilizada en la aplicación
app.config["SESSION_PERMANENT"] = False #Configura la sesion para que no sea permanente y se cierre cuando se cierre el navegador
app.config["SESSION_TYPE"] = "filesystem" # Define el tipo de almacenamiento para las sesiones, utilizando el almacenamiento en el sistema de archivos del servidor
Session(app)

@app.after_request
def after_request(response):
    """Asegura que las respuestas del servidor no se almacenen en caché del navegador"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


#ruta de inicio de la aplicación
@app.route('/')
def index():
    return render_template('home.html')


#inicio de sesión para los usuarios del sistema
@app.route('/login_colaborador', methods=['GET', 'POST'])
def login_colaborador():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        if not user or not password:
            error = "Debes completar todos los campos para continuar."
            return render_template('/auth/login_colaborador.html', error=error)

        # Verifica las creedenciales en la base de datos
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios_sistema WHERE usuario = %s', (user,))
        user_row = cursor.fetchone()
        cursor.close()

        if user_row and check_password_hash(user_row['contraseña'], password):
            # Si las credenciales son validas, el colaborador se loguea
            session['user_id'] = user_row['user_id']
            session['name'] = user_row['nombres']
            session['rol'] = user_row['rol']
            return redirect(url_for('dashboard_colaborador'))
        else:
            # Si las credenciales son invalidas, se envía un mensaje de error
            error = "Las credenciales ingresadas no son válidas. Por favor, inténtalo de nuevo."
            return render_template('/auth/login_colaborador.html', error=error)

    # Si entrea a la ruta del login_colaborador este renderiza la plantilla 
    return render_template('/auth/login_colaborador.html')


#inicio de sesión para los clientes    
@app.route('/login_usuario', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contraseña']

        if not email or not password:
            error = "Debes completar todos los campos para continuar."
            return render_template('/auth/login_usuario.html', error=error)

        # Verify credentials in the database
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (email,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row['contraseña'], password):
            # If credentials are valid, log in the user
            session['user_id'] = user_row['user_id']
            session['name'] = user_row['nombres']
            print("Inicio de sesión exitoso")
            return redirect(url_for('dashboard_colaborador'))
        else:
            # If credentials are invalid, show an error message
            error = "Las credenciales ingresadas no son válidas. Por favor, inténtalo de nuevo."
            print("Ocurrió un error chele")
            return render_template('/auth/login_usuario.html', error=error)
            cursor.close()
    # If accessing the login page for the first time or GET request, show the login form
    return render_template('/auth/login_usuario.html')


#ruta para el dashboard de los usuarios del sistema con restricción de acceso con inicio de sesión
@app.route('/dashboard_colaborador')
@login_requiredColaborador
def dashboard_colaborador():
    return render_template('dashboardcolaborador.html')


#Registro de usuarios para los clientes
@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == "POST":
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        cedula = request.form.get("cedula")
        correo = request.form.get("correo")
        contraseña = generate_password_hash(request.form.get("contraseña"))
        confirmacion = request.form.get("repetir")  
        telefono = request.form.get("telefono")

        # Validar campos en blanco
        if not nombres or not apellidos or not cedula or not correo or not contraseña or not confirmacion or not telefono:
            error = "Debes completar todos los campos para registrarte."
            return render_template('auth/registro_usuario.html', error=error)


        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
        user_row = cursor.fetchone()
        cursor.close()



        if request.form.get("contraseña") != confirmacion:  
            return apology("Passwords don't match", 403)

        db = connectionBD()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombres, apellidos, cedula, correo, contraseña, telefono) VALUES (%s, %s, %s, %s, %s, %s)", (nombres, apellidos, cedula, correo, contraseña, telefono))  # Corregido: añadir correo al INSERT
        db.commit()
        cursor.close()

        msg = "Registro exitoso!"
        return render_template('auth/login_usuario.html', msg=msg)  

    return render_template('auth/registro_usuario.html')


#Ruta para la reserva, con restricción de acceso con inicio de sesión de clientes
@app.route('/reserva')
@login_requiredCliente
def reserva():
    return render_template('reserva.html')


#Ruta de la landing page sin los botones de inicio de sesión, una vez que el usuario se ha logueado
@app.route('/home_user')
@login_requiredCliente
def home_user():
    return render_template('home_user.html')

# Proceso de cierre de sesión
@app.route('/Cerrar_Sesion')
def CerrarSesion():
    # Clear session variables
    session.pop('user_id', None)
    session.pop('name', None)
    print("Sesión cerrada exitosamente")
    return redirect(url_for('index'))


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()