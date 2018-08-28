#!/usr/bin/env python

import logging
# import os
import re
import socket
# import time
import requests

from flask import Flask, jsonify, request

logPath = "/tmp/flasklog"

MyHostName = socket.gethostname()
MyResolvedName = socket.gethostbyname(socket.gethostname())

logging.basicConfig(
    filename=logPath,
    level=logging.DEBUG, # if appDebug else logging.INFO,
    format="%(asctime)s esteps-sds 0.0.1 %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.info("esteps-sds initializing on %s (resolved %s)" % (MyHostName, MyResolvedName))

TOKEN = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read()
ENDPOINT_URL_TEMPLATE = "https://kubernetes/api/v1/namespaces/default/endpoints/%s"
ENDPOINTS = {}

SERVICE_RE = re.compile(r'^[a-z0-9-_]+$')

app = Flask(__name__)

########
# USER CRUD

@app.route('/v1/registration/<service_name>', methods=[ 'GET' ])
def handle_endpoint(service_name):
    if not SERVICE_RE.match(service_name):
        return "invalid service name '%s'" % service_name, 503

    url = ENDPOINT_URL_TEMPLATE % service_name

    r = requests.get(url, headers={"Authorization": "Bearer " + TOKEN}, verify=False)

    if r.status_code != 200:
        return jsonify({ "hosts": [] })

    endpoints = r.json()

    hostdicts = []
    sofar = None

    if "subsets" in endpoints:
        sofar = endpoints["subsets"]

    if sofar:
        sofar = sofar[0] 

        if "addresses" in sofar:
            sofar = sofar["addresses"]

    if sofar:
        for x in sofar:
            if "ip" in x:
                hostdicts.append({
                    "ip_address": x["ip"],
                    "port": 80,
                    "tags": {}
                })

    return jsonify({ "hosts": hostdicts })

@app.route('/v1/health')
def root():
    return jsonify({ "ok": True, "msg": "SDS healthy!" })

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
