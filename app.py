from flask import Flask, render_template, request, session, redirect
from config import SECRET_KEY
import sqlite3
import hashlib


app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'SECRET_KEY'  # Clave secreta para la sesión

def get_db_connection():
    conn = sqlite3.connect('gestor_contraseñas.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sitio TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = request.form['password']

        if not username or not password:
            return render_template('registro.html', error='El nombre de usuario y/o la contraseña no pueden estar vacíos.')

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            conn.close()
            return render_template('registro.html', error='El nombre de usuario ya está en uso. Por favor, elija otro.')

        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()

        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        session['user_id'] = user['id']

        conn.close()

        return redirect('/menu')

    return render_template('registro.html')

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect('/menu')

        return render_template('inicio_sesion.html', error='Nombre de usuario o contraseña incorrectos.')

    return render_template('inicio_sesion.html')


@app.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        username = request.form['username']
        
        # Verificar si el usuario existe en la base de datos
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user:
            # implementar la lógica para enviar un correo electrónico con la contraseña al usuario
            # usar bibliotecas como Flask-Mail o servicios de correo electrónico como SendGrid
            
            # Por ahora, simplemente muestra un mensaje de éxito
            return render_template('recuperar_contraseña.html', success='Se ha enviado un correo electrónico con la contraseña.')
        
        return render_template('recuperar_contraseña.html', error='No se encontró ningún usuario con ese nombre de usuario.')

    return render_template('recuperar_contraseña.html')



@app.route('/menu')
def menu():
    if 'user_id' in session:
        conn = get_db_connection()
        user_id = session['user_id']
        passwords = conn.execute('SELECT * FROM passwords WHERE user_id = ?', (user_id,)).fetchall()
        conn.close()

        return render_template('mostrar_contraseñas.html', passwords=passwords)

    return redirect('/inicio_sesion')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html')


@app.route('/agregar_contraseña', methods=['GET', 'POST'])
def agregar_contraseña():
    if 'user_id' in session:
        if request.method == 'POST':
            sitio = request.form['sitio']
            username = request.form['username']
            password = request.form['password']

            if not sitio or not username or not password:
                return render_template('agregar_contraseña.html', error='Todos los campos son obligatorios y no pueden estar vacíos.')

            conn = get_db_connection()
            user_id = session['user_id']
            conn.execute('INSERT INTO passwords (user_id, sitio, username, password) VALUES (?, ?, ?, ?)',
                        (user_id, sitio, username, password))
            conn.commit()
            conn.close()

            return redirect('/menu')

        return render_template('agregar_contraseña.html')

    return redirect('/inicio_sesion')


@app.route('/eliminar_contraseña/<int:password_id>', methods=['POST'])
def eliminar_contraseña_id(password_id):
    if 'user_id' in session:
        conn = get_db_connection()
        user_id = session['user_id']
        conn.execute('DELETE FROM passwords WHERE id = ? AND user_id = ?', (password_id, user_id))
        conn.commit()
        conn.close()

    return redirect('/menu')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('user_id', None)
    return redirect('/inicio_sesion')

@app.route('/eliminar_cuenta')
def eliminar_cuenta():
    if 'user_id' in session:
        return redirect('/confirmar_eliminacion')
    
    return redirect('/inicio_sesion')

@app.route('/del_cuenta')
def del_cuenta():
    if 'user_id' in session:
        conn = get_db_connection()
        user_id = session['user_id']
        
        # Eliminar las claves asociadas al usuario
        conn.execute('DELETE FROM passwords WHERE user_id = ?', (user_id,))
        
        # Eliminar el usuario
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        session.pop('user_id', None)
        return redirect('/registro')  # Redirige al formulario de registro después de eliminar la cuenta
    
    return redirect('/inicio_sesion')


@app.route('/confirmar_eliminacion', methods=['GET', 'POST'])
def confirmar_eliminacion():
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')
        
        if confirmation == 'eliminar':
            return redirect('/del_cuenta')
        
        return redirect('/profile')
    
    return render_template('confirmar_eliminacion.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 40

if __name__ == '__main__':
    app.run()