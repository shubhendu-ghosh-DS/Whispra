from pydantic import BaseModel

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SendMessageRequest(BaseModel):
    from_username: str
    password: str
    to_username: str
    message: str

class ScanMessagesRequest(BaseModel):
    username: str
    password: str

class SaveFriendRequest(BaseModel):
    username: str
    password: str
    friend_username: str
