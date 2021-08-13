import ntpath
import os
from io import BytesIO

from flask import Flask, send_file

import logic.config as config
import logic.service as service
import logic.setup as setup
import logic.vars as vars

setup.prepare_deploy()

app = Flask(__name__)
config.config_flask_app(app)


@app.route('/')
def alive():

    msj = f'Version: {vars.VERSION}'

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


service.start_thread_send_backend()

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=True)
