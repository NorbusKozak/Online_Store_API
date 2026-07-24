from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from schemas import UserCreateValidator, UserResponseValidator, ProductValidator, ProductResponseValidator, OrderCreateValidator, OrderResponseValidator
from crud import create_user, add_product, create_order, authenticate_user
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dotenv import load_dotenv
import models
import jwt
import os

#import Base from models for sql to know what tables to use
models.Base.metadata.create_all(bind = engine)

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise ValueError("There is no Key in .env!")

#starting an app
app = FastAPI(title="First Online Shop")


def create_access_token(data: dict):
    to_encode = data.copy()
    # Token expires in 30 min
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    #making a token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Cannot verify token. Try to log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        
    except Exception:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
        
#there were no used try/except block beacuse return of function in crud is either variable or none
# if none then there is no need for handling exception here beacuse it will never execute
@app.post('/register', response_model=UserResponseValidator, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreateValidator, db:Session = Depends(get_db)):
    register = create_user(db=db, user_data=user)

    if not register:
        raise HTTPException(status_code=400, detail="Unable to create account. E-mail might be taken")

    return register

@app.post('/products', response_model=ProductResponseValidator ,status_code=status.HTTP_201_CREATED)
def enter_product(product: ProductValidator, db: Session = Depends(get_db)):
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
