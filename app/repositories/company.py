
from sqlalchemy.orm import Session
from app import models


def create_company(code, db: Session) -> models.Company:
    _company = models.Company(code=code)
    db.add(_company)
    db.flush()
    return _company


def get_company_by_code(code, db: Session) -> None | models.Company:
    return db.query(models.Company).filter(models.Company.code.__eq__(code)).first()


def get_company_by_company_name(company_name, db: Session) -> None | models.Company:
    return db.query(models.Company).join(models.CompanyName, models.CompanyName.company_id == models.Company.id).filter(models.CompanyName.name.__eq__(company_name)).first()
