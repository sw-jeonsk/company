
from sqlalchemy import Column, func, BIGINT, VARCHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class CompanyModel(Base):
    __tablename__ = 'Company'

    id = Column(BIGINT, primary_key=True)
    code = Column(VARCHAR(128), unique=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    names = relationship("CompanyNameModel", back_populates="company")
    tags = relationship("CompanyTagModel", back_populates="company")


class CompanyNameModel(Base):
    __tablename__ = 'CompanyName'

    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('Company.id'))
    country = Column(VARCHAR(128), nullable=False, index=True)
    name = Column(VARCHAR(128), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    company = relationship("CompanyModel", back_populates="names")


class CompanyTagModel(Base):
    __tablename__ = 'CompanyTag'
    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('Company.id'))
    country = Column(VARCHAR(128), nullable=False, index=True)
    name = Column(VARCHAR(128), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    company = relationship("CompanyModel", back_populates="tags")
