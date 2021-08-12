from typing import List
from uuid import UUID

import logic.sqlite as sqlite
from logic.model import Metric
from datetime import datetime

_TABLE = 'METRIC'


def save_metric(m: Metric) -> Metric:

    query = f'''
        INSERT INTO {_TABLE} (CREATION_DATE, UUID, SENSOR_TYPE, VALUE)
        VALUES (?,?,?,?);
    '''
    params = [m.creation_date, str(m.uuid), m.sensor_type, m.value]

    sqlite.exec(query=query, params=params)

    return m


def get_metrics(limit: int) -> List[Metric]:

    query = f'''
        SELECT * FROM {_TABLE} LIMIT {limit};
    '''
    params = []

    result = sqlite.select(query=query, params=params)

    return [
        Metric(
            creation_date=datetime.fromisoformat(r.get('CREATION_DATE')),
            uuid=UUID(r.get('UUID')),
            sensor_type=r.get('SENSOR_TYPE'),
            value=r.get('VALUE')
        )
        for r in result
    ]


def get_all_metrics() -> List[Metric]:

    query = f'''
        SELECT * FROM {_TABLE};
    '''
    params = []

    result = sqlite.select(query=query, params=params)

    return [
        Metric(
            creation_date=datetime.fromisoformat(r.get('CREATION_DATE')),
            uuid=UUID(r.get('UUID')),
            sensor_type=r.get('SENSOR_TYPE'),
            value=r.get('VALUE')
        )
        for r in result
    ]
