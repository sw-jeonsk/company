from typing import List, Type
from sqlalchemy.orm import Session

from app.models import CompanyTagModel, CompanyNameModel, CompanyModel


def create_company_tag(company_tags: List[CompanyTagModel], db: Session) -> list[CompanyTagModel]:
    db.add_all(company_tags)
    db.flush()
    return company_tags


def get_company_tag_name_by_company_name(company_name: str, db: Session) -> List[Type[CompanyTagModel]]:
    return db.query(
        CompanyTagModel
    ).join(
        CompanyNameModel, CompanyNameModel.company_id == CompanyTagModel.company_id
    ).filter(CompanyNameModel.name.__eq__(company_name)).all()


def delete_company_tag_by_company_name_company_tag_name(company_name: str, tag_name: str, db: Session) -> None:
    subquery = db.query(CompanyModel.id).filter(CompanyModel.id == CompanyNameModel.company_id, CompanyNameModel.name.__eq__(company_name)).subquery()
    company_tags = db.query(
        CompanyTagModel
    ).join(
        CompanyNameModel, CompanyNameModel.company_id == CompanyTagModel.company_id
    ).filter(CompanyTagModel.company_id.in_(subquery), CompanyTagModel.name.__eq__(tag_name)).all()
    for obj in company_tags:
        db.delete(obj)
