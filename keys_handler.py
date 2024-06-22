import json
from typing import Any, Dict, Optional, Union
from httpx import Request
from error_response import ErrorResponse
from models import *
from dataclasses import dataclass, asdict


class KeyHandler:
    def __init__(self, client) -> None:
        self.client = client

    def create_key(self) -> Optional[Key]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/"
        req = Request('POST', req_url)

        try:
            response_data = {}
            self.client.send_request(req, response_data)
            self.client.logger.debug(response_data)
            # print(response_data)
            return Key(**response_data)
        except ErrorResponse as e:
            self.client.error(f"Error: {e}")
            return None

    def check_key(self, params: CheckKeyParams) -> Optional[Key]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/check"
        req_body = params.__dict__
        req = Request('POST', req_url, data=req_body)

        try:
            response_data = {}
            self.client.send_request(req, response_data)
            return Key(**response_data)
        except ErrorResponse as e:
            self.client.error(f"Error: {e}")
            return None

    def delete_key(self, id: str) -> Optional[ErrorResponse]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/{id}"
        req = Request('DELETE', req_url)
        response_data = {}

        try:
            self.client.send_request(req, response_data)
            if not response_data.get("success"):
                return ErrorResponse(code=500, message="Something went wrong")
            return None
        except ErrorResponse as e:
            return e

    def get_key(self, id: str) -> Optional[Key]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/{id}"
        req = Request('GET', req_url)
        response_data = {}

        try:
            self.client.send_request(req, response_data)
            return Key(**response_data)
        except ErrorResponse as e:
            # print(f"Error: {e}")
            self.client.error(f"Error: {e}")
            return None

    def get_all_keys(self) -> Optional[GetAllKeysResponse]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/"
        req = Request('GET', req_url)
        response_data = {}

        try:
            self.client.send_request(req, response_data)
            keys = [Key(**key) for key in response_data.get("keys", [])]
            return GetAllKeysResponse(keys=keys)
        except ErrorResponse as e:
            # print(f"Error: {e}")
            self.client.error(f"Error: {e}")
            return None

    def grant_permission_to_key(self, key_id: str, permission_id: str) -> Optional[ErrorResponse]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/{key_id}/{self.client.permission_sub_endpoint}/{permission_id}"
        req = Request('POST', req_url)
        response_data = {}

        try:
            self.client.send_request(req, response_data)
            if not response_data.get("success"):
                return ErrorResponse(code=500, message="Something went wrong")
            return None
        except ErrorResponse as e:
            return e

    def check_key_permission(self, key_id: str, permission_id: str) -> Optional[bool]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/{key_id}/{self.client.permission_sub_endpoint}/{permission_id}"
        req = Request('GET', req_url)
        response_data = {}

        try:
            self.client.send_request(req, response_data)
            return response_data.get("has_permission", False)
        except ErrorResponse as e:
            # print(f"Error: {e}")
            self.client.error(f"Error: {e}")
            return None

    def remove_key_permission(self, key_id: str, permission_id: str) -> Optional[ErrorResponse]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/{key_id}/{self.client.permission_sub_endpoint}/{permission_id}"
        req = Request('DELETE', req_url)
        response_data = {}

        try:
            self.client.send_request(req, response_data)
            if not response_data.get("success"):
                return ErrorResponse(code=500, message="Something went wrong")
            return None
        except ErrorResponse as e:
            return e

    def get_all_key_permissions(self, key_id: str) -> Optional[GetAllKeyPermissionsResponse]:
        req_url = f"{self.client.base_url}/{self.client.key_endpoint}/{key_id}/{self.client.permission_sub_endpoint}/"
        req = Request('GET', req_url)
        response_data = {}

        

        try:
            self.client.send_request(req, response_data)
            if not response_data.get("permissions", []):
                permissions = []
            else:
                permissions = [Permission(**perm) for perm in response_data.get("permissions", [])]
            return GetAllKeyPermissionsResponse(permissions=permissions)
        except ErrorResponse as e:
            # print(f"Error: {e}")
            self.client.error(f"Error: {e}")
            return None

