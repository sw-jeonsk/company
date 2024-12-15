from sqlalchemy.orm import Session
from app.models import CompanyModel, CompanyNameModel


def create_company(code, db: Session) -> CompanyModel:
    _company = CompanyModel(code=code)
    db.add(_company)
    db.flush()
    return _company


def get_company_by_code(code, db: Session) -> None | CompanyModel:
    return db.query(CompanyModel).filter(CompanyModel.code.__eq__(code)).first()


def get_company_by_company_name(company_name, db: Session) -> None | CompanyModel:
    return db.query(CompanyModel).join(CompanyNameModel, CompanyNameModel.company_id == CompanyModel.id).filter(CompanyNameModel.name.__eq__(company_name)).first()


