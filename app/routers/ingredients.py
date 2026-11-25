from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import IngredientCreate, IngredientRead
from app.services import ingredients as service

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.get("/", response_model=list[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return service.get_ingredients(db)


@router.get("/{ingredient_id}", response_model=IngredientRead)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = service.get_ingredient(db, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    return ingredient


@router.post("/", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
def create_ingredient(data: IngredientCreate, db: Session = Depends(get_db)):
    if service.get_ingredient_by_name(db, data.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ingredient already exists")
    return service.create_ingredient(db, data)


@router.put("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(ingredient_id: int, data: IngredientCreate, db: Session = Depends(get_db)):
    ingredient = service.get_ingredient(db, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    other = service.get_ingredient_by_name(db, data.name)
    if other and other.id != ingredient_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ingredient already exists")
    return service.update_ingredient(db, ingredient, data)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = service.get_ingredient(db, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    if ingredient.recipes:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ingredient is used in a recipe")
    service.delete_ingredient(db, ingredient)
