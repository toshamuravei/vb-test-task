from aiohttp.web import Response
from ujson import dumps as ujson_dumps


class BaseJSONResponse(Response):
    def __init__(self, response_data: dict):
        response_attrs = {
            "text": ujson_dumps(response_data),
            "content_type": "application/json"
        }
        return super().__init__(**response_attrs)
