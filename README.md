# Api para enviar emails a través de una api python

## Introducción

En este proyecto vamos a realizar una pequeña investigación de cómo enviar un correo electrónico a través de un código 
python. Mas información en la web https://1938.com.es/api_implementacion

Además, está relacionado los artículos https://1938.com.es/ejemplo-captcha y   https://1938.com.es/instalacion-hcaptcha

Python versión 3.7.3.
### Files

En este repositorio se pueden encontrar los siguientes ficheros:

* **api/__init__.py** Este fichero recoge el código para ejecutar la api al completo.

* **api/test_comunicacion_servidor.py** Este fichero recoge el código para ejecutar las pruebas presentadas en el artículo https://1938.com.es/usar-api-angular

* **envio_email/envio_email.py** Este fichero recoge el código para enviar un email.

* **password.py** En este fichero se almacena el password de la cuenta de gmail utilizada. 
  
* **clave.json**  Este archivo continee las credenciales de google para acceder a firebase. 

* **requirements.txt** Este archivo menciona los paquetes Python necesarios para ejecutar el código.

### Prerequisites

```
altair==3.0.1
Babel==2.7.0
flask==2.1.3
Flask-Babel==0.12.2
Flask-Cors==3.0.7
Flask-Login==0.4.1
Flask-RESTful==0.3.9
formsteps==0.1.0
marshmallow==3.0.0b2
marshmallow-jsonschema==0.5.0
osconf==0.1.3
pandas
phonenumbers==8.10.12
python-dateutil==2.8.0
python-stdnum==1.11
pytz==2019.1
XlsxWriter==1.1.8
werkzeug==0.16.1
firebase-admin
itsdangerous==2.0.1
```

### Installing
Para ejecutar este proyecto es necesario ejecutar el siguiente comando y añadir las credenciales en el fichero password.py  

```
python get-pip.py install -r requirements.txt
```
o en el caso de linux

```
pip install -r requirements.txt
```

## Authors
* Rubén Pérez Ibáñez

## License
Released Under CC BY-SA 4.0 License
