from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import logic.config as config


@dataclass
class Metric(object):

    creation_date: datetime
    mac: str
    sensor_type: str
    raspberry_uuid: UUID
    value: float
    unit: str

    def __init__(self, mac: str, sensor_type: str, value: float, unit: str, creation_date: datetime = None, raspberry_uuid: UUID = None):
        self.mac = mac
        self.sensor_type = sensor_type.upper().strip()
        self.value = value
        self.unit = unit.upper().strip()
        self.creation_date = creation_date
        self.raspberry_uuid = raspberry_uuid

        if not creation_date:
            self.creation_date = datetime.now()

        if not raspberry_uuid:
            self.raspberry_uuid = config.get_raspberry_uuid()

    def __eq__(self, other):
        return self.mac == other.mac
