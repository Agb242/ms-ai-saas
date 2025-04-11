from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TenantBase(BaseModel):
    name: str
    email: EmailStr

class TenantCreate(TenantBase):
    password: str
    kannel_sid: Optional[str] = None
    kannel_token: Optional[str] = None
    openrouter_key: Optional[str] = None

class Tenant(TenantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class MessageBase(BaseModel):
    text: str
    role: str

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    phone_number: str

class ConversationCreate(ConversationBase):
    tenant_id: int

class Conversation(ConversationBase):
    id: int
    created_at: datetime
    last_active_at: datetime
    messages: list[Message] = []

    class Config:
        from_attributes = True 