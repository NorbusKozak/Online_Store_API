from fastapi import FastAPI, status, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.schemas import UserCreateValidator, UserResponseValidator, ProductValidator, ProductResponseValidator, OrderCreateValidator, OrderResponseValidator, ShowProductsResponseValidator, ShowProductValidator, SearchProductResponseValidator, SearchProductValidator
from app.crud import create_user, add_product, create_order, authenticate_user, get_products, search_products
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import create_access_token, get_current_user
from app.dependencies import get_admin_user
from typing import List
import app.models as models
from app.email_utils import send_activation_email

#import Base from models for sql to know what tables to use
models.Base.metadata.create_all(bind = engine)

#starting an app
app = FastAPI(title="First Online Shop")

# allows backend and fronted to 'talk' with each other
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        
#there were no used try/except block beacuse return of function in crud is either variable or none
# if none then there is no need for handling exception here beacuse it will never execute
@app.post('/register', response_model=UserResponseValidator, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreateValidator, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):
    register = create_user(db=db, user_data=user)

    if not register:
        raise HTTPException(status_code=400, detail="Unable to create account. E-mail might be taken")

    background_tasks.add_task(send_activation_email, register.email, user.name)

    return register

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400,
                            detail="Invalid password or e-mail",
                            headers={"WWW-Authenticate": "Bearer"},)

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}

@app.post('/add_products', response_model=ProductResponseValidator ,status_code=status.HTTP_201_CREATED)
def enter_product(product: ProductValidator, db: Session = Depends(get_db), admin: models.User = Depends(get_admin_user)):
    new_product = add_product(db=db, product_data=product)

    if not new_product:
        raise HTTPException(status_code=400, detail="Unable to add product to database.")

    return new_product

@app.post('/make_order', response_model=OrderResponseValidator, status_code=status.HTTP_201_CREATED)
def order_create(order: OrderCreateValidator, current_user: models.User = Depends(get_current_user) ,db:Session = Depends(get_db)):
    new_order = create_order(db=db, order_data=order, user_id=current_user.id)

    if not new_order:
        raise HTTPException(status_code=400, detail="Unable to create an order.")

    return new_order

@app.get('/show_products', response_model=List[ShowProductsResponseValidator], status_code=status.HTTP_200_OK)
def show_products(prod: ShowProductValidator = Depends(), db: Session = Depends(get_db)):
    products = get_products(db=db, product_data=prod)

    if not products:
        raise HTTPException(status_code=400, detail="Not able to find any of the products under such price.")

    return products

@app.get('/search_products', response_model=List[SearchProductResponseValidator], status_code=status.HTTP_200_OK)
def search_name_products(prod: SearchProductValidator = Depends(), db: Session = Depends(get_db)):
    product = search_products(db=db, search_data=prod)

    if not product:
        raise HTTPException(status_code=400, detail=f"There is no such products as '{prod.name}'.")

    return product