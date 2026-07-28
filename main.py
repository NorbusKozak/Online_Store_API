from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from schemas import UserCreateValidator, UserResponseValidator, ProductValidator, ProductResponseValidator, OrderCreateValidator, OrderResponseValidator, ShowProductsResponseValidator, ShowProductValidator
from crud import create_user, add_product, create_order, authenticate_user, get_products
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import create_access_token, get_current_user
from dependencies import get_admin_user
from typing import List
import models

#import Base from models for sql to know what tables to use
models.Base.metadata.create_all(bind = engine)

#starting an app
app = FastAPI(title="First Online Shop")
        
#there were no used try/except block beacuse return of function in crud is either variable or none
# if none then there is no need for handling exception here beacuse it will never execute
@app.post('/register', response_model=UserResponseValidator, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreateValidator, db:Session = Depends(get_db)):
    register = create_user(db=db, user_data=user)

    if not register:
        raise HTTPException(status_code=400, detail="Unable to create account. E-mail might be taken")

    return register

@app.post('/products', response_model=ProductResponseValidator ,status_code=status.HTTP_201_CREATED)
def enter_product(product: ProductValidator, db: Session = Depends(get_db), admin: models.User = Depends(get_admin_user)):
    new_product = add_product(db=db, product_data=product)

    if not new_product:
        raise HTTPException(status_code=400, detail="Unable to add product to database.")

    return new_product

@app.post('/orders', response_model=OrderResponseValidator, status_code=status.HTTP_201_CREATED)
def order_create(order: OrderCreateValidator, current_user: models.User = Depends(get_current_user) ,db:Session = Depends(get_db)):
    new_order = create_order(db=db, order_data=order, user_id=current_user.id)

    if not new_order:
        raise HTTPException(status_code=400, detail="Unable to create an order.")

    return new_order

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400,
                            detail="Invalid password or e-mail",
                            headers={"WWW-Authenticate": "Bearer"},)

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/show_products', response_model=List[ShowProductsResponseValidator], status_code=status.HTTP_200_OK)
def show_products(prod: ShowProductValidator = Depends(), db: Session = Depends(get_db)):
    products = get_products(db=db, product_data=prod)

    if not products:
        raise HTTPException(status_code=400, detail="Not able to find any of the products under such price.")

    return products