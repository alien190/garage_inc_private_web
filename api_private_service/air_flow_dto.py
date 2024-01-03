from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Air_flow_dto:
    sensor_id:int
    air_flow_rate:float
    temperature: float
    air_consumption: float


def air_flow_from_json(json):
    return from_dict(data_class=Air_flow_dto, data=json)
