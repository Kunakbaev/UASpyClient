from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Permission:
    id: str
    name: str
    service_id: str
    service_name: str

@dataclass
class Key:
    key: str
    id: str
    service_id: str
    # service_name: str
    created_at: datetime

@dataclass
class CreatePermissionParams:
    permission_name: str

@dataclass
class GetPermissionParams:
    name: Optional[str] = None
    id: Optional[str] = None

@dataclass
class GetPermissionsResponse:
    permissions: List[Permission]

@dataclass
class StatusSuccess:
    success: bool

@dataclass
class ParseTokenParams:  
    jwt: str

@dataclass
class User:
    user_id: str

@dataclass
class CheckKeyParams:
    key: str

@dataclass
class GetAllKeysResponse:
    keys: List[Key]

@dataclass
class CheckKeyPermissionResponse:
    has_permission: bool

CheckUserPermissionResponse = CheckKeyPermissionResponse

@dataclass
class GetAllKeyPermissionsResponse:
    permissions: List[Permission]

GetAllUserPermissionsInServiceResponse = GetAllKeyPermissionsResponse
