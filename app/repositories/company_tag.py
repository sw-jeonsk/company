from typing import List, Type

from sqlalchemy.orm import Session

from app import models
from app.models import CompanyTag


def create_company_tag(company_tags: List[models.CompanyTag], db: Session) -> list[CompanyTag]:
    db.add_all(company_tags)
    db.flush()
    return company_tags


def get_company_tag_name_by_company_name(company_name: str, db: Session) -> List[Type[models.CompanyTag]]:
    return db.query(
        models.CompanyTag
    ).join(
        models.CompanyName, models.CompanyName.company_id == models.CompanyTag.company_id
    ).filter(models.CompanyName.name.__eq__(company_name)).all()


def delete_company_tag_by_company_name_company_tag_name(company_name: str, tag_name: str, db: Session) -> None:
    subquery = db.query(models.Company.id).filter(models.Company.id == models.CompanyName.company_id, models.CompanyName.name.__eq__(company_name)).subquery()
    company_tags = db.query(
        models.CompanyTag
    ).join(
        models.CompanyName, models.CompanyName.company_id == models.CompanyTag.company_id
    ).filter(models.CompanyTag.company_id.in_(subquery), models.CompanyTag.name.__eq__(tag_name)).all()
    for obj in company_tags:
        db.delete(obj)
