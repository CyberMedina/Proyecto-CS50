from flask import Flask, render_template

from config import config

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login_colaborador')
def login_colaborador():
    return render_template('auth/login_Colaborador.html')

@app.route('/login_usuario')
def login_usuario():
    return render_template('auth/login_usuario.html')

    
if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()