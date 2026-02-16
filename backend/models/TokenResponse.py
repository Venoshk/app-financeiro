from pydantic import BaseModel

class TokenResponse(BaseModel):
    connectToken: str
    