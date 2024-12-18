from typing import List, Type

from sqlalchemy.orm import Session

from app.models import CompanyTagModel
from app.repositories.company import get_company_by_company_name
from app.repositories.company_name import get_company_name_by_tag_name_country
from app.repositories.company_tag import create_company_tag, get_company_tag_name_by_company_name, delete_company_tag_by_company_name_company_tag_name
from app.schemas.company_name import OnlyCompanyNameSchema
from app.schemas.company_tag import NewTagSchema


def get_search_tag_name_service(query: str, x_wanted_language: str, db: Session) -> list[Type[OnlyCompanyNameSchema]]:
    return get_company_name_by_tag_name_country(query, x_wanted_language, db)


def new_tag_service(company_name: str, tags: List[NewTagSchema], db: Session) -> None:
    company = get_company_by_company_name(company_name, db)
    company_tags = get_company_tag_name_by_company_name(company_name, db)
    origin_company_tag_values = [f"{tag.country}|{tag.name}" for tag in company_tags]
    add_company_tag_values = [f"{country}|{name}" for tag in tags for country, name in tag.tag_name.items()]
    add_target_tag_values = list(set(add_company_tag_values) - set(origin_company_tag_values))

    if add_target_tag_values:
        results = []
        for add_target_tag_value in add_target_tag_values:
            country, name = add_target_tag_value.split("|")
            results.append(CompanyTagModel(company_id=company.id, country=country, name=name))
        create_company_tag(results, db)


def delete_tag_service(company_name: str, tag_name: str, db: Session) -> None:
    delete_company_tag_by_company_name_company_tag_name(company_name, tag_name, db)
