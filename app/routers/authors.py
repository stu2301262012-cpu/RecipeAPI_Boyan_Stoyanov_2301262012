from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AuthorCreate, AuthorRead, AuthorUpdate, RecipeRead
from app.services import authors as service
from app.services import recipes as recipes_service

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=list[AuthorRead])
def list_authors(db: Session = Depends(get_db)):
    return service.get_authors(db)


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = service.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    if service.get_author_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return service.create_author(db, data)


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, data: AuthorUpdate, db: Session = Depends(get_db)):
    author = service.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    if data.email is not None:
        other = service.get_author_by_email(db, data.email)
        if other and other.id != author_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return service.update_author(db, author, data)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = service.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    if author.recipes:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author has recipes")
    service.delete_author(db, author)


@router.get("/{author_id}/recipes", response_model=list[RecipeRead])
def list_author_recipes(author_id: int, db: Session = Depends(get_db)):
    if service.get_author(db, author_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return recipes_service.get_recipes_by_author(db, author_id)
