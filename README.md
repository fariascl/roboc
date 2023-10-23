# roboc

Bot experimental de Discord en Python

## Instalación

Es necesario tener instalado previamente Python 3 y Pip. De no ser así, se instala a través del siguiente comando:

Debian/Ubuntu: `sudo apt-get install -y python3 python3-pip`

Fedora: `sudo dnf install python3 -y python3-pip`

También, es necesario instalar MariaDB/MySQL Server

Debian/Ubuntu: `sudo apt-get install -y mariadb-server`

Fedora: `sudo dnf install mysql-community-server`

Luego, ejecutar el instalador (`sudo mysql_secure_installation`), seguir los pasos y finalizar. Posterior a esto, se debe **crear la base de datos, crear el usuario y asignarle los privilegios del usuario sobre la base de datos**.

Teniendo los pasos anteriores, se debe importar el archivo `schema.sql` en la base de datos creada. (`SOURCE schema.sql`).

Hecho lo anterior, se debe cambiar el nombre del archivo `env.example` a .`env`, y en su contenido se debe configurar las variables de entorno, como las que se ven a continuación


```
TOKEN=<token discord>
API_CLIMA_TOKEN=<(*)>

DB_HOST=<servidor base de datos>
DB_USER=<usuario base de datos>
DB_PASSWORD=<contraseña base de datos>
DB_NAME=<nombre base de datos>
```
(*) Para configurar la variable de entorno `API_CLIMA_TOKEN`, es necesario registrarse en la página de [meteored.cl](https://www.meteored.cl/api/#/registro) para así obtener una __affiliate_id__ (API KEY).

Para finalizar, se deben instalar las dependencias:

`pip3 install -r requirements.txt`

Y ejecutar el bot:

`python3 roboc.py`


## Uso
Para utilizar el bot, es necesario darle los permisos en el servidor en el cual el roboc es miembro.
Para ver el listado de comandos básicos se debe escribir `/ayuda`, y mostrará el mensaje de a continuación :
```
Hola!, soy roboc, un 🤖 para todo uso
Los comandos disponibles son: 

/recordar permite poner un recordatorio ⏰.
Uso: /recordar "asunto" dd-MM-AA hh:mm

/clima permite ver la temperatura ⛅ máxima en alguna ciudad.
Uso: /clima conce

/temblor permite ver el último temblor registrado

/torrent permite buscar torrents relacionados a un título.
Uso: /torrent los simpson

/dado permite lanzar un dado 🎲

/pregunta permite preguntar.
Uso: /pregunta "me irá bien en el certamen?"

/cachipun permite jugar al cachipún ✊ 🫲 ✌️ (al azar) entre dos usuarios.
Uso: /cachipun @usuarioA @usuarioB

/ayuda permite ver este mensaje
```


