from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Ingredient
from app.schemas import IngredientCreate


def get_ingredients(db: Session):
    return db.scalars(select(Ingredient)).all()


def get_ingredient(db: Session, ingredient_id: int):
    return db.get(Ingredient, ingredient_id)


def get_ingredient_by_name(db: Session, name: str):
    return db.scalars(select(Ingredient).where(func.lower(Ingredient.name) == name.lower())).first()


def create_ingredient(db: Session, data: IngredientCreate):
    ingredient = Ingredient(**data.model_dump())
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


def update_ingredient(db: Session, ingredient: Ingredient, data: IngredientCreate):
    ingredient.name = data.name
    db.commit()
    db.refresh(ingredient)
    return ingredient


def delete_ingredient(db: Session, ingredient: Ingredient):
    db.delete(ingredient)
    db.commit()
