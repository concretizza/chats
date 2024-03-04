from pydantic import BaseModel


class UserRequest(BaseModel):
    uuid: str
    account_uuid: str
