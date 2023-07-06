Bibliotecas utilizadas:
from flask import Flask, render_template, request, session, redirect: Importa las clases y funciones necesarias de Flask para crear la aplicación web.
from config import SECRET_KEY: Importa la variable SECRET_KEY desde el archivo config.py.
from favicon import get as get_favicon: Importa la función get del módulo favicon.
import sqlite3: Importa el módulo sqlite3 para interactuar con la base de datos SQLite.
import hashlib: Importa el módulo hashlib para realizar el hash de contraseñas.
from urllib.parse import urlparse: Importa la función urlparse del módulo urllib.parse para analizar y manipular URLs.
Configuración de la aplicación Flask:
app = Flask(__name__): Crea una instancia de la aplicación Flask.
app = Flask(__name__, static_url_path='/static'): Configura la ruta estática de la aplicación Flask.
app.secret_key = 'SECRET_KEY': Establece la clave secreta para la sesión de Flask. La clave secreta se obtiene desde el archivo config.py.
Funciones auxiliares:
def get_db_connection(): Establece una conexión con la base de datos SQLite y devuelve el objeto de conexión.
def create_tables(): Crea las tablas necesarias en la base de datos si no existen. Se definen las tablas users y passwords con sus respectivas columnas.
create_tables(): Se llama a la función create_tables() para crear las tablas al iniciar la aplicación Flask.
Rutas y funciones asociadas:
@app.route('/'): Ruta raíz de la aplicación. Renderiza la plantilla 'index.html'.

@app.route('/registro', methods=['GET', 'POST']): Ruta para registrar nuevos usuarios. Permite la solicitud GET y POST. Si se realiza una solicitud POST, se obtienen el nombre de usuario y la contraseña desde el formulario y se almacenan en la base de datos después de realizar el hash de la contraseña. Si el nombre de usuario ya existe, se muestra un mensaje de error. Si la solicitud es GET, renderiza la plantilla 'registro.html'.

@app.route('/inicio_sesion', methods=['GET', 'POST']): Ruta para iniciar sesión. Permite la solicitud GET y POST. Si se realiza una solicitud POST, se verifica el nombre de usuario y la contraseña ingresados con los registros en la base de datos. Si son válidos, se establece la sesión del usuario y se redirige a la página de menú. Si son inválidos, se muestra un mensaje de error. Si la solicitud es GET, renderiza la plantilla 'inicio_sesion.html'.

@app.route('/recuperar_contraseña', methods=['GET', 'POST']): Ruta para recuperar una contraseña olvidada. Permite la solicitud GET y POST. Si se realiza una solicitud POST, se verifica si el nombre de usuario ingresado existe en la base de datos. Si existe, se puede implementar la lógica para enviar un correo electrónico con la contraseña al usuario. En este momento, se muestra un mensaje de éxito. Si el nombre de usuario no existe, se muestra un mensaje de error. Si la solicitud es GET, renderiza la plantilla'recuperar_contraseña.html'.

@app.route('/menu'): Ruta para mostrar el menú principal. Si el usuario ha iniciado sesión, se obtienen todas las contraseñas asociadas a ese usuario desde la base de datos y se renderiza la plantilla 'mostrar_contraseñas.html' con la lista de contraseñas. Si el usuario no ha iniciado sesión, se redirige a la página de inicio de sesión.

@app.route('/profile'): Ruta para mostrar el perfil del usuario. Si el usuario ha iniciado sesión, se renderiza la plantilla 'profile.html'. Si el usuario no ha iniciado sesión, se redirige a la página de inicio de sesión.

@app.route('/agregar_contraseña', methods=['GET', 'POST']): Ruta para agregar una nueva contraseña. Si el usuario ha iniciado sesión, permite la solicitud GET y POST. Si se realiza una solicitud POST, se obtienen los datos del formulario (sitio, nombre de usuario y contraseña) y se agregan a la base de datos. Si falta algún campo, se muestra un mensaje de error. Si la solicitud es GET, renderiza la plantilla 'agregar_contraseña.html'. Si el usuario no ha iniciado sesión, se redirige a la página de inicio de sesión.

@app.route('/eliminar_contraseña/<int:password_id>', methods=['POST']): Ruta para eliminar una contraseña específica. Si el usuario ha iniciado sesión, se permite la solicitud POST y se elimina la contraseña con el ID especificado de la base de datos. Si el usuario no ha iniciado sesión, se redirige a la página de inicio de sesión.

@app.route('/cerrar_sesion'): Ruta para cerrar la sesión del usuario. Si el usuario ha iniciado sesión, se elimina la clave de sesión y se redirige a la página de inicio de sesión.

@app.route('/eliminar_cuenta'): Ruta para eliminar la cuenta del usuario. Si el usuario ha iniciado sesión, se redirige a la página de confirmación de eliminación. Si el usuario no ha iniciado sesión, se redirige a la página de inicio de sesión.

@app.route('/del_cuenta'): Ruta para eliminar la cuenta del usuario. Si el usuario ha iniciado sesión, se eliminan todas las contraseñas asociadas al usuario y se elimina el usuario de la base de datos. Luego, se elimina la clave de sesión y se redirige al formulario de registro.

@app.route('/confirmar_eliminacion', methods=['GET', 'POST']): Ruta para confirmar la eliminación de la cuenta. Si se realiza una solicitud POST y se proporciona una confirmación correcta, se redirige a la función del_cuenta(). Si se proporciona una confirmación incorrecta, se redirige al perfil del usuario. Si la solicitud es GET, renderiza la plantilla 'confirmar_eliminacion.html'.

@app.errorhandler(404): Manejador de errores para la página no encontrada. Renderiza la plantilla '404.html'.

Punto de entrada:
if __name__ == '__main__':: Verifica si el archivo es el punto de entrada principal. Si es así, se inicia la aplicación Flask llamando a app.run().
