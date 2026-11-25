from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Recipe, RecipeIngredient
from app.schemas import RecipeCreate, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeUpdate


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


def get_recipes_by_author(db: Session, author_id: int):
    return db.scalars(select(Recipe).where(Recipe.author_id == author_id)).all()


def get_recipe_ingredient(db: Session, recipe_id: int, ingredient_id: int):
    return db.get(RecipeIngredient, (recipe_id, ingredient_id))


def add_ingredient(db: Session, recipe_id: int, data: RecipeIngredientCreate):
    item = RecipeIngredient(recipe_id=recipe_id, **data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_ingredient(db: Session, item: RecipeIngredient, data: RecipeIngredientUpdate):
    item.quantity = data.quantity
    item.unit = data.unit
    db.commit()
    db.refresh(item)
    return item


def remove_ingredient(db: Session, item: RecipeIngredient):
    db.delete(item)
    db.commit()
