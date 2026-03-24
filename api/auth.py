from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from db.database import get_db
from models import User, Profile
from schemas import UserResponse, ProfileResponse, VerifyResponse
from core.firebase import verify_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/verify", response_model=VerifyResponse)
async def verify_auth(decoded_token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    name = decoded_token.get("name", "")
    picture = decoded_token.get("picture", "")

    if not uid or not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token data")

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        user = User(
            id=uid,
            email=email,
            full_name=name,
            avatar_url=picture
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    profile = db.query(Profile).filter(Profile.user_id == uid).first()
    
    return {
        "user": user,
        "profileComplete": profile is not None
    }

@router.get("/me", response_model=UserResponse)
async def get_me(decoded_token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    uid = decoded_token.get("uid")
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
