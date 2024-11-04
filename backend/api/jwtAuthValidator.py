import os
import jwt
import time
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64decode
from functools import lru_cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

OKTA_ISSUER = os.environ.get('OKTA_ISSUER')
OKTA_AUDIENCE = os.environ.get('OKTA_AUDIENCE')

def ttl_lru_cache(seconds_to_live: int, maxsize: int):
    def wrapper(func):
        @lru_cache(maxsize)
        def inner(__ttl, *args, **kwargs):
            return func(*args, **kwargs)
        return lambda *args, **kwargs: inner(time.time() // seconds_to_live, *args, **kwargs)
    return wrapper

@ttl_lru_cache(seconds_to_live=100, maxsize=1)
def get_public_key_from_jwks(kid):
    jwks_uri = f'{OKTA_ISSUER}/v1/keys'
    response = requests.get(jwks_uri)
    jwks = response.json()

    for key in jwks['keys']:
        if key['kid'] == kid:
            public_key_data = {
                'kty': key['kty'],
                'n': key['n'],
                'e': key['e']
            }
            return public_key_data
    return None

def construct_rsa_key(n, e):
    n = int.from_bytes(urlsafe_b64decode(n + '=='), 'big')
    e = int.from_bytes(urlsafe_b64decode(e + '=='), 'big')
    public_key = rsa.RSAPublicNumbers(e, n).public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header['kid']
            public_key_data = get_public_key_from_jwks(kid)
            if not public_key_data:
                raise ValueError('Public key not found for the given kid')
            public_key_pem = construct_rsa_key(public_key_data['n'], public_key_data['e'])
            decoded_token = jwt.decode(token, public_key_pem, algorithms=['RS256'], audience=OKTA_AUDIENCE, issuer=OKTA_ISSUER)
            user = self.get_user_from_payload(decoded_token)
            return (user, True)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {e}')
        
    def get_user_from_payload(self, payload):
        return {
            'id': payload.get('sub'),
            'is_authenticated': True
        }