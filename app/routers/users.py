from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..schemas import  UserOut,UserCreate
from ..utils import hash_pwd

router = APIRouter(
    prefix="/users",
    tags=["users"],
    )

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=UserOut)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (new_post.title, new_post.content, new_post.published),
    # )
    # nPost = cursor.fetchone()
    # conn.commit()
    new_user.password = hash_pwd(new_user.password)
    nUser = models.User(**new_user.dict())
    db.add(nUser)
    db.commit()
    db.refresh(nUser)    
    return nUser

@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=UserOut)
async def get_post(id: int,db: Session = Depends(get_db)):
    user_id = db.query(models.User).filter(models.User.id == id).first()    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return user_id