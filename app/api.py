from fastapi import APIRouter, HTTPException
from .models import SignupRequest, LoginRequest, SendMessageRequest, ScanMessagesRequest
from .crud import (
    get_user_by_username,
    create_user,
    verify_user_credentials,
    send_message,
    get_and_delete_messages,
    save_friend_username,
    get_all_friends
)

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Messaging App API is running"}

@router.post("/signup")
def signup(request: SignupRequest):
    if get_user_by_username(request.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    create_user(request.username, request.email, request.password)
    return {
        "message": f"User '{request.username}' registered successfully. Activation pending."
    }

@router.post("/login")
def login(request: LoginRequest):
    user = verify_user_credentials(request.username, request.password)
    
    if not user:
        return {"success": False, "detail": "Invalid username or password"}
    
    if not user.get("active", False):
        return {"success": False, "detail": "User is not active. Please contact admin."}

    return {"success": True, "detail": "Login successful"}

@router.post("/send_message")
def send_message_route(request: SendMessageRequest):
    user = verify_user_credentials(request.from_username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User is not active. Cannot send messages.")
    
    send_message(request.from_username, request.to_username, request.message)

    return {"message": "Message sent successfully"}

@router.post("/scan_messages")
def scan_messages(request: ScanMessagesRequest):
    user = verify_user_credentials(request.username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User is not active. Cannot scan messages.")
    
    messages = get_and_delete_messages(request.username)

    return {"messages": messages}


@router.post("/save_friends")
def save_friends_username(request: SaveFriendRequest):
    user = verify_user_credentials(request.username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User is not active. Cannot save friend username.")
    
    save_friend_username(request.username, request.friend_username)

    return {"message": "friend username saved successfully"}


@router.get("/get_friends", response_model=List[str])
def get_friends(username: str, password: str):
    # Verify the user credentials
    user = verify_user_credentials(username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User is not active. Cannot retrieve friends.")
    
    # Get all friends for the user
    friends_list = get_all_friends(username)

    return friends_list
