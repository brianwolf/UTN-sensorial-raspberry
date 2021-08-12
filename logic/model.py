from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

import logic.config as config


@dataclass
class Metric(object):

    uuid: UUID
    sensor_type: str
    value: float
    creation_date: datetime

    def __init__(self, uuid: UUID, sensor_type: str, value: float, creation_date: datetime = None, raspberry_uuid: UUID = None):
        self.uuid = uuid
        self.sensor_type = sensor_type.upper().strip()
        self.value = value
        self.creation_date = creation_date
        self.raspberry_uuid = raspberry_uuid

        if not creation_date:
            self.creation_date = datetime.now()

        if not raspberry_uuid:
            self.raspberry_uuid = config.get_raspberry_uuid()

    def __eq__(self, other):
        return self.uuid == other.uuid
