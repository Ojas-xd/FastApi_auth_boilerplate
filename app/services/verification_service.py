import secrets
from datetime import datetime,timedelta,timezone
from app.models.verification import EmailVerification,TokenType
from app.models.user import User
from fastapi import HTTPException
def create_verification_token(db, user_id):
    old = db.query(EmailVerification).filter(EmailVerification.user_id == user_id).first()
    if old:
        db.delete(old)
        db.commit()
    
    tokenn = secrets.token_urlsafe(32)
    expiry = datetime.now(timezone.utc) + timedelta(hours=24)
    new_entry = EmailVerification(
        user_id=user_id,
        token=tokenn,
        token_type=TokenType.EMAIL_VERIFICATION,
        expires_at=expiry
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return tokenn

def verify_token(db, token):
    record = db.query(EmailVerification).filter(
        EmailVerification.token == token
    ).first()

    if record is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    if record.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired, try again")

    user = db.query(User).filter(User.id == record.user_id).first()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
 
    user.is_verified = True
    db.delete(record)
    db.commit()

    return {"message": "User verified successfully"}
