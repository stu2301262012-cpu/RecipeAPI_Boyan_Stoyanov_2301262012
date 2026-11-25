from fastapi import FastAPI

from app.routers import authors, categories, ingredients, recipes

app = FastAPI(title="Recipe Catalog API")

app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)
