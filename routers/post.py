from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from schemas.post import PostCreate, PostUpdate, PostRead, PostSearchResponse
from schemas.user import UserProfile
from controllers import post
from controllers.auth import get_current_user
from database import get_db
from pydantic import PositiveInt

post_router = APIRouter()

@post_router.post('', response_model=PostRead)
def create_post(post_item: PostCreate, db: Session = Depends(get_db), user: UserProfile = Depends(get_current_user)):
	return post.create(db=db, post=post_item, user=user)

@post_router.get('/{post_id}', response_model=PostRead)
def read_post(post_id: PositiveInt, db: Session = Depends(get_db)):
	return post.read(db=db, post_id=post_id)

@post_router.put('/{post_id}', response_model=PostRead)
def update_post(post_item: PostUpdate, post_id: PositiveInt, db: Session = Depends(get_db), user: UserProfile = Depends(get_current_user)):
	return post.update(db=db, post_id=post_id, post=post_item, user=user)

@post_router.delete('/{post_id}')
def delete_post(post_id: PositiveInt, db: Session = Depends(get_db), user: UserProfile = Depends(get_current_user)):
	return post.delete(db=db, post_id=post_id, user=user)

@post_router.get('', response_model=PostSearchResponse)
def search_post(title: str = None, tags: list[str] = Query(None), db: Session = Depends(get_db)):
	return post.search(db=db, title=title, tags=tags)