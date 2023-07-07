from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models
from ..database import get_db
from ..schemas import PostCreate, PostUpdate, LimitedResponse, UserOut,UserCreate
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    )


@router.get("/", status_code=status.HTTP_200_OK,response_model=List[LimitedResponse])
async def getallposts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM POSTS""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=LimitedResponse)
async def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS where id = %s""",(str(id)))
    # id_post = cursor.fetchone()
    id_post = db.query(models.Post).filter(models.Post.id == id).first()    
    if not id_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return id_post

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createposts(new_post: PostCreate, db: Session = Depends(get_db),
                      user_email: str = Depends (oauth2.get_current_user)):
    print(user_email)
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (new_post.title, new_post.content, new_post.published),
    # )
    # nPost = cursor.fetchone()
    # conn.commit()
    nPost = models.Post(**new_post.dict())
    db.add(nPost)
    db.commit()
    db.refresh(nPost)    
    return nPost

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_post(id: int,db: Session = Depends(get_db),
                   user_email: str = Depends (oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM POSTS where id = %s RETURNING *""",(str(id),))
    # id_post = cursor.fetchone()
    # conn.commit()
    id_post = db.query(models.Post).filter(models.Post.id == id)
    
    if not id_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    else:
        id_post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, post: PostUpdate, db: Session = Depends(get_db),
                   user_email: str = Depends (oauth2.get_current_user)):
    # cursor.execute("""UPDATE POSTS SET TITLE = %s,CONTENT = %s, PUBLISHED = %s WHERE ID = %s RETURNING *""",
    #                (post.title,post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    else:
        updated_post.update(post.dict(),synchronize_session=False)
        db.commit()
        return updated_post.first()