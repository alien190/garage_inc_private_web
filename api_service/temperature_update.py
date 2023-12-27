from flask import (Blueprint, request)
import datetime
from .temperature_dto import temperature_from_json
from flask import current_app
from .measurment_saver import MeasurmentSaver

bp = Blueprint('temperature_update', __name__, url_prefix='/temperature_update')

@bp.route('/', methods=['POST'])
def register():
    try:    
        temperature_dto = temperature_from_json(request.json)
       
        with MeasurmentSaver() as save:
            save(temperature_dto.sensor_id, temperature_dto.temperature, temperature_dto.humidity)  

        return 'Data was updated', 200

    except Exception as error:
        print(error)
        return str(error), 500