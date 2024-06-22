import httpx
import json
from typing import Any, Dict, Tuple
from permissions_handler import PermissionHandler
from keys_handler import KeyHandler
from tokens_handler import TokenHandler
from users_handler import UserHandler
import logging
from error_response import ErrorResponse



class UASClient:
    def __init__(self, host: str, service_key: str, service_id: str, logger: logging.Logger) -> None:
        self.base_url = host
        self.service_key = service_key
        self.service_id = service_id

        self.permission_handler = PermissionHandler(self)
        self.token_handler = TokenHandler(self)
        self.key_handler = KeyHandler(self)
        self.user_handler = UserHandler(self)

        # headers={"User-Agent":"curl/7.72.0"}
        self.http_client = httpx.AsyncClient()
        self.http_client.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.service_key}"
        })

        self.permission_endpoint = f"service/{service_id}/permission"
        self.token_endpoint = "tokens"
        self.key_endpoint = f"service/{service_id}/key"
        self.service_user_endpoint = f"service/{service_id}/user"
        self.user_endpoint = "user"
        self.permission_sub_endpoint = "permission"

        self.logger = logger

    # wrap around logger
    def info(self, comment) -> None:
        if self.logger:
            self.logger.info(comment)

    def error(self, error_message) -> None:
        if self.logger:
            self.logger.error(error_message)




    async def send_request(self, req: httpx.Request, success_value: Dict[str, Any]) -> None:
        error_response = ErrorResponse(0, "")
        has_custom_error, err = await self.send_custom_request(req, success_value, error_response)

        if err:
            self.error(err)
            raise err
        elif has_custom_error:
            raise error_response

    async def send_custom_request(self, req: httpx.Request, success_value: Dict[str, Any], error_value: ErrorResponse) -> Tuple[bool, Exception]:
        self.info(self.http_client.headers)
        res = await self.http_client.send(req)
        self.info(res.status_code)
        status_ok = 200 <= res.status_code < 300

        if not status_ok:
            try:
                error_content = res.json()
                error_value.code = res.status_code
                error_value.message = error_content.get("error", "Unknown error")
                return True, None
            except json.JSONDecodeError:
                return False, Exception(f"unknown, status code: {res.status_code}")
        elif res.status_code != 204:
            try:
                success_value.update(res.json())
                return False, None
            except json.JSONDecodeError as e:
                return False, e
        return False, None

