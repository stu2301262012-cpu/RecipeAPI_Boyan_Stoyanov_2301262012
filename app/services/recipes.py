from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Recipe
from app.schemas import RecipeCreate, RecipeUpdate


def get_recipes(db: Session):
    return db.scalars(select(Recipe)).all()


def get_recipe(db: Session, recipe_id: int):
    return db.get(Recipe, recipe_id)


def get_recipe_by_title(db: Session, author_id: int, title: str):
    query = select(Recipe).where(Recipe.author_id == author_id, func.lower(Recipe.title) == title.lower())
    return db.scalars(query).first()


def create_recipe(db: Session, data: RecipeCreate):
    recipe = Recipe(**data.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def update_recipe(db: Session, recipe: Recipe, data: RecipeUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(recipe, key, value)
    db.commit()
    db.refresh(recipe)
    return recipe


def delete_recipe(db: Session, recipe: Recipe):
    db.delete(recipe)
    db.commit()
