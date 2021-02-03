

'''
Clase que tiene como objetivo enviar email.
'''
from envio_email_api.envio_email.password import password_gmail


class SendEMail():
    def send_email_test(self, para):
        import smtplib
        import datetime

        gmail_user = '1938web@gmail.com'
        gmail_password = password_gmail

        from_address = gmail_user
        to_address = para
        today = datetime.date.today()
        today = today.strftime('%Y-%m-%d')
        asunto = "Test Envio Email"
        mensaje=  'Envio de un correo'
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        	    """ % (from_address, ", ".join(to_address), asunto, mensaje)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(from_address, to_address, message)
        server.close()


    def send_email_puja_nueva(self, para, subasta):
        import smtplib
        import datetime

        gmail_user = '1938web@gmail.com'
        gmail_password = password_gmail

        from_address = gmail_user
        to_address = para
        today = datetime.date.today()
        today = today.strftime('%Y-%m-%d')
        asunto = "Subasta: La subasta " + subasta['titulo'][0] + 'tiene una nueva puja. '
        mensaje=  'La subasta:' + subasta['titulo'][0]  + 'tiene una nueva puja. Actualmente, la puja más alta tiene un valor de ' + subasta['puja_ganadora'][0]
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        	    """ % (from_address, ", ".join(to_address), asunto, mensaje)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(from_address, to_address, message)
        server.close()
