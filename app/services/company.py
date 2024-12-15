from sqlalchemy.orm import Session

from app.models import CompanyModel, CompanyTagModel
from app.schemas.company import CreateCompanySchema
from app.repositories.company import create_company
from app.repositories.company_name import create_company_names
from app.repositories.company_tag import create_company_tag


def create_company_service(company: CreateCompanySchema, db: Session) -> CompanyModel:
    with db.begin():
        # company 추가
        _company = create_company(company.code, db=db)
        # company name 추가
        create_company_names(company_id=_company.id, company_name=company.company_name, db=db)
        company_tags = []
        for tags in company.tags:
            for country, _name in tags.get("tag_name").items():
                company_tags.append(
                    CompanyTagModel(company_id=_company.id, country=country, name=_name)
                )
        # company tag 추가
        create_company_tag(company_tags=company_tags, db=db)
    return _company
