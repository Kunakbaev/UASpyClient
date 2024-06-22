import json
from typing import Any, Dict, Optional, Union
from httpx import Request
from error_response import ErrorResponse
from models import *
from dataclasses import dataclass, asdict


GetAllUserPermissionsInServiceResponse = GetAllKeyPermissionsResponse

class UserHandler:
    def __init__(self, client) -> None:
        self.client = client

    async def grant_permission_to_user(self, user_id: str, permission_id: str) -> Optional[ErrorResponse]:
        req_url = f"{self.client.base_url}/{self.client.service_user_endpoint}/{user_id}/{self.client.permission_sub_endpoint}/{permission_id}"
        req = Request('POST', req_url)
        response_data = {}

        try:
            await self.client.send_request(req, response_data)
            if not response_data.get("success"):
                return ErrorResponse(code=500, message="Something went wrong")
            return None
        except ErrorResponse as e:
            return e

    async def check_user_permission(self, user_id: str, permission_id: str) -> Optional[bool]:
        req_url = f"{self.client.base_url}/{self.client.service_user_endpoint}/{user_id}/{self.client.permission_sub_endpoint}/{permission_id}"
        req = Request('GET', req_url)
        response_data = {}

        try:
            await self.client.send_request(req, response_data)
            return response_data.get("has_permission", False)
        except ErrorResponse as e:
            self.client.error(e)
            return None

    async def remove_user_permission(self, user_id: str, permission_id: str) -> Optional[ErrorResponse]:
        req_url = f"{self.client.base_url}/{self.client.service_user_endpoint}/{user_id}/{self.client.permission_sub_endpoint}/{permission_id}"
        req = Request('DELETE', req_url)
        response_data = {}

        try:
            await self.client.send_request(req, response_data)
            if not response_data.get("success"):
                return ErrorResponse(code=500, message="Something went wrong")
            return None
        except ErrorResponse as e:
            return e

    async def get_all_user_permissions_in_service(self, user_id: str) -> Optional[GetAllUserPermissionsInServiceResponse]:
        req_url = f"{self.client.base_url}/{self.client.service_user_endpoint}/{user_id}/{self.client.permission_sub_endpoint}/"
        req = Request('GET', req_url)
        response_data = {}

        try:
            await self.client.send_request(req, response_data)
            permissions = [Permission(**perm) for perm in response_data.get("permissions", [])]
            return GetAllUserPermissionsInServiceResponse(permissions=permissions)
        except ErrorResponse as e:
            self.client.error(e)
            return None
