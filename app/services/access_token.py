import os

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class AccessToken:
    def __init__(self, algorithm='RS256'):
        self.public_key = self.load_public_key(os.getenv('APP_SECURITY_PUBLIC_KEY'))
        self.private_key = self.load_private_key(os.getenv('APP_SECURITY_PRIVATE_KEY'))
        self.algorithm = algorithm

    @staticmethod
    def load_public_key(public_key_path):
        with open(public_key_path, 'rb') as pem_file:
            public_key_pem = pem_file.read()

        return serialization.load_pem_public_key(public_key_pem, backend=default_backend())

    @staticmethod
    def load_private_key(private_key_path):
        with open(private_key_path, 'rb') as pem_file:
            private_key_pem = pem_file.read()

        return serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

    def decode(self, token):
        try:
            return jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
                audience=os.getenv('APP_SECURITY_AUDIENCE'),
            )
        except jwt.InvalidTokenError as e:
            return None

    def encode(self, payload):
        payload['aud'] = os.getenv('APP_SECURITY_AUDIENCE')

        return jwt.encode(
            payload,
            self.private_key,
            algorithm=self.algorithm
        )
