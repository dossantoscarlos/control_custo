
import os
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.control_custo.domain.models import User


class KeycloakService:
    def __init__(self, server_url: str, internal_server_url: str, realm: str, client_id: str, issuer: str):
        self.server_url = server_url
        self.internal_server_url = internal_server_url
        self.realm = realm
        self.client_id = client_id
        self.issuer = issuer
        self.public_key = self._get_public_key()

    def _get_public_key(self):
        certs_url = f"{self.internal_server_url}/realms/{self.realm}/protocol/openid-connect/certs"
        try:
            response = requests.get(certs_url)
            response.raise_for_status()
            jwks = response.json()
            # Find the key with use='sig' (signing)
            for key in jwks['keys']:
                if key['use'] == 'sig':
                    # The public key is the first element of the x5c array
                    return f"-----BEGIN CERTIFICATE-----\n{key['x5c'][0]}\n-----END CERTIFICATE-----"
            raise HTTPException(status_code=500, detail="Public key for signing not found in JWKS")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Could not fetch public key from Keycloak: {e}")

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.issuer,
                options={"verify_aud": False} # Set to True in production
            )

            user = User(
                id=payload.get("sub") or "",
                username=payload.get("preferred_username") or "",
                email=payload.get("email") or  "",
                roles=payload.get("realm_access", {}).get("roles", []),
            )
            return user
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL") or "http://keycloak:8080"
KEYCLOAK_INTERNAL_SERVER_URL = os.getenv("KEYCLOAK_INTERNAL_SERVER_URL") or "http://keycloak:8080"
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM") or "master"
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID") or "fastapi-app"
KEYCLOAK_ISSUER = os.getenv("KEYCLOAK_ISSUER") or "http://keycloak:8080/realms/master"

keycloak_service = KeycloakService(
    server_url=KEYCLOAK_SERVER_URL,
    internal_server_url=KEYCLOAK_INTERNAL_SERVER_URL,
    realm=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID,
    issuer=KEYCLOAK_ISSUER,
)

get_current_user = keycloak_service.get_current_user
