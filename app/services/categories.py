from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas import CategoryCreate


def get_categories(db: Session):
    return db.scalars(select(Category)).all()


def get_category(db: Session, category_id: int):
    return db.get(Category, category_id)


def get_category_by_name(db: Session, name: str):
    return db.scalars(select(Category).where(func.lower(Category.name) == name.lower())).first()


def create_category(db: Session, data: CategoryCreate):
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category: Category, data: CategoryCreate):
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()
