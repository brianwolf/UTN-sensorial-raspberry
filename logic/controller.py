from flask import Blueprint, jsonify, request

import logic.config as config
import logic.service as service
from logic.model import Metric


blue_print = Blueprint('controller', __name__, url_prefix='/api/v1')


@blue_print.route('/metrics', methods=['POST'])
def add_metric():

    j = request.json
    m = Metric(
        mac=j['mac'],
        sensor_type=j['sensor_type'],
        value=j['value'],
        unit=j['unit']
    )

    service.add_metric(m)

    return '', 201


@blue_print.route('/metrics/all', methods=['GET'])
def get_all_metrics():

    result = [
        {
            'mac': m.mac,
            'sensor_type': str(m.sensor_type),
            'value': str(m.value),
            'unit': m.unit,
            'raspberry_uuid': str(m.raspberry_uuid),
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


@blue_print.route('/mocks/backend/metrics', methods=['POST'])
def mock_backend_metrics():

    config.logger().info(f'Receive body -> {request.json}')
    return '', 201
