from flask import Flask, request, jsonify, Response
import json
import requests
import logging
import os
import sys
from flask_cors import CORS, cross_origin
from sesamutils import VariablesConfig, sesam_logger
import urllib3

urllib3.disable_warnings()
app = Flask(__name__)

## Helpers
logger = sesam_logger("Steve the logger", app=app)
CORS(app,
     resources={r"/*": {
         "origins": "*"
     }},
     headers={
         'Access-Control-Request-Headers', 'Content-Type',
         'Access-Control-Allow-Origin'
     })


@app.route('/')
def index():
    output = {
        'service': 'Autoconnect up and running',
        'remote_addr': request.remote_addr
    }
    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)