from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
    promotion = Column(String)

    def __repr__(self):
        return "<Item(name={}, description={}, price={}, promotion={}, id={})>".format(
            self.name,
            self.description,
            self.price,
            self.promotion,
            self.id
        )
