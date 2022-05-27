from werkzeug.exceptions import MethodNotAllowed
from flask import jsonify, g, abort, request, url_for, redirect, current_app, render_template
from flask_restful import Resource, Api
from flask_login import login_required
from flask_babel import lazy_gettext
from formsteps.forms import FormStep

from ..envio_email.envio_email import SendEMail
from ..login import check_login_user, token_valid
from ..utils import ArgumentsParser
import requests

class EnvioEmailApi(Api):
    pass


class BaseResource(Resource):
    pass


class ApiCatchall(BaseResource):

    def get(self, path):
        abort(404)

    post = get
    put = get
    delete = get
    patch = get


class ModelResource(BaseResource):

    model = None

    def __init__(self):
        self.force_filter = None
        self.force_limit = None

    def get(self, *args, **kwargs):
        try:
            search_params, limit, offset = ArgumentsParser.parse()
        except (ValueError, SyntaxError) as e:
            response = jsonify({
                'status': 'ERROR',
                'errors': {'filter': 'No valid filter'}
            })
            response.status_code = 422
            return response
        try:
            if self.force_filter:
                search_params += self.force_filter
            if self.force_limit:
                limit = self.force_limit
            model = self.model()
            result = model.get(search_params, limit=limit, offset=offset)
        except :
            response = jsonify({'status': 'ERROR'})
            response.status_code = 422
            return response
        return jsonify(dict(result._asdict()))


class ReadOnlyResource(BaseResource):

    def not_allowed(self):
        raise MethodNotAllowed

    post = patch = not_allowed


class SecuredResource(BaseResource):

    method_decorators = [login_required]


class ResourceFormStep(Resource, FormStep):

    n_steps = 0

    @property
    def step_url(self):
        return url_for(self.__class__.__name__.lower())

    def build_response_dict(self, errors=None):
        if errors is None:
            errors = []
        definition = self.definition
        definition['status'] = 200
        definition['result']['render'].update({
            'errors': errors,
            'done': False,
            'steps': self.n_steps
        })
        return definition

    def make_response(self, errors=None):
        return jsonify(self.build_response_dict(errors))

    def get(self):
        return self.make_response()

    def post(self):
        current_app.logger.debug('JSON: {}'.format(request.json))
        form_data = request.json.get(self.serializer.__class__.__name__)
        current_app.logger.debug('Form data: {}'.format(form_data))
        if form_data is None:
            form_data = {}
        errors = self.validate(form_data)
        current_app.logger.debug('Errors: {}'.format(errors))
        return self.make_response(errors)


class SecuredResourceFormStep(ResourceFormStep, SecuredResource):
    pass



class UserToken(Resource):
    def post(self):
        g.login_via_header = True
        token = check_login_user(**request.json)
        return jsonify({
            'token': token
        })


class UserTokenValid(Resource):
    def post(self):
        # Don't use cookies
        g.login_via_header = True
        user = token_valid(request.json.get('token'))
        return jsonify({
            'token_is_valid': user is not None
        })

'''
Función destinada al envio de un email sencillo
'''
class Envio_Sencillo_Email (SecuredResource):
    def post(self,email_destino):
        try:
            enviar_email = SendEMail()
            enviar_email.send_email_test(email_destino)
            response = jsonify({'status': 'ok'})
            response.status_code = 200
            return response
        except:
            response = jsonify({'status': 'error'})
            response.status_code = 422
            return response


'''
Función destinada a conectarse a firebase y obtener un documento tipo subasta
'''
class Subasta(SecuredResource):
    def get(self,subasta):
        # Don't use cookies
        db = g.backend_cnx
        # Project ID is determined by the GCLOUD_PROJECT environment variable
        doc_ref = db.collection(u'subastas').document(subasta)
        doc = doc_ref.get()
        # print(u'Document data: {}'.format(doc.to_dict()))
        enviar_email = SendEMail()
        for i in doc.to_dict()['acceso_subasta']:
            enviar_email.send_email_puja_nueva(i,doc.to_dict() )


'''
Función destinada a realizar una verificación de captcha de google
'''
class Verificar_Captcha(Resource):
        def post(self, token):
            recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_secret_key = ''
            payload = {
                'secret': recaptcha_secret_key,
                'response': token,
                'remoteip': request.remote_addr,
            }
            response = requests.post(recaptcha_url, data=payload)
            result = response.json()
            return result.get('success', False)


'''
Función destinada a realizar una verificación de hCaptcha
'''
class Verificar_HCaptcha(Resource):
        def post(self, token):
            recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_secret_key = 'Secret_key_hcaptcha'
            payload = {
                'secret': recaptcha_secret_key,
                'response': token,
                'remoteip': request.remote_addr,
            }
            response = requests.post(recaptcha_url, data=payload)
            result = response.json()
            return result.get('success', False)


local_resources = [
    (ApiCatchall, '/<path:path>/'),
    (UserToken, '/get_token'),
    (UserTokenValid, '/is_token_valid'),
    (Subasta, '/subasta/<string:subasta>/'),
    (Envio_Sencillo_Email, '/envio_email/<string:email_destino>/'),
    (Verificar_Captcha, '/verificar/<string:token>/'),
    (Verificar_HCaptcha, '/verificar/<string:token>/'),

]

resources = (local_resources

)
