import os

from flask import jsonify, Response, request, send_file
import requests
from envio_email_api.api import Resource
import base64




class Saludo(Resource):
    def get(self):
        response = jsonify(
                {'status': 'ok', 'info': 'hola'})
        response.status_code = 200
        return response






class DescargarFichero(Resource):
    def get(self):
        print('rte')
        try:
            path = os.path.abspath(os.getcwd())+ '/ejemplo.pdf'
            return send_file(path)
        except Exception as error:
            response = jsonify({'status': 'error'})
            response.status_code = 422
            return response



test_resources = [
    (Saludo, '/saludo/inicial/'),
    (DescargarFichero, '/descargar_fichero_test/')

]
