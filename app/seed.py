from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db import SessionLocal
from app.entities.user_entity import UserEntity
from app.entities.store_entity import StoreEntity
from app.entities.product_entity import ProductEntity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed():
    db: Session = SessionLocal()

    # ==========================
    # USERS
    # ==========================
    admin = db.query(UserEntity).filter_by(email="admin@example.com").first()
    if not admin:
        admin = UserEntity(
            email="admin@example.com",
            password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin)

    seller = db.query(UserEntity).filter_by(email="seller@example.com").first()
    if not seller:
        seller = UserEntity(
            email="seller@example.com",
            password=hash_password("seller123"),
            role="seller"
        )
        db.add(seller)

    user = db.query(UserEntity).filter_by(email="user@example.com").first()
    if not user:
        user = UserEntity(
            email="user@example.com",
            password=hash_password("user123"),
            role="user"
        )
        db.add(user)

    db.commit()

    # Refresh seller (needed for seller.id)
    db.refresh(seller)

    # ==========================
    # STORE
    # ==========================
    store = db.query(StoreEntity).filter_by(name="Main Store").first()
    if not store:
        store = StoreEntity(
            name="Main Store",
            seller_id=seller.id
        )
        db.add(store)
        db.commit()
        db.refresh(store)

    # ==========================
    # PRODUCTS
    # ==========================
    existing_products = db.query(ProductEntity).count()

    if existing_products == 0:
        products = [
            ProductEntity(
                store_id=store.id,
                name=f"Product {i}",
                price=1000 + i * 100,
                stock=10 + i
            )
            for i in range(1, 11)
        ]

        db.add_all(products)
        db.commit()

    db.close()

    print("✅ Seed data inserted successfully!")


if __name__ == "__main__":
    seed()
