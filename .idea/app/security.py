from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer


SECURITY_KEY = "kjznvaoexnvaodrgnv"
ALGORITHMS = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/token")

class Token(BaseModel):
    access_token: str
    token_type: str