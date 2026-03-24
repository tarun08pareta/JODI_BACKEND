from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models import User, Profile
from schemas import ProfileResponse, ProfileUpdate, ProfileCreate
from core.firebase import verify_token

router = APIRouter(prefix="/api/profiles", tags=["profiles"])

def get_current_user_id(decoded_token: dict = Depends(verify_token)) -> str:
    return decoded_token.get("uid")

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile_data: ProfileCreate,
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    existing = db.query(Profile).filter(Profile.user_id == uid).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    import uuid
    profile = Profile(
        id=str(uuid.uuid4()),
        user_id=uid,
        **profile_data.model_dump(exclude_unset=True)
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model=List[ProfileResponse])
async def get_profiles(
    skip: int = 0,
    limit: int = 20,
    gender: str = None,
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    query = db.query(Profile).filter(Profile.user_id != uid)
    if gender:
        query = query.filter(Profile.gender == gender)
    profiles = query.offset(skip).limit(limit).all()
    return profiles

@router.get("/me", response_model=ProfileResponse)
@router.get("/me/profile", response_model=ProfileResponse)
async def get_my_profile(uid: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == uid).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile(user_id: str, uid: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/me", response_model=ProfileResponse)
@router.put("/me/profile", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == uid).first()
    update_data = profile_data.model_dump(exclude_unset=True)
    
    if not profile:
        import uuid
        profile = Profile(
            id=str(uuid.uuid4()),
            user_id=uid,
            **update_data
        )
        db.add(profile)
    else:
        for key, value in update_data.items():
            setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile
