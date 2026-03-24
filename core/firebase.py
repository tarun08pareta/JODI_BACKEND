import os
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

_firebase_initialized = False
_firebase_auth = None

def init_firebase():
    global _firebase_initialized, _firebase_auth
    if _firebase_initialized:
        return _firebase_auth is not None
    
    try:
        import firebase_admin
        from firebase_admin import credentials, auth
        
        if not firebase_admin._apps:
            from dotenv import load_dotenv
            load_dotenv()
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if cred_path:
                # Ensure path is absolute relative to python directory
                if not os.path.isabs(cred_path):
                    import pathlib
                    base_dir = pathlib.Path(__file__).parent.parent
                    cred_path = os.path.join(base_dir, cred_path.replace('./', ''))
                
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                else:
                    raise ValueError(f"Credentials not found at {cred_path}")
            else:
                firebase_admin.initialize_app(options={'projectId': 'jodi-ai-app'})
        
        _firebase_auth = auth
        _firebase_initialized = True
        return True
    except Exception as e:
        print(f"Firebase init warning: {e}")
        _firebase_initialized = True
        _firebase_auth = None
        return False

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        if not init_firebase():
            raise HTTPException(status_code=401, detail="Firebase not configured")
        
        decoded_token = _firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid auth credentials: {type(e).__name__}: {e}")
