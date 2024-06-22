import json
from typing import Any, Dict, Optional, Union
from httpx import Request
from error_response import ErrorResponse
from models import *
from dataclasses import dataclass, asdict


class TokenHandler:
    def __init__(self, client) -> None:
        self.client = client

    async def parse_token(self, params: ParseTokenParams) -> Optional[User]:
        req_url = f"{self.client.base_url}/{self.client.token_endpoint}/parse"

        req_body = params.__dict__
        req = Request("POST", req_url, data=req_body)

        try:
            response_data = {}
            await self.client.send_request(req, response_data)
            return User(**response_data)
        except ErrorResponse as e:
            self.client.error(e)
            return None

