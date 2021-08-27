import ntpath
import os
from io import BytesIO

from flask import Flask, jsonify, request, send_file

import logic.config as config
import logic.service as service
import logic.setup as setup
from logic.vars import Vars, get, current_vars, set

setup.prepare_deploy()

app = Flask(__name__)
config.config_flask_app(app)


@app.route('/')
def alive():

    msj = f'Version: {get(Vars.VERSION)}'

    config.logger().info(msj)
    return msj, 200


@app.route('/postman', methods=['GET'])
def download_postman_collection():

    postman_files = sorted([
        f for f in os.listdir(os.getcwd())
        if str(f).endswith('.postman_collection.json')
    ], reverse=True)

    collection_dir = next(iter(postman_files), None)

    return send_file(BytesIO(open(collection_dir, 'rb').read()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(collection_dir))


@app.route('/vars', methods=['GET'])
def get_vars():
    return jsonify(current_vars()), 200


@app.route('/vars', methods=['PUT'])
def set_var():
    j = request.json

    for k, v in j.items():
        set(Vars[k], str(v))

    return '', 200


service.start_thread_send_backend()

if __name__ == '__main__':
    app.run(host=get(Vars.HOST), port=get(Vars.PORT), debug=True)
