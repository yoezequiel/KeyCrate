## Documentación de la Aplicación de Gestión de Contraseñas

### Bibliotecas utilizadas:
- `Flask`: Permite crear la aplicación web y gestionar las rutas y solicitudes HTTP.
- `render_template`: Renderiza las plantillas HTML para generar las páginas web.
- `request`: Proporciona acceso a los datos enviados por el cliente en las solicitudes HTTP.
- `session`: Permite almacenar y acceder a datos de sesión para usuarios.
- `redirect`: Realiza redirecciones a otras rutas.
- `sqlite3`: Permite interactuar con la base de datos SQLite.
- `hashlib`: Utilizado para realizar el hash de contraseñas.
- `urlparse`: Proporciona funciones para analizar y manipular URLs.

### Configuración de la aplicación Flask:
- `app = Flask(__name__)`: Crea una instancia de la aplicación Flask.
- `app = Flask(__name__, static_url_path='/static')`: Configura la ruta estática de la aplicación Flask.
- `app.secret_key = 'SECRET_KEY'`: Establece la clave secreta para la sesión de Flask.

### Funciones auxiliares:
- `get_db_connection()`: Establece una conexión con la base de datos SQLite y devuelve el objeto de conexión.
- `create_tables()`: Crea las tablas necesarias en la base de datos si no existen.

### Rutas y funciones asociadas:
- `/`: Ruta raíz de la aplicación. Renderiza la plantilla 'index.html'.
- `/registro`: Ruta para registrar nuevos usuarios.
- `/inicio_sesion`: Ruta para iniciar sesión.
- `/recuperar_contraseña`: Ruta para recuperar una contraseña olvidada.
- `/menu`: Ruta para mostrar el menú principal.
- `/profile`: Ruta para mostrar el perfil del usuario.
- `/agregar_contraseña`: Ruta para agregar una nueva contraseña.
- `/eliminar_contraseña/<int:password_id>`: Ruta para eliminar una contraseña específica.
- `/cerrar_sesion`: Ruta para cerrar la sesión del usuario.
- `/eliminar_cuenta`: Ruta para eliminar la cuenta del usuario.
- `/del_cuenta`: Ruta para eliminar la cuenta del usuario.
- `/confirmar_eliminacion`: Ruta para confirmar la eliminación de la cuenta.
- `errorhandler(404)`: Manejador de errores para la página no encontrada.

### Punto de entrada:
- `if __name__ == '__main__':`: Inicia la aplicación Flask.
