from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import Unit


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class IngredientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    instructions: str = Field(min_length=1)
    prep_time_minutes: int = Field(gt=0)
    servings: int = Field(gt=0)
    author_id: int
    category_id: int | None = None


class RecipeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    instructions: str | None = Field(default=None, min_length=1)
    prep_time_minutes: int | None = Field(default=None, gt=0)
    servings: int | None = Field(default=None, gt=0)
    category_id: int | None = None


class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    quantity: float = Field(gt=0)
    unit: Unit


class RecipeIngredientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ingredient_id: int
    quantity: float
    unit: Unit
    ingredient: IngredientRead


class RecipeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    instructions: str
    prep_time_minutes: int
    servings: int
    author_id: int
    category_id: int | None
    ingredients: list[RecipeIngredientRead] = []
