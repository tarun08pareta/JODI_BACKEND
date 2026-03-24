from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os

from db.database import engine, Base
from core.firebase import init_firebase
from core.socket import sio
from api.auth import router as auth_router
from api.profiles import router as profiles_router
from api.messages import router as messages_router

app = FastAPI(
    title="Stellar Spark Match API",
    description="Backend API for Stellar Spark Match dating application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000", 
        "http://localhost:8080", 
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profiles_router)
app.include_router(messages_router)

# Socket.IO event handlers
@sio.event
async def connect(sid, environ, auth):
    print(f"🔌 Socket connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"🔌 Socket disconnected: {sid}")

@sio.event
async def join(sid, user_id):
    if user_id:
        print(f"User {user_id} joined room {user_id}")
        sio.enter_room(sid, user_id)

@sio.event
async def typing(sid, data):
    sender_id = data.get("senderId")
    receiver_id = data.get("receiverId")
    if receiver_id and sender_id:
        await sio.emit("user_typing", {"senderId": sender_id}, room=receiver_id)

@sio.event
async def stop_typing(sid, data):
    sender_id = data.get("senderId")
    receiver_id = data.get("receiverId")
    if receiver_id and sender_id:
        await sio.emit("user_stop_typing", {"senderId": sender_id}, room=receiver_id)

# Wrap FastAPI with ASGI Socket.IO app
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

@app.on_event("startup")
async def startup_event():
    # Initialize DB tables
    Base.metadata.create_all(bind=engine)
    # Initialize Firebase Admin SDK
    init_firebase()

@app.get("/")
async def root():
    return {"message": "Stellar Spark Match API (Python)", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
