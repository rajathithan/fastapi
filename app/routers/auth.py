from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models
from ..database import get_db
from ..schemas import  Token
from ..utils import pass_verify
from ..oauth2 import create_access_token
from datetime import timedelta

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", status_code=status.HTTP_200_OK,response_model=Token)
async def create_user(login_user: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    
    #OAuth2PasswordRequestForm - accepts fields username and password    
    user_info = db.query(models.User).filter(models.User.email == login_user.username).first()   
     
    if not user_info:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not pass_verify(login_user.password,user_info.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    access_token = create_access_token(data={"user_email": user_info.email}, expires_delta=timedelta(15))
    
    return {"access_token": access_token, "token_type": "bearer"}