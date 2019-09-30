import sys

from flask import Flask
from flask import request

app = Flask(__name__)

port = int(sys.argv[1])

context = ('/etc/ssl/server.crt', '/etc/ssl/server.key')

LOOKUP_VENDORS = {'aastra', 'cisco', 'gigaset', 'htek', 'polycom', 'snom', 'thomson', 'yealink'}
INPUT_VENDORS = {'aastra', 'cisco', 'polycom', 'snom'}
MENU_VENDORS = {'cisco'}


@app.route(
    '/0.1/directories/menu/<profile>/<xivo_user_uuid>/<vendor>', methods=['GET']
)
def menu_get(profile, xivo_user_uuid, vendor):
    if vendor not in MENU_VENDORS:
        return '', 404
    if not request.headers.get('X-Auth-Token', ''):
        return '', 401
    return '', 200


@app.route(
    '/0.1/directories/input/<profile>/<xivo_user_uuid>/<vendor>', methods=['GET']
)
def input_get(profile, xivo_user_uuid, vendor):
    if vendor not in INPUT_VENDORS:
        return '', 404
    if not request.headers.get('X-Auth-Token', ''):
        return '', 401
    return '', 200


@app.route(
    '/0.1/directories/lookup/<profile>/<xivo_user_uuid>/<vendor>', methods=['GET']
)
def lookup_get(profile, xivo_user_uuid, vendor):
    if vendor not in LOOKUP_VENDORS:
        return '', 404
    if not request.headers.get('X-Auth-Token', ''):
        return '', 401
    return '', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, ssl_context=context, debug=True)
