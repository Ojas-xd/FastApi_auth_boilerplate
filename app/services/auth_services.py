from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password, create_token, create_refresh_token,decode_token
def register_user(db, email: str, password: str):
    q = db.query(User).filter(User.email == email).first()
    if q:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    ha = hash_password(password)
    new_user = User(email=email, hashed_password=ha)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db, email: str, password: str):
    q = db.query(User).filter(User.email == email).first()
    
    if not q:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    ver = verify_password(password, q.hashed_password)
    
    if not ver:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_token({"sub": str(q.id)})
    refresh_token = create_refresh_token({"sub": str(q.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
def refresh_access_token(refresh_token: str):
    payload = decode_token(refresh_token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    access_token = create_token({"sub": user_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }