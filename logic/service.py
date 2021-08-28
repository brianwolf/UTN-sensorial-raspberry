import threading
import time
from datetime import datetime
from typing import List

import requests

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
