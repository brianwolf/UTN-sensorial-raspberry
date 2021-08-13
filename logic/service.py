import threading
import time
from datetime import datetime
from typing import List

import logic.config as config
import logic.repository as repo
import logic.vars as vars
from logic.model import Metric

_THREAD_RUNNING = False


def add_metric(m: Metric) -> Metric:
    return repo.save_metric(m)


def get_metrics(limit: int) -> List[Metric]:
    return repo.get_metrics(limit)


def get_all_metrics() -> List[Metric]:
    return repo.get_all_metrics()


def send_metrics_to_backend(ms: List[Metric]):
    TODO: 'hacer el post'


def delete_metrics(creation_dates: List[datetime]):
    TODO: 'hacer el delete'


def _send_metrics_to_backend():

    global _THREAD_RUNNING

    while _THREAD_RUNNING:

        ms = get_metrics(vars.SEND_BACKEND_MAX_METRICS)
        tries = 0
        error = None

        while ms and tries < vars.SEND_BACKEND_TRIES:
            try:
                tries += 1
                config.logger().info(
                    f'Thread -> Ready to send {len(ms)} metrics in trie {tries}')

                send_metrics_to_backend(ms)
                delete_metrics([m.creation_date for m in ms])
                break

            except Exception as e:
                config.logger().warning(
                    f'Thread -> Error on send to backend -> try: {tries}, error: {e.args}')
                tries += 1
                error = e

        if error:
            config.logger().exception(error)
            TODO: 'Thread -> no hay internet, guardar menos informacion por un tiempo'

        time.sleep(vars.SEND_BACKEND_SECONDS)


def start_thread_send_backend():
    global _THREAD_RUNNING

    if _THREAD_RUNNING:
        return

    _THREAD_RUNNING = True
    threading.Thread(target=_send_metrics_to_backend).start()


def stop_thread_send_backend():
    global _THREAD_RUNNING
    _THREAD_RUNNING = False
