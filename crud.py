from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User, Product, Order, OrderItem
from schemas import UserCreateValidator, ProductValidator, ItemAddToCartValidator, OrderCreateValidator, ShowProductValidator

#encryption of a password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def create_user(db: Session, user_data: UserCreateValidator):
    try:
        encrypted_password = pwd_context.hash(user_data.password) 

        new_user = User(email = user_data.email,
                        hashed_password = encrypted_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        db.rollback()
        print(f"Error with creating new user, {e}")
        return None

def add_product(db: Session, product_data: ProductValidator):
    try:
        new_product = Product(**product_data.model_dump())

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    except Exception as e:
        db.rollback()
        print(f"Error with adding a new product, {e}")
        return None

def create_order(db:Session, order_data: OrderCreateValidator, user_id: int):
    try:
        new_order = Order(user_id = user_id, total_price = 0.0)
        db.add(new_order)
        db.flush()
        calculated_price = 0.0

        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()

            if not product:
                raise Exception(f"Product with id {item.product_id} does not exist.")

            calculated_price += product.price * item.quantity

            order_item = OrderItem(
                order_id = new_order.id,
                product_id = item.product_id,
                name = product.name,
                quantity = item.quantity
            )

            db.add(order_item)

        product.stock -= item.quantity
        
        new_order.total_price = calculated_price
        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception as e:
        db.rollback()
        print(f"Error with creating a order: {e}")
        return None

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not pwd_context.verify(password, user.hashed_password):
        return None
    
    return user
#searching for the product
def get_products(db: Session, product_data: ShowProductValidator):

    if product_data.max_price is not None:
        product = db.query(Product).filter(Product.price <= product_data.max_price)

    return product.offset(product_data.skip).limit(product_data.limit).all()