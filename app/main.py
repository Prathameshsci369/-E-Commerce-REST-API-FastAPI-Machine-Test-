from typing import List
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler

# Import from local modules
from database import engine, get_db, Base
from models import CategoryModel, ProductModel
from schemas import Category, CategoryBase, Product, ProductBase
# Import both the limiter and the security function
from security import limiter, verify_api_key

# --- APP SETUP ---
app = FastAPI(title="E-Commerce Machine Test")

# ATTACH LIMITER
app.state.limiter = limiter
# Add the handler that returns "429 Too Many Requests" when limit is hit
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Exception Handler for Database Errors
@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Data conflict. This item might already exist."}
    )

# Startup Event
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# --- CATEGORIES ---

@app.get("/api/categories/", response_model=List[Category], tags=["Categories"])
@limiter.limit("20/minute") # Throttling: 20 reads/min
# IMPORTANT: Must include 'request: Request' argument for limiter to work
def read_categories(request: Request, page: int = Query(1, ge=1), limit: int = Query(10, ge=1), db=Depends(get_db)):
    offset = (page - 1) * limit
    return db.query(CategoryModel).offset(offset).limit(limit).all()

@app.post("/api/categories/", response_model=Category, tags=["Categories"])
@limiter.limit("5/minute") # Throttling: 5 writes/min
def create_category(request: Request, category: CategoryBase, db=Depends(get_db), authorized: bool = Depends(verify_api_key)):
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.put("/api/categories/{id}", response_model=Category, tags=["Categories"])
@limiter.limit("5/minute")
def update_category(request: Request, id: int, category: CategoryBase, db=Depends(get_db), authorized: bool = Depends(verify_api_key)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/api/categories/{id}", tags=["Categories"])
@limiter.limit("5/minute")
def delete_category(request: Request, id: int, db=Depends(get_db), authorized: bool = Depends(verify_api_key)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}

# --- PRODUCTS ---

@app.get("/api/products/", response_model=List[Product], tags=["Products"])
@limiter.limit("20/minute")
def read_products(request: Request, page: int = Query(1, ge=1), limit: int = Query(10, ge=1), db=Depends(get_db)):
    offset = (page - 1) * limit
    return db.query(ProductModel).offset(offset).limit(limit).all()

@app.get("/api/products/{id}", response_model=Product, tags=["Products"])
@limiter.limit("20/minute")
def read_product(request: Request, id: int, db=Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/products/", response_model=Product, tags=["Products"])
@limiter.limit("5/minute")
def create_product(request: Request, product: ProductBase, db=Depends(get_db), authorized: bool = Depends(verify_api_key)):
    category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category ID does not exist")
    
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/api/products/{id}", response_model=Product, tags=["Products"])
@limiter.limit("5/minute")
def update_product(request: Request, id: int, product: ProductBase, db=Depends(get_db), authorized: bool = Depends(verify_api_key)):
    db_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category ID does not exist")

    db_product.name = product.name
    db_product.price = product.price
    db_product.category_id = product.category_id
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{id}", tags=["Products"])
@limiter.limit("5/minute")
def delete_product(request: Request, id: int, db=Depends(get_db), authorized: bool = Depends(verify_api_key)):
    db_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}