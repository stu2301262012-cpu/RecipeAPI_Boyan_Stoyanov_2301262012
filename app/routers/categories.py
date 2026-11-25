from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CategoryCreate, CategoryRead
from app.services import categories as service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return service.get_categories(db)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = service.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    if service.get_category_by_name(db, data.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    return service.create_category(db, data)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = service.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    other = service.get_category_by_name(db, data.name)
    if other and other.id != category_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    return service.update_category(db, category, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = service.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    service.delete_category(db, category)
