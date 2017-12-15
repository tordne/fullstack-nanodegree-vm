import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    menu_items = relationship(
        "MenuItem",
        order_by="MenuItem.course",
        back_populates="restaurant")

    def __repr__(self):
        return "<Restaurant(id='%s', name='%s')>" % (
            self.id, self.name)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship("Restaurant", back_populates="menu_items")

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }

    def __repr__(self):
        return "<MenuItem(id='%s', name='%s', price='%s', course='%s', )>" % (
            self.id, self.name, self.price, self.course)


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
