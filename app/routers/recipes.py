from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import RecipeCreate, RecipeRead, RecipeUpdate
from app.services import authors as authors_service
from app.services import categories as categories_service
from app.services import recipes as service

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=list[RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    return service.get_recipes(db)


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = service.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


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
