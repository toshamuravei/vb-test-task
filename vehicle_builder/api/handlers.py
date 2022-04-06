from aiohttp.web import Request

from api.exceptions import BaseClientJSONError
from api.responses import BaseJSONResponse
from api.services.vehicle import BasicVehicleService


async def get_vehicle_details(request: Request):
    try:
        vehicle_id = int(request.match_info["vehicle_id"])
    except ValueError:
        raise BaseClientJSONError("Vehicle id must be int")

    vehicle_service = BasicVehicleService(vehicle_id, request["db_session"])

    vehicle = await vehicle_service.get_vehicle()
    if not vehicle:
        raise BaseClientJSONError(f"Vehicle #{vehicle_id} is not found")

    vehicle_details = await vehicle_service.obtain_vehicle_details(vehicle)
    return BaseJSONResponse(response_data=vehicle_details)
