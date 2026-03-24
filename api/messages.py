from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models import User, Message
from schemas import MessageCreate, MessageResponse, MessageUpdate
from core.firebase import verify_token

router = APIRouter(prefix="/api/messages", tags=["messages"])

def get_current_user_id(decoded_token: dict = Depends(verify_token)) -> str:
    return decoded_token.get("uid")

@router.get("/", response_model=List[MessageResponse])
async def get_conversations(
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        (Message.sender_id == uid) | (Message.receiver_id == uid)
    ).order_by(Message.created_at.desc()).all()
    return messages

@router.get("/conversation/{partner_id}", response_model=List[MessageResponse])
async def get_conversation(
    partner_id: str,
    skip: int = 0,
    limit: int = 50,
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        ((Message.sender_id == uid) & (Message.receiver_id == partner_id)) |
        ((Message.sender_id == partner_id) & (Message.receiver_id == uid))
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
    return messages

@router.post("/", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    import uuid
    message = Message(
        id=str(uuid.uuid4()),
        sender_id=uid,
        receiver_id=message_data.receiver_id,
        content=message_data.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    from core.socket import sio
    msg_dict = {
        "id": message.id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "read": message.read,
        "created_at": message.created_at.isoformat()
    }
    
    # We must await sio.emit inside an async route, which we are in
    await sio.emit("new_message", msg_dict, room=message.receiver_id)
    await sio.emit("new_message", msg_dict, room=message.sender_id)
    
    return message

@router.put("/{message_id}/read", response_model=MessageResponse)
async def mark_as_read(
    message_id: str,
    uid: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == uid
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.read = True
    db.commit()
    db.refresh(message)
    return message
