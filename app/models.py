
from sqlalchemy import Column, func, BIGINT, VARCHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Company(Base):
    __tablename__ = 'Company'

    id = Column(BIGINT, primary_key=True)
    code = Column(VARCHAR(128), unique=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    names = relationship("CompanyName", back_populates="company")
    tags = relationship("CompanyTag", back_populates="company")


class CompanyName(Base):
    __tablename__ = 'CompanyName'

    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('Company.id'))
    country = Column(VARCHAR(128), nullable=False, index=True)
    name = Column(VARCHAR(128), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    company = relationship("Company", back_populates="names")


class CompanyTag(Base):
    __tablename__ = 'CompanyTag'
    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('Company.id'))
    country = Column(VARCHAR(128), nullable=False, index=True)
    name = Column(VARCHAR(128), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    company = relationship("Company", back_populates="tags")
