import requests
import os
from fastapi import APIRouter, Depends
from typing import List

from ...application.services import ItemService
from ...domain.models import Item, TokenDTO, LoginRequest
from ..db.repository import InMemoryItemRepository
from ..auth.keycloak import get_current_user, User

router = APIRouter()

def get_item_service() -> ItemService:
    return ItemService(InMemoryItemRepository())

@router.get("/items", response_model=List[Item])
def list_items(service: ItemService = Depends(get_item_service), current_user: User = Depends(get_current_user)):
    return service.get_all_items()

@router.post("/items", response_model=Item)
def create_item(
    name: str,
    description: str,
    service: ItemService = Depends(get_item_service),
    current_user: User = Depends(get_current_user)):
    
    return service.create_item(name, description)

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login", response_model=TokenDTO)
def login(payload: LoginRequest):
  
    data = {
        "client_id": os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-id-client"),
        "username": payload.username,
        "password": payload.password,
        "grant_type": os.getenv("KEYCLOAK_GRANT_TYPE", "password"),
    }
    
    data["client_secret"] = os.getenv("KEYCLOAK_CLIENT_SECRET", '')

    try:
        resp = requests.post(
            "http://keycloak:8080/realms/fastapi-realm/protocol/openid-connect/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    except requests.RequestException as e:
        return {"error": "Failed to connect to authentication server", "details": str(e)}
    # retorna JSON direto do keycloak
    return resp.json()
