from typing import List, Dict, Type
from sqlalchemy.orm import Session
from app.models import CompanyNameModel, CompanyModel, CompanyTagModel


def create_company_names(company_id: int, company_name: Dict, db: Session) -> List[CompanyNameModel]:
    _company_names = [CompanyNameModel(company_id=company_id, country=country, name=name) for country, name in company_name.items()]
    db.add_all(_company_names)
    db.flush()
    return _company_names


def get_company_name_by_country(company: CompanyModel, country: str, db: Session) -> None | CompanyNameModel:
    return db.query(CompanyNameModel).filter(CompanyModel.id.__eq__(company.id), CompanyNameModel.country.__eq__(country)).first()


def get_company_name_by_name(name, db: Session) -> None | CompanyNameModel:
    return db.query(CompanyNameModel).filter(CompanyNameModel.name.__eq__(name)).first()


def get_company_name_contains_by_country(query, country, db: Session) -> list[Type[CompanyNameModel]]:
    return db.query(CompanyNameModel).filter(CompanyNameModel.name.ilike(f'%{query}%'), CompanyNameModel.country.__eq__(country)).all()


def get_company_names_by_tag_name(name, db: Session) -> list[Type[CompanyNameModel]]:
    return db.query(
        CompanyNameModel
    ).outerjoin(
        CompanyModel, CompanyNameModel.company_id == CompanyModel.id
    ).outerjoin(
        CompanyTagModel, CompanyTagModel.company_id == CompanyModel.id
    ).filter(
        CompanyTagModel.name == name,
    ).order_by(CompanyNameModel.company_id.asc()).all()
