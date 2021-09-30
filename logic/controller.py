import random
from datetime import datetime, timedelta

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


@blue_print.route('/metrics/db/to/backend', methods=['POST'])
def send_metrics_db_to_backend():

    sent = service.send_db_metrics_to_backend()
    return jsonify({'sent': sent}), 200


@blue_print.route('/metrics/to/backend', methods=['POST'])
def send_metrics_to_backend():

    req = request.json
    ms = [
        Metric(
            mac=j['mac'],
            sensor_type=j['sensor_type'],
            value=j['value'],
            unit=j['unit']
        )
        for j in req
    ]
    service.send_metrics_to_backend(ms)

    return '', 201


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

    config.logger().info(f'Mock receive body -> {request.json}')
    return '', 201


@blue_print.route('/mocks/metrics', methods=['GET'])
def mock_metrics():

    count = int(request.args.get('count', 3))
    date_init = request.args.get('date_init')
    date_final = request.args.get('date_init')
    time_delta = request.args.get('time_delta')

    if date_init:
        date_init = datetime.fromisoformat(date_init)

    if date_final:
        date_final = datetime.fromisoformat(date_final)

    if time_delta == 'minutes':
        time_delta = 60

    if time_delta == 'hours':
        time_delta = 60 ** 2

    if time_delta == 'days':
        time_delta = 24 * 60 ** 2

    service.metrics_hard(count, date_init, date_final, time_delta)

    return '', 200
