import json
from typing import Any, Dict, Optional, Union
from httpx import Request
from error_response import ErrorResponse
from models import *
import client as cl
from dataclasses import dataclass, asdict
import logging


class PermissionHandler:
    def __init__(self, client) -> None:
        self.client = client

    async def create_permission(self, params: CreatePermissionParams) -> Optional[Permission]:
        req_url = f"{self.client.base_url}/{self.client.permission_endpoint}/"
        req_body = params.__dict__
        req = Request("POST", req_url, data=req_body)

        try:
            response_data = {}
            await self.client.send_request(req, response_data)
            return Permission(**response_data)
        except ErrorResponse as e:
            self.client.error(e)
            return None

    async def get_permissions(self, params: GetPermissionParams) -> Optional[GetPermissionsResponse]:
        req_url = f"{self.client.base_url}/{self.client.permission_endpoint}/"

        if params.id is None:
            if params.name is not None:
                req_url = f"{req_url}?name={params.name}"
            req = Request('GET', req_url)
            response_data = {}
            try:
                await self.client.send_request(req, response_data)
                permissions = [Permission(**perm) for perm in response_data.get("permissions", [])]
                return GetPermissionsResponse(permissions=permissions)
            except ErrorResponse as e:
                self.client.error(e)
                return None
        else:
            req_url = f"{req_url}{params.id}"
            req = Request('GET', req_url)
            response_data = {}
            try:
                await self.client.send_request(req, response_data)
                if params.name is not None and response_data.get("name") != params.name:
                    return GetPermissionsResponse(permissions=[])
                permission = Permission(**response_data)
                return GetPermissionsResponse(permissions=[permission])
            except ErrorResponse as e:
                self.client.error(e)
                return None

    async def delete_permission(self, ID: str):
        req_url = f"{self.client.base_url}/{self.client.permission_endpoint}/{ID}"
        req = Request('DELETE', req_url)
        response = {}

        try:
            await self.client.send_request(req, response)
            if not response.get("Success"):
                raise Exception("Something went wrong")
        except ErrorResponse as e:
            self.client.error(e)

