import sys

from flask import Flask

app = Flask(__name__)

port = int(sys.argv[1])

context = ('/etc/ssl/server.crt', '/etc/ssl/server.key')

VALID_VENDOR = 'cisco'


@app.route('/0.1/directories/menu/<profile>/{vendor}'.format(vendor=VALID_VENDOR), methods=['GET'])
def menu_get(profile):
    return '', 200


@app.route('/0.1/directories/input/<profile>/{vendor}'.format(vendor=VALID_VENDOR), methods=['GET'])
def input_get(profile):
    return '', 200


@app.route('/0.1/directories/lookup/<profile>/{vendor}'.format(vendor=VALID_VENDOR), methods=['GET'])
def lookup_get(profile):
    return '', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, ssl_context=context, debug=True)
