from uuid import UUID, uuid4

from flask import Blueprint, jsonify, render_template, request

import logic.service as service
from logic.model import Metric

blue_print = Blueprint('receiver', __name__, url_prefix='/api/v1')


@blue_print.route('/metrics', methods=['POST'])
def add_metric():

    body = request.json
    m = Metric(
        uuid=UUID(body['uuid']),
        sensor_type=body['sensor_type'],
        value=body['value']
    )

    service.add_metric(m)

    return '', 201


@blue_print.route('/metrics/all', methods=['GET'])
def get_all_metrics():

    asd = service.get_all_metrics()

    result = [
        {
            'uuid': str(m.uuid),
            'sensor_type': str(m.sensor_type),
            'value': str(m.value),
            'creation_date': m.creation_date.isoformat()
        }
        for m in service.get_all_metrics()
    ]

    return jsonify(result), 200


@blue_print.route('/thread/start', methods=['GET'])
def thread_start():

    service.start_thread_send_backend()
    return jsonify({'running': True}), 200


@blue_print.route('/thread/stop', methods=['GET'])
def thread_stop():

    service.stop_thread_send_backend()
    return jsonify({'running': False}), 200
