from fastapi import HTTPException, Depends
from app.core.security import decode_token, oauth2_scheme
from app.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    resu = decode_token(token)
    if resu is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = resu.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user