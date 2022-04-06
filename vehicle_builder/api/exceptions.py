from typing import Optional

from aiohttp.web import HTTPClientError
from ujson import dumps as ujson_dumps


DEFAULT_CLIENT_ERR_CODE: int = 400


class BaseClientJSONError(HTTPClientError):
    DEFAULT_ERR_DETAILS = "Error details was not specified"

    def __init__(self, err_msg: Optional[str] = None):
        error_attrs = {
            "content_type": "application/json",
            "text": ujson_dumps({"details": err_msg if err_msg else self.DEFAULT_ERR_DETAILS})
        }
        return super().__init__(**error_attrs)
