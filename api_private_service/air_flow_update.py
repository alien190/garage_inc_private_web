from flask import (Blueprint, request)
import datetime
from .air_flow_dto import air_flow_from_json
from flask import current_app
from .measurment_saver import MeasurmentSaver

bp = Blueprint('air_flow_update', __name__, url_prefix='/air_flow_update')

@bp.route('/', methods=['POST'])
def register():
    try:    
        aif_flow_dto = air_flow_from_json(request.json)
       
        with MeasurmentSaver() as saver:
            saver.save_air_flow(aif_flow_dto.sensor_id,aif_flow_dto.air_flow_rate,aif_flow_dto.temperature,aif_flow_dto.air_consumption)  

        return 'Data was updated', 200

    except Exception as error:
        print(error)
        return str(error), 500