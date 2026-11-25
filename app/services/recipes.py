from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Recipe, RecipeIngredient
from app.schemas import RecipeCreate, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeRead, RecipeUpdate


def get_recipes(db: Session, title: str | None, category_id: int | None, max_prep_time: int | None):
    query = select(Recipe)
    if title:
        query = query.where(Recipe.title.ilike(f"%{title.strip()}%"))
    if category_id is not None:
        query = query.where(Recipe.category_id == category_id)
    if max_prep_time is not None:
        query = query.where(Recipe.prep_time_minutes <= max_prep_time)
    return db.scalars(query).all()


def scale_recipe(recipe: Recipe, servings: int):
    result = RecipeRead.model_validate(recipe)
    factor = servings / recipe.servings
    result.servings = servings
    for item in result.ingredients:
        item.quantity = round(item.quantity * factor, 2)
    return result


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
