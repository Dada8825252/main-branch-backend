from sqlalchemy.orm import Session
from schemas.post import PostCreate, PostUpdate
from models.post import Post

def create(db: Session, post: PostCreate):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def read(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update(db: Session, post_id: int, post: PostUpdate):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    post_data = post.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    db.commit()
    return db_post

def delete(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}