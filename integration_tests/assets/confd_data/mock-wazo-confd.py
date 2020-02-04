# -*-coding: utf-8-*-
# Copyright 2020 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

port = int(sys.argv[1])

API_VERSION = '1.1'

context = ('/usr/local/share/ssl/server.crt', '/usr/local/share/ssl/server.key')

extensions_features_assoc = {
    'phoneprogfunckey': '_*735',
    'enablednd': '*25',
    'fwdunc': '_*21',
    'fwdbusy': '_*23',
    'fwdrna': '_*22',
}

def _json_extension(exten):
    return jsonify({
        'items': [
            {
                'exten': exten,
            },
        ],
    })


@app.route('/{}/extensions/features'.format(API_VERSION), methods=['GET'])
def extensions_features():
    search = request.args.get('search')
    return _json_extension(extensions_features_assoc.get(search))


@app.route('/{}/users/<user_uuid>'.format(API_VERSION), methods=['GET'])
def user_uuid_get(user_uuid):
    return jsonify({
        'id': 123,
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, ssl_context=context, debug=True)
