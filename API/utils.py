import os
import requests
from jose import jwt


def get_public_key() -> dict:
    keycloak_internal_url = os.getenv("API_APP_KEYCLOAK_INTERNAL_URL")
    realm = os.getenv("API_APP_KEYCLOAK_REALM")
    url = f"{keycloak_internal_url}/realms/{realm}/protocol/openid-connect/certs"

    resp = requests.get(url)
    resp.raise_for_status()

    jwks = resp.json()
    return jwks['keys'][0]

def validate_token(token: str) -> dict:
    iss = os.getenv("API_APP_KEYCLOAK_REALMS_URL")

    try:
        key = get_public_key()
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=iss
        )
        return payload
    except:
        return {}
