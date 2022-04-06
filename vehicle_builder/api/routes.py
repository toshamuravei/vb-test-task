from aiohttp import web

from api.handlers import get_vehicle_details

routes = [
    web.get(r'/api/vehicles/{vehicle_id:\d+}', get_vehicle_details),
]
