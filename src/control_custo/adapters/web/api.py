import logging
import requests
import os
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from control_custo.application.services import ItemService
from control_custo.domain.models import Item, TokenResponse, LoginRequest
from control_custo.adapters.db.repository import InMemoryItemRepository
from control_custo.adapters.auth.keycloak import get_current_user, User

router = APIRouter()

def get_item_service() -> ItemService:
    """
    Returns an instance of ItemService that is used to handle CRUD operations
    for items.

    The ItemService is instantiated with an InMemoryItemRepository, which is a simple
    in-memory repository that is used to store items.

    Returns:
        ItemService: An instance of ItemService that is used to handle CRUD operations
        for items.
    """
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


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):

    if not payload.username or not payload.password:
        raise HTTPException(
            status_code=422,
            detail="Credenciais de login inválidas."
        )

    client_id = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-id-client")
    grant_type = os.getenv("KEYCLOAK_GRANT_TYPE", "password")

    data = {
        "client_id": client_id,
        "username": payload.username,
        "password": payload.password,
        "grant_type": grant_type,
    }
    
    data["client_secret"] = os.getenv("KEYCLOAK_CLIENT_SECRET", '')
    realm = os.getenv("KEYCLOAK_REALM", "fastapi")
    
    try:
        resp = requests.post(
            f"http://keycloak:8080/realms/{realm}/protocol/openid-connect/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        return resp.json()
    except Exception as e:
        logging.error(f"Request exception: {e}")
        raise HTTPException(
            status_code=422,
            detail="Falha ao conectar ao servidor de autenticação."
        )
