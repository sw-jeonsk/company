from typing import List, Type

from sqlalchemy.orm import Session

from app import models
from app.models import CompanyName
from app.repositories.company import get_company_by_company_name
from app.repositories.company_name import get_company_names_by_tag_name
from app.repositories.company_tag import create_company_tag, get_company_tag_name_by_company_name, delete_company_tag_by_company_name_company_tag_name
from app.schemas.company_tag import NewTag


def get_search_tag_name_service(query: str, x_wanted_language: str, db: Session) -> list[Type[CompanyName]]:
    company_names = get_company_names_by_tag_name(query, db)
    results = []
    breakpoint()
    for company_name in company_names:
        if company_name.company_id in results:
            continue
        if company_name.country == x_wanted_language:
            results.append(company_name)

    return company_names


def new_tag_service(company_name: str, tags: List[NewTag], db: Session) -> None:
    company = get_company_by_company_name(company_name, db)
    company_tags = get_company_tag_name_by_company_name(company_name, db)
    origin_company_tag_values = [f"{tag.country}|{tag.name}" for tag in company_tags]
    add_company_tag_values = [f"{country}|{name}" for tag in tags for country, name in tag.tag_name.items()]
    add_target_tag_values = list(set(add_company_tag_values) - set(origin_company_tag_values))

    if add_target_tag_values:
        results = []
        for add_target_tag_value in add_target_tag_values:
            country, name = add_target_tag_value.split("|")
            results.append(models.CompanyTag(company_id=company.id, country=country, name=name))
        create_company_tag(results, db)


def delete_tag_service(company_name: str, tag_name: str, db: Session) -> None:
    delete_company_tag_by_company_name_company_tag_name(company_name, tag_name, db)
