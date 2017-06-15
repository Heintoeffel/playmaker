#!/usr/bin/env python3

from flask import Flask, render_template, request
from googleplay_api.service import Play

import json, os

static = '/usr/share/playmaker/static'
static_path = static if os.path.isdir(static) else 'static'
templates = '/usr/share/playmaker/templates'
templates_path = templates if os.path.isdir(templates) else 'templates'

# application setup
app = Flask(__name__, static_folder=static_path, template_folder=templates_path)
service = Play()


@app.route('/')
def render_home():
    return render_template('index.html')


@app.route('/gplay/search', methods=['GET'])
def search_app():
    number = request.args.get('numEntries')
    if number is not '':
        return json.dumps(service.search(request.args.get('search'),
                                         int(number)))
    return json.dumps(service.search(request.args.get('search')))


@app.route('/gplay/download', methods=['POST'])
def download_app():
    toDownload = service.download_selection(request.json['download'])
    return json.dumps(toDownload)


@app.route('/gplay/check', methods=['POST'])
def check_local():
    return json.dumps(service.check_local_apks())


@app.route('/gplay/getapps', methods=['GET'])
def get_apks():
    apps = sorted(service.currentSet, key=lambda k: k['title'])
    return json.dumps(apps)

@app.route('/gplay/delete', methods=['POST'])
def delete_app():
    res = service.remove_local_app(request.json['delete'])
    if res:
        return 'OK'
    else:
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0')