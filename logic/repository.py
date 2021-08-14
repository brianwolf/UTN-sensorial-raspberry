from datetime import datetime
from typing import List
from uuid import UUID

import logic.sqlite as sqlite
from logic.model import Metric

_TABLE = 'METRIC'


def save_metric(m: Metric) -> Metric:

    query = f'''
        INSERT INTO {_TABLE} (CREATION_DATE, MAC, SENSOR_TYPE, RASPBERRY_UUID, VALUE, UNIT)
        VALUES (?,?,?,?,?,?);
    '''
    params = [
        m.creation_date,
        m.mac,
        m.sensor_type,
        str(m.raspberry_uuid),
        m.value,
        m.unit
    ]

    sqlite.exec(query=query, params=params)

    return m


def get_metrics(limit: int) -> List[Metric]:

    query = f'''
        SELECT * FROM {_TABLE} LIMIT {limit};
    '''
    params = []

    result = sqlite.select(query=query, params=params)

    return _to_metrics(result)


def get_all_metrics() -> List[Metric]:

    query = f'''
        SELECT * FROM {_TABLE};
    '''
    params = []

    result = sqlite.select(query=query, params=params)

    return _to_metrics(result)


def delete_metrics(creation_dates: List[datetime]):

    if not creation_dates:
        return

    query_dates = ''
    for d in creation_dates:
        query_dates += f'\'{d}\','
    query_dates = query_dates[0:-1]

    query = f'''
        DELETE FROM {_TABLE}
        WHERE CREATION_DATE in ({query_dates});
    '''

    sqlite.exec(query=query)


def _to_metrics(result: List) -> List[Metric]:
    return [
        Metric(
            creation_date=datetime.fromisoformat(r.get('CREATION_DATE')),
            mac=r.get('MAC'),
            sensor_type=r.get('SENSOR_TYPE'),
            raspberry_uuid=UUID(r.get('RASPBERRY_UUID')),
            value=r.get('VALUE'),
            unit=r.get('UNIT')
        )
        for r in result
    ]
