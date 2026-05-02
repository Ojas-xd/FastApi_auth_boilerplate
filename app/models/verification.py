from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Enum
from app.database import Base
import enum
from sqlalchemy.sql import func


class TokenType(str,enum.Enum):
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    PASSWORD_RESET = "PASSWORD_RESET"


class EmailVerification(Base):
    __tablename__ = "emailverification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)

    token_type = Column(Enum(TokenType), nullable=False,unique=False)

    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())