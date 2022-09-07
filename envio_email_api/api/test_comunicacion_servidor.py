import os

from flask import jsonify, Response, request, send_file
import requests
from envio_email_api.api import Resource
import base64



'''
Para más información visita la web https://1938.com.es/usar-api-angular dónde hay una explicación
completa de estas funciones
'''
ALLOWED_EXTENSIONS = set([ 'pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



'''
Ejemplo de función que devuelve un json con una información. 
'''
class Saludo(Resource):
    def get(self):
        response = jsonify(
                {'status': 'ok', 'info': 'hola'})
        response.status_code = 200
        return response





'''
Función para devolver un fichero de una API REST
'''
class DescargarFichero(Resource):
    def get(self):
        try:
            path = os.path.abspath(os.getcwd())+ '/ejemplo.pdf'
            return send_file(path)
        except Exception as error:
            response = jsonify({'status': 'error'})
            response.status_code = 422
            return response


'''
Función para obtener un fichero de una API REST y devolverlo
'''
class DescargarFichero(Resource):
    def get(self):
        try:
            path = os.path.abspath(os.getcwd())+ '/ejemplo.pdf'
            return send_file(path)
        except Exception as error:
            response = jsonify({'status': 'error'})
            response.status_code = 422
            return response



class Obtener_fichero(Resource):
    def post(self):
        try:
            if 'file' not in request.files:
                resp = jsonify({'message': 'La api no ha recibido el archivo'})
                resp.status_code = 400
                return resp
            file = request.files['file']
            if file.filename == '':
                resp = jsonify({'message': 'El archivo no tiene nombre'})
                resp.status_code = 400
                return resp
            if file and allowed_file(file.filename):
                path = os.path.abspath(os.getcwd()) + '/envio_email_api/pdf/'
                file_almacenado = path + file.filename
                resultado_comprimido = path  + file.filename
                file.save(file_almacenado)
                return send_file(resultado_comprimido)
            else:
                resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
                resp.status_code = 400
                return resp
            response = jsonify(
                {'status': 'ok'})
            response.status_code = 200
            return response
        except Exception as error:
            print(str(error))
            response = jsonify({'status': 'error'})
            response.status_code = 422
            return response

'''
Función para devolver un ejemplo de JSON. 
'''
class Ejemplo_peticion_respuesta_json(Resource):
    def post(self):
        response = jsonify(
            {
                "links": {
                    "self": "http://example.com/articles",
                    "next": "http://example.com/articles?page[offset]=2",
                    "last": "http://example.com/articles?page[offset]=10"
                },
                "datos": {
                    "type": "articles",
                    "id": "1",
                    "attributes": {
                        "title": "JSON:API paints my bikeshed!"
                    },
                    "relationships": {
                        "author": {
                            "links": {
                                "self": "http://example.com/articles/1/relationships/author",
                                "related": "http://example.com/articles/1/author"
                            },
                            "data": {
                                "type": "people",
                                "id": "9"
                            }
                        },
                        "comments": {
                            "links": {
                                "self": "http://example.com/articles/1/relationships/comments",
                                "related": "http://example.com/articles/1/comments"
                            },
                            "data": [{
                                "type": "comments",
                                "id": "5"
                            },
                                {
                                    "type": "comments",
                                    "id": "12"
                                }
                            ]
                        }
                    }
                }
            })
        response.status_code = 200
        return response


test_resources = [
    (Saludo, '/saludo/inicial/'),
    (DescargarFichero, '/descargar_fichero_test/'),
    (Obtener_fichero, '/ejemplo_envio_fichero/'),
    (Ejemplo_peticion_respuesta_json, '/ejemplo_json/')

]
