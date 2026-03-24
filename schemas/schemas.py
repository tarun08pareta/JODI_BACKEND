from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = ""
    avatar_url: Optional[str] = ""

class UserCreate(UserBase):
    password: Optional[str] = None # Not used with Firebase, kept for compat

class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str  # Firebase UID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class VerifyResponse(BaseModel):
    user: UserResponse
    profileComplete: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class ProfileBase(BaseModel):
    name: Optional[str] = ""
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = ""
    profession: Optional[str] = ""
    bio: Optional[str] = ""
    avatar_url: Optional[str] = ""
    looking_for: Optional[str] = None
    plan: Optional[str] = "basic"

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    profession: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    looking_for: Optional[str] = None
    plan: Optional[str] = None

class ProfileResponse(ProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GalleryBase(BaseModel):
    image_url: str

class GalleryCreate(GalleryBase):
    pass

class GalleryResponse(GalleryBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    receiver_id: str

class MessageUpdate(BaseModel):
    read: bool = True

class MessageResponse(MessageBase):
    id: str
    sender_id: str
    receiver_id: str
    read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CallSignalBase(BaseModel):
    room_id: str
    receiver_id: str
    type: str
    payload: Optional[dict] = {}

class CallSignalCreate(CallSignalBase):
    pass

class CallSignalResponse(CallSignalBase):
    id: str
    sender_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CallMessageBase(BaseModel):
    room_id: str
    content: str

class CallMessageCreate(CallMessageBase):
    pass

class CallMessageResponse(CallMessageBase):
    id: str
    sender_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
