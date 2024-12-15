from typing import List, Dict, Type
from sqlalchemy.orm import Session
from app import models
from app.models import CompanyName, CompanyTag


def create_company_names(company_id: int, company_name: Dict, db: Session) -> List[models.CompanyName]:
    _company_names = [models.CompanyName(company_id=company_id, country=country, name=name) for country, name in company_name.items()]
    db.add_all(_company_names)
    db.flush()
    return _company_names


def get_company_name_by_country(company: models.Company, country: str, db: Session) -> None | models.CompanyName:
    return db.query(models.CompanyName).filter(models.Company.id.__eq__(company.id), models.CompanyName.country.__eq__(country)).first()


def get_company_name_by_name(name, db: Session) -> None | models.CompanyName:
    return db.query(models.CompanyName).filter(models.CompanyName.name.__eq__(name)).first()


def get_company_name_contains_by_country(query, country, db: Session) -> list[Type[CompanyName]]:
    return db.query(models.CompanyName).filter(models.CompanyName.name.ilike(f'%{query}%'), models.CompanyName.country.__eq__(country)).all()


def get_company_names_by_tag_name(name, db: Session) -> list[Type[CompanyName]]:
    return db.query(
        models.CompanyName
    ).outerjoin(
        models.Company, models.CompanyName.company_id == models.Company.id
    ).outerjoin(
        models.CompanyTag, models.CompanyTag.company_id == models.Company.id
    ).filter(
        CompanyTag.name == name,
    ).order_by(models.CompanyName.company_id.asc()).all()
