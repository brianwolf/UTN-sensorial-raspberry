import random

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

    metrics = []

    count_metrics = int(request.args.get('count', 10))

    for n in range(0, count_metrics):

        rnd = random.randint(1, 4)

        if rnd == 1:
            mac='02:42:21:1f:e8:16-1'
            sensor_type = 'temperatura'
            value = 50 * random.random()
            unit = 'ºC'

        if rnd == 2:
            mac='02:42:21:1f:e8:16-2'
            sensor_type = 'humedad'
            value = 60 * random.random()
            unit = '% HR'

        if rnd == 3:
            mac='02:42:21:1f:e8:16-3'
            sensor_type = 'calidad_del_aire'
            value = 90 * random.random()
            unit = 'PPM CO2'

        if rnd == 4:
            mac='02:42:21:1f:e8:16-4'
            sensor_type = 'produccion'
            value = int(random.randint(0, 3))
            unit = 'bool'

        m = Metric(
            mac=mac,
            sensor_type=sensor_type,
            value=value,
            unit=unit
        )
        service.add_metric(m)

    return '', 200
