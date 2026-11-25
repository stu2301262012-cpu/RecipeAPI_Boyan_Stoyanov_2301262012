from fastapi import FastAPI

app = FastAPI(
    title="Recipe Catalog API",
    description="REST API for a catalog of recipes, authors, categories and ingredients.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Recipe Catalog API is running. Open /docs for Swagger UI."}
