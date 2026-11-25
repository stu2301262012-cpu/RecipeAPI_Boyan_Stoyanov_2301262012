from fastapi import FastAPI

from app.routers import authors, categories

app = FastAPI(title="Recipe Catalog API")

app.include_router(authors.router)
app.include_router(categories.router)
