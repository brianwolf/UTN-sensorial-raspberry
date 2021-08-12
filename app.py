import os

from flask import Flask, render_template, request

import logic.config as config
import logic.service as service
import setup

setup.prepare_deploy()

app = Flask(__name__)
config.config_flask_app(app)


@app.route('/')
def alive():

    version = os.getenv('VERSION', 'LOCAL')
    msj = f'Version: {version}'

    config.logger().info(msj)
    return msj, 200


service.start_thread_send_backend()

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=True)
