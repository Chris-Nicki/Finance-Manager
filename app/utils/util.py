import jwt
import os
from datetime import datetime, timedelta, timezone

# Create a secret key constant
SECRET_KEY = os.environ.get('SECRET_KEY') or "I'll Never Tell!"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'user_id': user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        print('Token has expired')
        return None
    except Exception as e:
        print(f"An error has occurred: {e}")
        return None