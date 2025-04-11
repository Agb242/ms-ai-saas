from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from . import models, schemas, auth
from .database import engine, get_db
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from .services.openrouter import OpenRouterService
from .services.kannel import KannelService

# Création des tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMS AI SaaS API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: schemas.TenantBase,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tenants/", response_model=schemas.Tenant)
async def create_tenant(
    tenant: schemas.TenantCreate,
    db: Session = Depends(get_db)
):
    db_tenant = db.query(models.Tenant).filter(models.Tenant.email == tenant.email).first()
    if db_tenant:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(tenant.password)
    db_tenant = models.Tenant(
        name=tenant.name,
        email=tenant.email,
        password_hash=hashed_password,
        kannel_sid=tenant.kannel_sid,
        kannel_token=tenant.kannel_token,
        openrouter_key=tenant.openrouter_key
    )
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@app.get("/tenants/me", response_model=schemas.Tenant)
async def read_tenants_me(current_user: models.Tenant = Depends(get_current_user)):
    return current_user

@app.post("/conversations/", response_model=schemas.Conversation)
async def create_conversation(
    conversation: schemas.ConversationCreate,
    current_user: models.Tenant = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_conversation = models.Conversation(
        tenant_id=current_user.id,
        phone_number=conversation.phone_number
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.get("/conversations/", response_model=List[schemas.Conversation])
async def read_conversations(
    current_user: models.Tenant = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversations = db.query(models.Conversation).filter(
        models.Conversation.tenant_id == current_user.id
    ).all()
    return conversations

@app.post("/sms/inbound")
async def sms_inbound(
    to: str,
    from_: str,
    text: str,
    db: Session = Depends(get_db)
):
    # 1. Identifier le tenant par le numéro "to"
    tenant = db.query(models.Tenant).filter(models.Tenant.phone_number == to).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # 2. Créer/récupérer la conversation
    conversation = db.query(models.Conversation).filter(
        models.Conversation.tenant_id == tenant.id,
        models.Conversation.phone_number == from_
    ).first()

    if not conversation:
        conversation = models.Conversation(
            tenant_id=tenant.id,
            phone_number=from_
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 3. Stocker le message utilisateur
    user_message = models.Message(
        conversation_id=conversation.id,
        role="user",
        text=text
    )
    db.add(user_message)
    db.commit()

    # 4. Récupérer les derniers messages pour le contexte
    last_messages = db.query(models.Message).filter(
        models.Message.conversation_id == conversation.id
    ).order_by(models.Message.created_at.desc()).limit(10).all()

    # 5. Appeler OpenRouter AI
    openrouter = OpenRouterService(api_key=tenant.openrouter_key)
    messages = [
        {"role": msg.role, "content": msg.text}
        for msg in reversed(last_messages)
    ]
    ai_response = await openrouter.generate_response(messages)

    # 6. Stocker la réponse de l'IA
    ai_message = models.Message(
        conversation_id=conversation.id,
        role="assistant",
        text=ai_response
    )
    db.add(ai_message)
    db.commit()

    # 7. Envoyer la réponse via Kannel
    kannel = KannelService(
        username=tenant.kannel_sid,
        password=tenant.kannel_token
    )
    await kannel.send_sms(to=from_, text=ai_response)

    return {"status": "success"} 