from time import time

from flask import g, current_app, request


class Metrics(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.start_timer)
        app.teardown_request(self.stop_timer)

    def start_timer(self):
        g.start_request = time()

    def stop_timer(self, response):
        stop = time()
        delta = stop - g.start_request
        current_app.logger.info('Time for %s: %ss', request.path, delta)
