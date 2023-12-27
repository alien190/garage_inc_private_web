from dacite import from_dict
from dataclasses import dataclass
from typing import List

@dataclass
class Temperature_dto:
    sensor_id:int
    temperature: float
    humidity:float

def temperature_from_json(json):
    return from_dict(data_class=Temperature_dto, data=json)
