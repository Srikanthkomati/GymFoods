from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth_utils import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = verify_token(token, expected_type="access")
    return user_id
