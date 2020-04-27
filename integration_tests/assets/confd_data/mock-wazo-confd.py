# -*-coding: utf-8-*-
# Copyright 2016-2020 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

port = int(sys.argv[1])

API_VERSION = '1.1'

extensions_features_data = {
    'items': [
        {'feature': 'phoneprogfunckey', 'exten': '_*735.'},
        {'feature': 'enablednd', 'exten': '*25'},
        {'feature': 'fwdunc', 'exten': '_*21.'},
        {'feature': 'fwdrna', 'exten': '_*22.'},
        {'feature': 'fwdbusy', 'exten': '_*23.'},
        {'feature': 'incallfilter', 'exten': '*27'},
    ],
}

_requests = []


@app.before_request
def log_request():
    global _requests

    if request.path.startswith('/_'):
        return

    log = {
        'method': request.method,
        'path': request.path,
        'query': request.args.items(multi=True),
        'body': request.data,
        'json': request.json,
        'headers': dict(request.headers),
    }
    _requests.append(log)


@app.route('/_requests', methods=['GET'])
def list_requests():
    return jsonify({'requests': _requests})


@app.route('/_reset', methods=['POST'])
def reset_requests():
    global _requests
    _requests = []
    return '', 204


@app.route('/{}/extensions/features'.format(API_VERSION), methods=['GET'])
def extensions_features():
    return jsonify(extensions_features_data)


@app.route('/{}/users/<user_uuid>'.format(API_VERSION), methods=['GET'])
def user_uuid_get(user_uuid):
    return jsonify(
        {'id': user_uuid, 'uuid': user_uuid, 'lines': [{'name': 'line-123'}]}
    )


@app.route(
    '/{}/users/<user_uuid>/services/<service_name>'.format(API_VERSION), methods=['PUT']
)
def user_service_put(user_uuid, service_name):
    return '', 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
