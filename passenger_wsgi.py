import os
import sys


# sys.path.insert(0, os.path.dirname(__file__))


# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works today!\n'
#     version = 'Python %s\n' % sys.version.split()[0]
#     response = '\n'.join([message, version])
#     return [response.encode()]
from whitenoise import WhiteNoise
from SiorikLearn import wsgi

application = wsgi.application
application = WhiteNoise(application, root="/home/siorikco/LEARNSIORIK/static")
