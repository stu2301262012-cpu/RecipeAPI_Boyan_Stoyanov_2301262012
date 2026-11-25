from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    RecipeCreate,
    RecipeIngredientCreate,
    RecipeIngredientRead,
    RecipeIngredientUpdate,
    RecipeRead,
    RecipeUpdate,
)
from app.services import authors as authors_service
from app.services import categories as categories_service
from app.services import ingredients as ingredients_service
from app.services import recipes as service

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=list[RecipeRead])
def list_recipes(
    title: str | None = None,
    category_id: int | None = None,
    max_prep_time: int | None = None,
    db: Session = Depends(get_db),
):
    return service.get_recipes(db, title, category_id, max_prep_time)


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = service.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.get("/{recipe_id}/scaled", response_model=RecipeRead)
def get_scaled_recipe(recipe_id: int, servings: int = Query(gt=0, le=62), db: Session = Depends(get_db)):
    recipe = service.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return service.scale_recipe(recipe, servings)


@router.post("/", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
def create_recipe(data: RecipeCreate, db: Session = Depends(get_db)):
    if authors_service.get_author(db, data.author_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    if data.category_id is not None and categories_service.get_category(db, data.category_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    if service.get_recipe_by_title(db, data.author_id, data.title):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author already has a recipe with this title")
    return service.create_recipe(db, data)


@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(recipe_id: int, data: RecipeUpdate, db: Session = Depends(get_db)):
    recipe = service.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    if data.category_id is not None and categories_service.get_category(db, data.category_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    if data.title is not None:
        other = service.get_recipe_by_title(db, recipe.author_id, data.title)
        if other and other.id != recipe_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author already has a recipe with this title")
    return service.update_recipe(db, recipe, data)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = service.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    service.delete_recipe(db, recipe)


@router.get("/{recipe_id}/ingredients", response_model=list[RecipeIngredientRead])
def list_recipe_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    recipe = service.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe.ingredients


@router.post("/{recipe_id}/ingredients", response_model=RecipeIngredientRead, status_code=status.HTTP_201_CREATED)
def add_recipe_ingredient(recipe_id: int, data: RecipeIngredientCreate, db: Session = Depends(get_db)):
    if service.get_recipe(db, recipe_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    if ingredients_service.get_ingredient(db, data.ingredient_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    if service.get_recipe_ingredient(db, recipe_id, data.ingredient_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ingredient already in recipe")
    return service.add_ingredient(db, recipe_id, data)


@router.put("/{recipe_id}/ingredients/{ingredient_id}", response_model=RecipeIngredientRead)
def update_recipe_ingredient(
    recipe_id: int, ingredient_id: int, data: RecipeIngredientUpdate, db: Session = Depends(get_db)
):
    item = service.get_recipe_ingredient(db, recipe_id, ingredient_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not in recipe")
    return service.update_ingredient(db, item, data)


@router.delete("/{recipe_id}/ingredients/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_recipe_ingredient(recipe_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    item = service.get_recipe_ingredient(db, recipe_id, ingredient_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not in recipe")
    service.remove_ingredient(db, item)
