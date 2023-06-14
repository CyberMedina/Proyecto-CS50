from functools import wraps
from flask import session, redirect, url_for
from functools import wraps
from flask import session, redirect, url_for


#Validación para el inicio de sesión de colaoborador
def login_requiredColaborador(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("/login_colaborador"))
        return f(*args, **kwargs)
    return decorated_function
# END: a1b2c3d4e5f6import os
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


#Validación para los iniciar sesión de los clientes
def login_requiredCliente(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login_usuario")
        return f(*args, **kwargs)
    return decorated_function



def login_requiredColaborador(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login_colaborador")
        return f(*args, **kwargs)
    return decorated_function



