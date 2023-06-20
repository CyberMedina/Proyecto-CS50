from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_requiredColaborador, login_requiredCliente, login_requiredCliente2, nologin_requiredCliente, check_reservas
from urllib.parse import urlencode #Dependencia utilizada para redirigir al modal de inicio de sesión
import urllib.parse #
from config import connectionBD


app=Flask(__name__)

#Actualiza el proyecto al realizar modificaciones en el HTML en la carpeta templates
app.config["TEMPLATES_AUTO_RELOAD"] = True



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
@nologin_requiredCliente
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
            session['usersis_id'] = user_row['usersis_id']
            session['name'] = user_row['nombres']
            session['id_rol'] = user_row['id_rol']
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
            return render_template('/home.html', error=error)

        # Verifica las credenciales en la base de datos
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (email,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row['contraseña'], password):
            # Si las credenciales son validas, el cliente se loguea
            session['user_id'] = user_row['user_id']
            session['cedula'] = user_row['cedula']
            session['nombres'] = user_row['nombres']
            session['apellidos'] = user_row['apellidos']
            session['correo'] = user_row['correo']
            session['telefono'] = user_row['telefono']
            print("Inicio de sesión exitoso")
            return redirect(url_for('home_user'))
        else:
            # Si las credenciales son invalidas, se envía un mensaje de error
            error = "Las credenciales ingresadas no son válidas. Por favor, inténtalo de nuevo."
            print("Ocurrió un error chele")
            return render_template('/home.html', error=error)
            cursor.close()
    # Si entrea a la ruta del login_usuario este renderiza la plantilla

    return render_template('/home.html')


#inicio de sesión para los clientes que lleva hacia reservas
@app.route('/login_usuario2', methods=['GET', 'POST'])
def login_usuario2():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contraseña']

        if not email or not password:
            error = "Debes completar todos los campos para continuar."
            return render_template('/home.html', error=error)

        # Verifica las credenciales en la base de datos
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (email,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row['contraseña'], password):
            # Si las credenciales son validas, el cliente se loguea
            session['user_id'] = user_row['user_id']
            session['cedula'] = user_row['cedula']
            session['nombres'] = user_row['nombres']
            session['apellidos'] = user_row['apellidos']
            session['correo'] = user_row['correo']
            session['telefono'] = user_row['telefono']
            print("Inicio de sesión exitoso")
            return redirect(url_for('reserva'))
        else:
            # Si las credenciales son invalidas, se envía un mensaje de error
            error = "Las credenciales ingresadas no son válidas. Por favor, inténtalo de nuevo."
            print("Ocurrió un error chele")
            return render_template('/home.html', error=error)
            cursor.close()
    # Si entrea a la ruta del login_usuario este renderiza la plantilla
    error2 = session.pop('error2', None)  # Obtiene el mensaje de error de la sesión y lo elimina
    return render_template('/home.html', error2=error2)


#ruta para el dashboard del colaborador
@app.route('/dashboard_colaborador')
@login_requiredColaborador
def dashboard_colaborador():
    return render_template('dashboardcolaborador.html')


# Ruta para el registro de usuario
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
        #cursor.close()



        if request.form.get("contraseña") != confirmacion:
            error = "Las contraseñas no son iguales."  
            return render_template('auth/registro_usuario.html', error=error)
        
        elif user_row:
            error = "El correo ya se encuentra registrado."
            return render_template('auth/registro_usuario.html', error=error)

        db = connectionBD()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombres, apellidos, cedula, correo, contraseña, telefono) VALUES (%s, %s, %s, %s, %s, %s)", (nombres, apellidos, cedula, correo, contraseña, telefono))  # Corregido: añadir correo al INSERT
        db.commit()
        cursor.close()

        modal_params = {'modal': 'true'}
        modal_url = "/login_usuario?" + urlencode(modal_params)
        return redirect(modal_url)
    return render_template('auth/registro_usuario.html')





@app.route('/reserva', methods=['GET', 'POST'])
@login_requiredCliente2
@check_reservas
def reserva():
    user_is_logged_in = True
    user_data = {
        'cedula': session.get('cedula'),
        'nombres': session.get('nombres'),
        'apellidos': session.get('apellidos'),
        'correo': session.get('correo'),
        'telefono': session.get('telefono')
    }

    if request.method == "POST":

        cantperson = request.form.get("cantperson")
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        estancia = 2.00
        estado = 0

        # Realizar la inserción en la base de datos utilizando los datos de la sesión
        db = connectionBD()
        cursor = db.cursor()
        cursor.execute("INSERT INTO reservas (user_id, cantperson, hora, estancia, fecha, estado) VALUES (%s, %s, %s, %s, %s, %s)", (session['user_id'], cantperson, hora, estancia, fecha, estado))
        db.commit()
        cursor.close()
        return redirect(url_for('finreserva'))

        


    return render_template('reserva.html', user_is_logged_in=user_is_logged_in, user_data=user_data)


#fin reserva
@app.route('/finreserva', methods=['GET', 'POST'])
@login_requiredCliente2
def finreserva():
    return render_template('finreserva.html', correo=session['correo'])

@app.route('/checkreserva', methods=['GET', 'POST'])
@login_requiredCliente2
def checkreserva():
    return render_template('checkreserva.html', correo=session['correo'], nombre=session['nombres'])

# Ruta que renderiza la plantilla de inicio, pero esta vez con el icono del usuario
@app.route('/home_user')
@login_requiredCliente
def home_user():
    return render_template('home_user.html')

@app.route('/editar_usuario')
@login_requiredCliente
def editar_usuario():
    return render_template('auth/editar_usuario.html')

# Ruta para cerrar sesión usuario
@app.route('/Cerrar_Sesion')
def CerrarSesion():
    # Clear session variables
    session.pop('user_id', None)
    session.pop('name', None)
    print("Sesión cerrada exitosamente")
    return redirect(url_for('index'))

# Ruta para cerrar sesión colaborador
@app.route('/Cerrar_Sesion_Colaborador')
def CerrarSesionColaborador():
    # Clear session variables
    session.pop('user_id', None)
    session.pop('name', None)
    print("Sesión cerrada exitosamente")
    return redirect(url_for('login_colaborador'))


if __name__=='__main__':
    app.run()