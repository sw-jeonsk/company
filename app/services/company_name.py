from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.company_name import get_company_name_by_country, get_company_name_contains_by_country, get_company_name_by_name


def get_company_name_service(company, country, db: Session):
    return get_company_name_by_country(company, country, db)


def get_company_name_autocomplete_service(query, country, db: Session):
    return get_company_name_contains_by_country(query, country, db)


def get_company_search_service(company_name: str, country: str, db: Session):
    if company_name := get_company_name_by_name(company_name, db):
        for company_name in company_name.company.names:
            if company_name.country == country:
                return company_name
    raise HTTPException(status_code=404)
