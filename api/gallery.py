from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from db.database import get_db
from models import User, Gallery
from schemas import GalleryCreate, GalleryResponse
from core.security import get_current_user

router = APIRouter(prefix="/api/gallery", tags=["gallery"])

@router.get("/", response_model=List[GalleryResponse])
async def get_gallery(
    user_id: UUID,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    gallery = db.query(Gallery).filter(Gallery.user_id == user_id).offset(skip).limit(limit).all()
    return gallery

@router.post("/", response_model=GalleryResponse)
async def add_to_gallery(
    gallery_data: GalleryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gallery = Gallery(
        user_id=current_user.id,
        image_url=gallery_data.image_url
    )
    db.add(gallery)
    db.commit()
    db.refresh(gallery)
    return gallery

@router.delete("/{gallery_id}")
async def delete_from_gallery(
    gallery_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gallery = db.query(Gallery).filter(
        Gallery.id == gallery_id,
        Gallery.user_id == current_user.id
    ).first()
    
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    
    db.delete(gallery)
    db.commit()
    return {"message": "Gallery item deleted"}
