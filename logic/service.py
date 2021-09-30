import random
import threading
import time
from datetime import datetime, timedelta
from os import terminal_size
from typing import List

import requests
from flask import json
from flask.json import jsonify

import logic.config as config
import logic.repository as repo
from logic.model import Metric
from logic.vars import Vars, get

_THREAD_RUNNING = False


def add_metric(m: Metric) -> Metric:
    return repo.save_metric(m)


def get_metrics(limit: int) -> List[Metric]:
    return repo.get_metrics(limit)


def get_all_metrics() -> List[Metric]:
    return repo.get_all_metrics()


def send_metrics_to_backend(ms: List[Metric]):

    data = [
        {
            'mac': m.mac,
            'sensor_type': str(m.sensor_type),
            'value': str(m.value),
            'unit': m.unit,
            'raspberry_uuid': str(m.raspberry_uuid),
            'creation_date': m.creation_date.isoformat()
        }
        for m in ms
    ]

    with config._APP.app_context():
        config.logger().info(f'Sending -> {len(data)} mectrics')
        r = requests.post(url=get(Vars.SEND_BACKEND_URL), json=data)
        config.logger().info(
            f'Response -> status: {r.status_code}')


def delete_metrics(creation_dates: List[datetime]):
    repo.delete_metrics(creation_dates)


def send_db_metrics_to_backend() -> int:

    ms = get_metrics(int(get(Vars.SEND_BACKEND_MAX_METRICS)))
    if not ms:
        config.logger().info('There are no metrics to send')
        return 0

    tries = 0
    while tries < int(get(Vars.SEND_BACKEND_TRIES)):
        try:
            tries += 1
            config.logger().info(
                f'Ready to send {len(ms)} metrics on try {tries}')

            send_metrics_to_backend(ms)
            delete_metrics([m.creation_date for m in ms])
            break

        except Exception as e:
            config.logger().warning(
                f'Error on send to backend -> try: {tries}, error: {e.args}')

            if tries == int(get(Vars.SEND_BACKEND_TRIES)):
                raise e

    config.logger().info(
        f'Were sent to backend {len(ms)} metrics on try {tries}')
    return len(ms)


def _thread_send_metrics_to_backend():

    while thread_can_run():
        try:
            send_db_metrics_to_backend()

        except Exception as e:
            config.logger().exception(e)

        time.sleep(int(get(Vars.SEND_BACKEND_SECONDS)))


def start_thread_send_backend():
    global _THREAD_RUNNING

    if thread_can_run():
        return

    _THREAD_RUNNING = True
    threading.Thread(target=_thread_send_metrics_to_backend).start()


def stop_thread_send_backend():
    global _THREAD_RUNNING
    _THREAD_RUNNING = False


def thread_can_run() -> bool:
    return _THREAD_RUNNING


def metrics_hard(count: int, date_init: datetime, date_final: datetime, time_delta: int):

    sensor_types = ['temperatura', 'humedad', 'calidad_del_aire', 'produccion']

    sensor_types = {
        'temperatura': {
            'macs': ['T1', 'T2', 'T3'],
            'unit': 'ºC'
        },
        'humedad': {
            'macs': ['H1', 'H2', 'H3'],
            'unit': '% HR'
        },
        'calidad_del_aire': {
            'macs': ['A1', 'A2', 'A3'],
            'unit': 'PPM CO2'
        },
        'produccion': {
            'macs': ['P1', 'P2', 'P3'],
            'unit': 'bool'
        }
    }

    for sensor_type, conf in sensor_types.items():
        for mac in conf.get('macs'):
            for n in range(0, count):

                value = random_value(sensor_type)
                creation_date = random_date(date_init, date_final, time_delta)

                m = Metric(
                    mac=mac,
                    sensor_type=sensor_type,
                    value=value,
                    unit=conf.get('unit'),
                    creation_date=creation_date
                )
                add_metric(m)


def random_value(sensor_type: str) -> int:

    if sensor_type == 'temperatura':
        return random.randint(15, 35)

    if sensor_type == 'humedad':
        return random.randint(50, 95)

    if sensor_type == 'calidad_del_aire':
        return random.randint(50, 90)

    if sensor_type == 'produccion':
        return random.randint(0, 2)


def random_date(date_init: datetime = None, date_final: datetime = None, time_delta: int = None):

    if time_delta and date_init and date_final:

        while True:
            date_result = _random_date(time_delta)
            if date_init < date_result < date_final:
                return date_result

    if date_init and date_final:
        time_rnd = date_init.timestamp() + random.random() * (date_final.timestamp() -
                                                              date_init.timestamp())
        time_rnd += (random.randint(0, 60) + random.randint(0, 60) *
                     60 + random.randint(0, 60) * 3600)
        return datetime.fromtimestamp(time_rnd)

    return datetime.now() + (timedelta(minutes=20 * random.random()) * (-1)**int(random.randint(1, 2)))


def _random_date(time_delta: int):
    cte = 10
    time_rnd = random.randint(1, cte) * cte * time_delta * 1000

    time_add = timedelta(milliseconds=time_rnd)
    return datetime.now() + time_add * (-1)**(random.randint(1, 2))
