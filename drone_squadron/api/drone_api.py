from sqlalchemy.engine import ResultProxy

from drone_squadron.api.base_api import BaseApi
from drone_squadron.api.squadron_api import SquadronApi
from drone_squadron.crud.drone_crud import DroneCrud
from drone_squadron.crud.squadron_crud import SquadronCrud
from drone_squadron.error.error import ValidationError
from drone_squadron.model.drone_model import DroneModel
from drone_squadron.service.calculate_cost import calculate_cost


class DroneApi(BaseApi):
    def __init__(self):
        super().__init__(DroneCrud)

    def post(self, data):
        drone_cost = 50
        cost = calculate_cost(data) + drone_cost
        model = DroneModel(data.get('name'), data.get('squadron'), cost)
        if not model.validate():
            return ValidationError(model.get_errors())
        SquadronApi().spend_scrap(data.get('squadron'), cost)
        with self.crud() as crud:
            result = crud.insert(**data)  # type: ResultProxy
            data = result.last_inserted_params()
            data['id'] = result.inserted_primary_key[0]
        return self.get_by_id(data['id'])

    def put(self, item_id, data):
        cost = calculate_cost(data)
        drone = self.get_by_id(item_id)
        model = DroneModel(drone['name'], data.get('squadron'), cost)
        if not model.validate():
            return ValidationError(model.get_errors())
        SquadronCrud().spend_scrap(data.get('squadron'), cost)
        with self.crud() as crud:
            result = crud.update(item_id=item_id, **data)  # type: ResultProxy
            data = result.last_updated_params()
        return data

    def get_by_squadron_id(self, squadron_id):
        with self.crud() as crud:
            result = crud.select_by_squadron_id(squadron_id)  # type: ResultProxy
            data = result.fetchall()
        return data
