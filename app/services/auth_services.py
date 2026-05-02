from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password, create_token, create_refresh_token,decode_token
from app.services.verification_service import create_verification_token
from app.services.mail import send_verification_email
from app.models.verification import EmailVerification
from datetime import datetime,timezone
def register_user(db, email: str, password: str):
    q = db.query(User).filter(User.email == email).first()
    if q:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    ha = hash_password(password)
    new_user = User(email=email, hashed_password=ha,is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    tokenn=create_verification_token(db,new_user.id)
    send_verification_email.delay(tokenn,email)
    return new_user

def login_user(db, email: str, password: str):
    q = db.query(User).filter(User.email == email).first()
    
    if not q:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    ver = verify_password(password, q.hashed_password)
    
    if not ver:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if q.is_verified==False:
        a=db.query(EmailVerification).filter(EmailVerification.user_id==q.id).first()
        if a.expires_at< datetime.now():
            tokenn=create_verification_token(db,a.user_id)
            send_verification_email.delay(tokenn,email)
        else:
            send_verification_email.delay(a.token,email)
        
        raise HTTPException(status_code=403, detail="Email not verified please check you inbox and verify again")
    
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