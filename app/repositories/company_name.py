from typing import List, Dict, Type

from sqlalchemy import case
from sqlalchemy.orm import Session, aliased

from app.models import CompanyNameModel, CompanyModel, CompanyTagModel
from app.schemas.company_name import OnlyCompanyNameSchema


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


def get_company_by_tag_name(name, db: Session) -> list[Type[CompanyNameModel]]:
    data = db.query(
        CompanyNameModel
    ).outerjoin(
        CompanyTagModel, CompanyTagModel.company_id == CompanyNameModel.company_id
    ).filter(
        CompanyTagModel.name == name,
    )
    return data.all()


def get_company_name_by_tag_name_country(name, country, db: Session):

    country_name = aliased(CompanyNameModel)
    no_country_name = aliased(CompanyNameModel)

    company_name_case = case(
(country_name.country == country, country_name.name),
        else_=no_country_name.name
    )
    query = db.query(
        CompanyModel.id.label("company_id"), company_name_case.label("company_name")
    ).outerjoin(
        country_name, (country_name.company_id == CompanyModel.id) & (country_name.country == country)
    ).outerjoin(
        no_country_name, no_country_name.company_id == CompanyModel.id
    ).outerjoin(
        CompanyTagModel, CompanyTagModel.company_id == CompanyModel.id
    ).filter(
        CompanyTagModel.name == name,
    ).group_by(CompanyModel.id,  "company_name")
    return [OnlyCompanyNameSchema(name=row[1]) for row in query.all()]
