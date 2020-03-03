from werkzeug.wrappers import Request, Response, ResponseStream
from datetime import datetime,timedelta

class middleware:
    def __init__(self, rate_limit, app):
        self.rate_limit = timedelta(seconds=rate_limit)
        self.last_request = None
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if self.tooFast():
            res = Response(u'Too Many Requests', mimetype= 'text/plain', status=429)
            return res(environ, start_response)

        self.incrementTimer()
        return self.app(environ, start_response)

    def too_fast(self):
        if self.last_request == None:
            self.incrementTimer()
            return False

        if datetime.now() - self.last_request < self.rate_limit:
            return True
        return False

    def incrementTimer(self):
        self.last_request = datetime.now()