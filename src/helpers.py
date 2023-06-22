from functools import wraps
from flask import session, redirect, url_for, session
from urllib.parse import urlencode #Dependencia utilizada para redirigir al modal de inicio de sesión
import urllib.parse 
from config import connectionBD

#Validación para el inicio de sesión de colaborador
def login_requiredColaborador(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("/login_colaborador"))
        return f(*args, **kwargs)
    return decorated_function


#Validación para los iniciar sesión de los clientes
def login_requiredCliente(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login_usuario")
        return f(*args, **kwargs)
    return decorated_function

#Ultra validación para el botón ubicado en home.html de reserva verifique si el usuario está logueado o no
#Redirigiendolo al modal de inicio de sesión


def login_requiredCliente2(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            modal_id = "iniciosesion2"  # ID del modal que deseas abrir
            modal_params = {"modal": "true", "modal_id": modal_id,}
            modal_url = url_for('login_usuario2') + '?' + urlencode(modal_params)
            session['error2'] = "Debes iniciar sesión para poder reservar"  # Almacena el mensaje de error en la sesión
            return redirect(modal_url)
        return f(*args, **kwargs)
    return decorated_function


#Validación para que los usuarios clientes que ya hayan iniciado sesión siempre los redirija al home_user
def nologin_requiredCliente(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id"):
            return redirect("/home_user")
        return f(*args, **kwargs)
    return decorated_function


def login_requiredColaborador(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usersis_id") is None:
            return redirect("/login_colaborador")
        return f(*args, **kwargs)
    return decorated_function

def check_reservas(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Realizar la consulta en la base de datos
        db = connectionBD()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) AS count_reservas FROM reservas WHERE user_id = %s AND estado = 0', (session['user_id'],))
        result = cursor.fetchone()
        cursor.close()

        # Verificar si el usuario tiene reservas con estado > 0
        if result['count_reservas'] > 0:
            # Si el usuario tiene reservas, redireccionar a una página de error o mostrar un mensaje de error
            return redirect('/checkreserva')
        return f(*args, **kwargs)
    return decorated_function






