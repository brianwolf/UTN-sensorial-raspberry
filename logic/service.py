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


def _send_metrics_to_backend():

    global _THREAD_RUNNING

    while _THREAD_RUNNING:

        ms = get_metrics(int(get(Vars.SEND_BACKEND_MAX_METRICS)))
        tries = 0
        error = None

        if not ms:
            config.logger().info('Thread -> nothing metrics to send')

        while ms and tries < int(get(Vars.SEND_BACKEND_TRIES)):
            try:
                tries += 1
                config.logger().info(
                    f'Thread -> Ready to send {len(ms)} metrics on try {tries}')

                send_metrics_to_backend(ms)
                delete_metrics([m.creation_date for m in ms])
                break

            except Exception as e:
                config.logger().warning(
                    f'Thread -> Error on send to backend -> try: {tries}, error: {e.args}')
                error = e

        if error:
            config.logger().exception(error)
            # TODO: Thread -> no hay internet, guardar menos informacion por un tiempo

        time.sleep(int(get(Vars.SEND_BACKEND_SECONDS)))


def start_thread_send_backend():
    global _THREAD_RUNNING

    if _THREAD_RUNNING:
        return

    _THREAD_RUNNING = True
    threading.Thread(target=_send_metrics_to_backend).start()


def stop_thread_send_backend():
    global _THREAD_RUNNING
    _THREAD_RUNNING = False
