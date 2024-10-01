from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    photo_url = Column(String)
    category = Column(String)
    vendor_id = Column(String, ForeignKey("vendors.id"))
    vendor = relationship("Vendor", back_populates="products", lazy="subquery")