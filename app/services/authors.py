from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate


def get_authors(db: Session):
    return db.scalars(select(Author)).all()


def get_author(db: Session, author_id: int):
    return db.get(Author, author_id)


def get_author_by_email(db: Session, email: str):
    return db.scalars(select(Author).where(func.lower(Author.email) == email.lower())).first()


def create_author(db: Session, data: AuthorCreate):
    author = Author(**data.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update_author(db: Session, author: Author, data: AuthorUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author: Author):
    db.delete(author)
    db.commit()
