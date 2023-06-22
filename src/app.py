from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from datetime import datetime
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_requiredColaborador, login_requiredCliente, login_requiredCliente2, nologin_requiredCliente, check_reservas
from urllib.parse import urlencode #Dependencia utilizada para redirigir al modal de inicio de sesión
import urllib.parse #
from config import connectionBD
from flask import Flask
from flask_mail import Mail, Message
from flask import Flask, g #Con esto podemos tener una variable global para poder ser usadas nuestros HTML con jinja 




app=Flask(__name__)

app.jinja_env.globals['g'] = g #Se instancia la variable global para ser usada en jinja

#No puuede ser cambiada esta función, ya que esta función es una palabra reservada
@app.before_request
def before_request():
    if 'usersis_id' in session:
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT us.usersis_id, us.nombres, us.apellidos, r.rolname FROM usuarios_sistema us JOIN rol r ON us.id_rol = r.id_rol WHERE us.usersis_id = %s', (session['usersis_id'],))
        user_row = cursor.fetchone()
        cursor.close()

        g.id_rol = session['usersis_id']
        g.nombres = user_row['nombres']
        g.apellidos = user_row['apellidos']
        g.rolname = user_row['rolname']


# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'elgustocj@gmail.com'
app.config['MAIL_PASSWORD'] = 'jeijrzfqlxwmsuhw'
app.config['MAIL_DEFAULT_SENDER'] = 'elgustocj@gmail.com'

mail = Mail(app)

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
    #Función para abrir un modal en especifico al recargar el html y con el id del modal
    modal_id = "iniciosesion2"  # ID del modal que deseas abrir
    modal_params = {"modal": "true", "modal_id": modal_id,}
    modal_url = url_for('login_usuario2') + '?' + urlencode(modal_params)
    
    return redirect(modal_url)


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
    error = None
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
            return render_template('auth/registro_usuario.html', error=error, nombres=nombres, apellidos=apellidos, cedula=cedula, correo=correo, telefono=telefono)


        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
        user_row = cursor.fetchone()

        if request.form.get("contraseña") != confirmacion:
            error = "Las contraseñas no son iguales."  
            return render_template('auth/registro_usuario.html', error=error, nombres=nombres, apellidos=apellidos, cedula=cedula, correo=correo, telefono=telefono)
        
        elif user_row:
            error = "El correo ya se encuentra registrado."
            return render_template('auth/registro_usuario.html', error=error, nombres=nombres, apellidos=apellidos, cedula=cedula, telefono=telefono)

        db = connectionBD()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombres, apellidos, cedula, correo, contraseña, telefono) VALUES (%s, %s, %s, %s, %s, %s)", (nombres, apellidos, cedula, correo, contraseña, telefono))
        db.commit()
        cursor.close()

        modal_params = {'modal': 'true'}
        modal_url = "/login_usuario?" + urlencode(modal_params)
        return redirect(modal_url)

    return render_template('auth/registro_usuario.html', error=error)






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


#Vistas y rutas de colaborador de las solicitudes pendiente
@app.route('/solicitudes_pendientes', methods=['GET', 'POST'])
@login_requiredColaborador
def solicitudes_pendientes():
    # Obtener las solicitudes pendientes de la base de datos
    db = connectionBD()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT u.user_id, u.nombres, u.apellidos, r.id_reservas, r.cantperson, TIME_FORMAT(r.hora, '%h:%i %p') AS hora, r.estancia, DATE_FORMAT(r.fecha, '%Y-%m-%d') AS fecha, r.estado, DATE_FORMAT(r.registroreserva, '%Y-%m-%d %h:%i %p') AS registroreserva FROM reservas r INNER JOIN usuarios u ON r.user_id = u.user_id WHERE r.estado = 0;")
    solicitudes = cursor.fetchall()
    cursor.close()

    if request.method == "POST":
        return redirect(url_for('gestionsolicitud'), solicitudes=solicitudes, g=g)



    

    return render_template('solicitudes_pendientes.html', solicitudes=solicitudes, g=g)

