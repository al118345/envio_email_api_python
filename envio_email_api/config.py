import os

from flask import Flask, g, current_app
import jinja2
from envio_email_api.metrics import Metrics
from flask_login import LoginManager
from collections import OrderedDict

try:
    # Due: https://www.python.org/dev/peps/pep-0476
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
except ImportError:
    pass



metrics = Metrics()


def create_app(**config):
    """
    Create a EnvioEmailApi app
    :param config:
    :return: EnvioEmailApi app
    """
    app = Flask(__name__, static_folder=None)
    app.config.from_envvar('EnvioEmailApi_SETTINGS', silent=True)
    app.config.update(config)

    if not app.config['SECRET_KEY']:
        app.config['SECRET_KEY'] = '343234234324234234344342423'

    if 'LOG_LEVEL' not in app.config:
        app.config['LOG_LEVEL'] = 'DEBUG'

    configure_login(app)
    configure_babel(app)
    configure_api(app)
    configure_backend(app)
    configure_metrics(app)
    configure_json_encoder(app)
    configure_cors(app)

    return app


def configure_api(app):
    """
    Configure diffenrend API endpoints
    :param app: Flask application
    :return:
    """
    from envio_email_api.api import EnvioEmailApi
    from envio_email_api.api import resources

    api = EnvioEmailApi(prefix='/api/v1')

    # Default Resources
    resources_index = OrderedDict([(r[1], r) for r in resources])

    # Custom packages resources
    import importlib
    import pkg_resources
    importlib.reload(pkg_resources)

    from pkg_resources import working_set

    templates_loader = [app.jinja_loader]



    app.jinja_loader = jinja2.ChoiceLoader(templates_loader)

    for resource in resources_index.values():
        print('Loading resource {} in {}'.format(
            resource[0], resource[1]
        ))
        api.add_resource(*resource)

    api.init_app(app)


def setup_backend_conn():
        try:
            import firebase_admin
            from firebase_admin import credentials
            from firebase_admin import firestore

            # Use a service account
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            filename = os.path.join(fileDir, 'envio_email_api/clave.json')

            cred = credentials.Certificate(filename)
            try:

                firebase_admin.initialize_app(cred)
                g.backend_cnx = firestore.client()
            except:
                g.backend_cnx = firestore.client()



        except Exception as exc:
            current_app.logger.critical("ERROR setting up backend: {}".format(exc))

def noquote(s):
    return s

def configure_backend(app):
    app.before_request(setup_backend_conn)


def configure_metrics(app):
    metrics.init_app(app)


def configure_login(app):
    from envio_email_api.login import load_user_from_header, load_user, CustomSessionInterface
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Add request loader callback
    login_manager.request_loader(load_user_from_header)
    login_manager.user_loader(load_user)
    app.session_interface = CustomSessionInterface()


def configure_babel(app):
    """Configure Babel for app
    """
    if 'BABEL_DEFAULT_LOCALE' not in app.config:
        app.config['BABEL_DEFAULT_LOCALE'] = 'es'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'




def configure_json_encoder(app):
    from envio_email_api.utils import CustomJSONEncoder
    app.json_encoder = CustomJSONEncoder


def configure_cors(app):
    from flask_cors import CORS
    cors = CORS(origins=['*'])
    cors.init_app(app)

