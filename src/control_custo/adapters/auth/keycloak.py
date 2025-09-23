import os
import requests
import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import serialization
from src.control_custo.domain.models import User


class KeycloakService:
    def __init__(self):
        self.server_url = os.getenv("KEYCLOAK_SERVER_URL", "http://keycloak:8080")
        self.internal_server_url = os.getenv("KEYCLOAK_INTERNAL_SERVER_URL", "http://keycloak:8080")
        self.realm = os.getenv("KEYCLOAK_REALM", "fastapi-realm")
        self.client_id = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-id-client")
        self.issuer = f"{self.server_url}/realms/{self.realm}"

        # Cache de chaves (dict {kid: public_key_pem})
        self._key_cache: dict[str, bytes] = {}
        self._last_fetch = 0
        self._cache_ttl = 3600  # 1h

    def _fetch_jwks(self):
        """Busca JWKS no Keycloak e atualiza o cache de chaves públicas."""
        certs_url = f"{self.internal_server_url}/realms/{self.realm}/protocol/openid-connect/certs"
        try:
            response = requests.get(certs_url, timeout=5)
            response.raise_for_status()
            jwks = response.json()
            new_cache = {}
            for key in jwks.get("keys", []):
                if key.get("use") == "sig" and "x5c" in key:
                    cert_str = f"-----BEGIN CERTIFICATE-----\n{key['x5c'][0]}\n-----END CERTIFICATE-----"
                    cert_obj = load_pem_x509_certificate(cert_str.encode())
                    pub_key = cert_obj.public_key().public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                    new_cache[key["kid"]] = pub_key
            if new_cache:
                self._key_cache = new_cache
                self._last_fetch = time.time()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Could not fetch JWKS: {e}")

    # def _get_public_key(self, kid: str):
    #     """Recupera a chave pública pelo kid, atualizando o cache se necessário."""
    #     # Atualiza cache se expirou
    #     if time.time() - self._last_fetch > self._cache_ttl or kid not in self._key_cache:
    #         self._fetch_jwks()

    #     if kid not in self._key_cache:
    #         raise HTTPException(status_code=401, detail="Invalid token: unknown kid")

    #     return self._key_cache[kid]

    def _get_public_key(self, kid: str) -> bytes:
        """Recupera a chave pública pelo kid, atualizando o cache se necessário."""
        # Atualiza cache se expirou
        if time.time() - self._last_fetch > self._cache_ttl or kid not in self._key_cache:
            self._fetch_jwks()

        if kid not in self._key_cache:
            raise HTTPException(status_code=401, detail="Invalid token: unknown kid")

        return self._key_cache[kid]

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        try:
            # Descobrir qual kid foi usado
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")
            if not kid:
                raise HTTPException(status_code=401, detail="Token sem kid no header")

            # Recuperar a chave pública correspondente
            public_key = self._get_public_key(kid)

            # Decodificar o token
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=self.client_id,  # valida client_id
                issuer=self.issuer,       # valida realm
                options={"verify_aud": False}  # desabilita verificação de audiência (opcional)
            )

            # Montar objeto User
            return User(
                id=payload.get("sub") or "",
                username=payload.get("preferred_username") or "",
                email=payload.get("email") or "",
                roles=payload.get("realm_access", {}).get("roles", []),
            )

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Instância única (injeção em rotas)
get_current_user = KeycloakService().get_current_user
