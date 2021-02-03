from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask_login import UserMixin, login_user
from flask import current_app, g, request
from flask.sessions import SecureCookieSessionInterface


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(
            *args, **kwargs
        )


class EnvioEmailUser(UserMixin):
    """
    Envio email User User class
    """
    def __init__(self, user_id, login, **kwargs):
        self.user_id = user_id
        self.login = login
        self.locale = current_app.config['BABEL_DEFAULT_LOCALE']
        for name, value in kwargs.items():
            setattr(self, name, value)

    def is_authenticated(self):
        """Check if this type of user is authenticated

        Always returns True
        """
        return True

    def is_active(self):
        """Check if this user is activated

        Always returns True
        """
        return True

    def get_id(self):
        """
        Get the user identification

        :return: user identification
        :rtype: str
        """
        return self.user_id

    def get_login(self):
        """
        Get the user login ID
        :return: login ID
        :rtype: str
        """
        return self.login

    @classmethod
    def login(cls, user, password):
        """
        Check if the user and password are correct
        :param user: User name
        :param password: Password
        :return: an instance of the current object user
        :rtype: Envio Email User
        """
        if user == "Subasta" and password == "Sub123Ruben":
            kwargs = {
                'id': 1,
                'user_id': str(1),
                'login': 'Subasta',
                'email': 'rubenpeib@gmail.com',
            }
            kwargs['locale'] = 'ES'
            return cls(**kwargs)
        return None

    def change_password(self, current, password):
        """
        Changes the password of the current user

        Uses the backend to do that, calling `change_password` from EnvioEmailUser

        :param current: Current password
        :param password: New password
        :return:
        """
        return None

    @property
    def token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600 * 24)
        token = s.dumps(vars(self)).decode('utf-8')
        return token


def load_user_from_header(request):
    current_app.logger.debug('Getting token from header')
    token = request.headers.get('Authorization')
    return token_valid(token)


def token_valid(token):
    if token is not None:
        s = Serializer(current_app.config['SECRET_KEY'])
        current_app.logger.debug('Using secret: {}'.format(current_app.config['SECRET_KEY']))
        try:
            values = s.loads(token)
            g.partner_id = int(values['user_id'])
            current_app.logger.debug('Current partner id: {}'.format(
                g.partner_id
            ))
            return EnvioEmailUser(**values)
        except SignatureExpired:
            current_app.logger.debug('Token has expired')
        except BadSignature as exc:
            current_app.logger.debug('Token seems not valid: {}'.format(exc.message))
    return None


def generate_token(user):
    return user.token


def check_login_user(user, password):
    # Get the user and all this stuff
    current_app.logger.debug('Checking login for user: {}'.format(
        user
    ))
    logged_user = EnvioEmailUser.login(user, password)
    if logged_user is not None:
        current_app.logger.debug('Login for user: {} OK'.format(
            user
        ))
        login_user(logged_user)
        return generate_token(logged_user)
    else:
        current_app.logger.debug('Login for user: {} ERROR'.format(
            user
        ))
        return None


def load_user(user_id):
    user = EnvioEmailUser(user_id=user_id)
    g.partner_id = int(user_id)
    return user
