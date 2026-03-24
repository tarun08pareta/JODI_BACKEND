from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import json

from db.database import get_db
from models import User, CallSignal, CallMessage
from schemas import CallSignalCreate, CallSignalResponse, CallMessageCreate, CallMessageResponse
from core.security import get_current_user

router = APIRouter(prefix="/api/calls", tags=["calls"])

@router.get("/signals", response_model=List[CallSignalResponse])
async def get_signals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    signals = db.query(CallSignal).filter(
        (CallSignal.sender_id == current_user.id) | (CallSignal.receiver_id == current_user.id)
    ).order_by(CallSignal.created_at.desc()).limit(50).all()
    
    result = []
    for signal in signals:
        signal_dict = {
            "id": signal.id,
            "room_id": signal.room_id,
            "sender_id": signal.sender_id,
            "receiver_id": signal.receiver_id,
            "type": signal.type,
            "payload": json.loads(signal.payload) if signal.payload else {},
            "created_at": signal.created_at
        }
        result.append(signal_dict)
    return result

@router.post("/signals", response_model=CallSignalResponse)
async def send_signal(
    signal_data: CallSignalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import uuid4
    signal = CallSignal(
        id=uuid4(),
        room_id=signal_data.room_id,
        sender_id=current_user.id,
        receiver_id=signal_data.receiver_id,
        type=signal_data.type,
        payload=json.dumps(signal_data.payload)
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    
    return {
        "id": signal.id,
        "room_id": signal.room_id,
        "sender_id": signal.sender_id,
        "receiver_id": signal.receiver_id,
        "type": signal.type,
        "payload": json.loads(signal.payload),
        "created_at": signal.created_at
    }

@router.delete("/signals/{room_id}")
async def delete_signals(
    room_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(CallSignal).filter(
        CallSignal.room_id == room_id,
        (CallSignal.sender_id == current_user.id) | (CallSignal.receiver_id == current_user.id)
    ).delete()
    db.commit()
    return {"message": "Signals deleted"}

@router.get("/messages/{room_id}", response_model=List[CallMessageResponse])
async def get_call_messages(
    room_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(CallMessage).filter(
        CallMessage.room_id == room_id
    ).order_by(CallMessage.created_at.asc()).all()
    return messages

@router.post("/messages", response_model=CallMessageResponse)
async def send_call_message(
    message_data: CallMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import uuid4
    message = CallMessage(
        id=uuid4(),
        room_id=message_data.room_id,
        sender_id=current_user.id,
        content=message_data.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
