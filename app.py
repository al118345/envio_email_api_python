from envio_email_api.config import create_app


application = create_app()


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True, use_reloader=False)
