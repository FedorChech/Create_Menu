from sqlalchemy import create_engine, MetaData, Column, Integer, Table, Text, Connection, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///db.db")
connection = engine.connect()

metadata = MetaData()

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    __tableargs__ = {
        'comment': 'Продукты'
    }

    id = Column(Integer, primary_key=True)
    ProductName = Column(Text)
    Calories = Column(Integer)
    dishes = relationship("DishProduct", back_populates="product", passive_deletes=True)


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    DishName = Column(Text)

    # Определите отношение с таблицей DishProduct
    products = relationship("DishProduct", back_populates="dish", cascade="all, delete-orphan")


class DishProduct(Base):
    __tablename__ = 'dish_product'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey("dish.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    gramm = Column(Integer, default=0)

    # Определите отношение с таблицей Dish
    dish = relationship("Dish", back_populates="products")

    # Определите отношение с таблицей Product
    product = relationship("Product", back_populates="dishes")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
