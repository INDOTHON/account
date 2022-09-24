from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.utils.translation import gettext as _

import jwt
from datetime import datetime, timedelta

from django.conf import settings
from .models import User

secret = settings.SECRET_KEY
alg = settings.JWT_ALGORITM

def jwt_encode(payload):
    exp = datetime.utcnow() + timedelta(seconds=100)
    payload['exp'] = exp
    token = jwt.encode(payload, secret, algorithm=alg)
    return token

def jwt_decode(token):
    try:
        data = jwt.decode(token, secret, algorithms=[alg])
    except jwt.exceptions.ExpiredSignatureError:
        msg = _('Signature has expired.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.exceptions.DecodeError:
        msg = _('Error decoding signature.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.exceptions.InvalidTokenError:
        raise exceptions.AuthenticationFailed()
    return data

def get_token(request):
    token = request.COOKIES.get('Bearer')
    return token

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = get_token(request)
        if token is None:
            return None
        payload = jwt_decode(token)
        user = self.instance_user(payload)
        return user, token

    def authenticate_header(self, request):
        return 'Bearer'

    def instance_user(self, payload):
        user = User(
            uuid=payload['uuid'],
            email=payload['email']
        )
        return user