# Ruta parar el formulario de rechazo de la solicitud
@app.route('/rechazo_solicitud/<int:id_reservas>', methods=['GET', 'POST'])
def rechazo_solicitud(id_reservas):

    if request.method == "POST":
        motivo_rechazo = request.form.get('motivo_rechazo')
        
        if not motivo_rechazo:
            error_message = "Por favor, ingresa el motivo de rechazo."
            return render_template('rechazo_solicitud.html', user_row=user_row, error_message=error_message)
        
        # Obtener los datos del formulario
        usersis_id = session['usersis_id'] #User id del usuario actual
        fecharespuesta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        motivo_rechazo = request.form['motivo_rechazo']
        
        # Actualizar el estado y realizar la inserción en la base de datos
        db = connectionBD()
        cursor = db.cursor()
        cursor.execute("UPDATE reservas SET estado = 2 WHERE id_reservas = %s", (id_reservas,))
        cursor.execute("UPDATE reservas SET usersis_id = %s, fecharespuesta = %s, descripcion = %s WHERE id_reservas = %s", (usersis_id, fecharespuesta, motivo_rechazo, id_reservas))
        db.commit()

        #Haciendo consulta para obtener los datos que se enviaran al correo
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT u.nombres, u.apellidos, u.correo FROM reservas r INNER JOIN usuarios u ON r.user_id = u.user_id WHERE r.id_reservas = %s", (id_reservas,))
        user_row = cursor.fetchone()

        destinatario=user_row['correo']
        nombres=user_row['nombres']
        apellidos=user_row['apellidos']

        # Enviar correo electrónico con el motivo de rechazo
        enviar_correo_rechazo(destinatario, nombres, apellidos, motivo_rechazo)

        return redirect(url_for('solicitudes_pendientes'))
    

        

    db = connectionBD()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SET lc_time_names = 'es_ES'")
    cursor.execute("SELECT u.user_id, u.nombres, u.apellidos, u.cedula, u.correo, u.contraseña, u.telefono, r.id_reservas, r.cantperson, TIME_FORMAT(r.hora, '%h:%i %p') AS hora, r.estancia, DATE_FORMAT(r.fecha, '%W %d de %M de %Y') AS fecha, r.estado, DATE_FORMAT(r.registroreserva, '%Y-%m-%d %h:%i %p') AS registroreserva FROM reservas r INNER JOIN usuarios u ON r.user_id = u.user_id WHERE r.id_reservas = %s", (id_reservas,))
    user_row = cursor.fetchone()

    

    return render_template('rechazo_solicitud.html', user_row=user_row)

# Función para enviar correo de rechazo
def enviar_correo_rechazo(destinatario, nombres, apellidos, motivo_rechazo):
    asunto = 'Rechazo de solicitud de reserva en el restaurante El gusto CJ'
    cuerpo = f'Estimado/a {nombres} {apellidos} \n\nLamentamos informarte que tu solicitud de reserva en el restaurante ha sido rechazada debido a la siguiente razón:\n\n{motivo_rechazo}\n\nTe agradecemos por tu interés en nuestro restaurante y esperamos poder atenderte en otra ocasión.\n\nSaludos cordiales\nEl gusto CJ'
    enviar_correo(destinatario, asunto, cuerpo)

# Función genérica para enviar un correo
def enviar_correo(destinatario, asunto, cuerpo):
    mensaje = Message(asunto, recipients=[destinatario])
    mensaje.body = cuerpo
    mail.send(mensaje)

# Ruta parar el formulario de aceptación de la solicitud
@app.route('/aceptar_solicitud/<int:id_reservas>', methods=['GET', 'POST'])
def aceptar_solicitud(id_reservas):
     
    if request.method == "POST":
        return redirect(url_for('solicitudes_pendientes'))
    

        

    db = connectionBD()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SET lc_time_names = 'es_ES'")
    cursor.execute("SELECT u.user_id, u.nombres, u.apellidos, u.cedula, u.correo, u.contraseña, u.telefono, r.id_reservas, r.cantperson, TIME_FORMAT(r.hora, '%h:%i %p') AS hora, r.estancia, DATE_FORMAT(r.fecha, '%W %d de %M de %Y') AS fecha, r.estado, DATE_FORMAT(r.registroreserva, '%Y-%m-%d %h:%i %p') AS registroreserva FROM reservas r INNER JOIN usuarios u ON r.user_id = u.user_id WHERE r.id_reservas = %s", (id_reservas,))
    user_row = cursor.fetchone()
        




    return render_template('aceptar_solicitud.html', user_row=user_row)

#Solitudes aprobadas
@app.route('/solicitudes_aprobadas', methods=['GET', 'POST'])
def solicitudes_aprobadas():
    # Obtener las solicitudes pendientes de la base de datos
    db = connectionBD()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT u.user_id, u.nombres, u.apellidos, r.id_reservas, r.cantperson, TIME_FORMAT(r.hora, '%h:%i %p') AS hora, r.estancia, DATE_FORMAT(r.fecha, '%Y-%m-%d') AS fecha, r.estado, DATE_FORMAT(r.registroreserva, '%Y-%m-%d %h:%i %p') AS registroreserva FROM reservas r INNER JOIN usuarios u ON r.user_id = u.user_id WHERE r.estado = 1;")
    solicitudes = cursor.fetchall()
    cursor.close()


    return render_template('solicitudes_aprobadas.html', solicitudes=solicitudes)

#Solicitudes rechazadas
@app.route('/solicitudes_rechazadas', methods=['GET', 'POST'])
def solicitudes_rechazadas():
    db = connectionBD()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT u.user_id, u.nombres, u.apellidos, r.id_reservas, r.cantperson, TIME_FORMAT(r.hora, '%h:%i %p') AS hora, r.estancia, DATE_FORMAT(r.fecha, '%Y-%m-%d') AS fecha, r.estado, DATE_FORMAT(r.registroreserva, '%Y-%m-%d %h:%i %p') AS registroreserva FROM reservas r INNER JOIN usuarios u ON r.user_id = u.user_id WHERE r.estado = 2;")
    solicitudes = cursor.fetchall()
    cursor.close()


    return render_template('solicitudes_rechazadas.html', solicitudes=solicitudes)

if __name__=='__main__':
    app.debug = True
    app.run()
