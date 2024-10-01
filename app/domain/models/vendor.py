from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(String, primary_key=True, index=True)
    brand_name = Column(String, index=True)
    brand_logo = Column(String)
    products = relationship("Product", back_populates="vendor", lazy="subquery")
