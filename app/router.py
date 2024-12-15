from typing import List

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.schemas.company import CreateCompanySchema
from app.schemas.company_name import CompanyNameSchema, OnlyCompanyNameSchema
from app.schemas.company_tag import NewTagSchema
from app.services.company import create_company_service
from app.services.company_name import get_company_name_service, get_company_name_autocomplete_service, get_company_search_service
from app.services.company_tag import get_search_tag_name_service, new_tag_service, delete_tag_service
from db.database import get_db
from db.decorator import transactional

router = APIRouter(
    prefix="",
)


@router.get("/search", response_model=List[OnlyCompanyNameSchema])
def company_name_autocomplete(query, x_wanted_language: str = Header(...), db: Session = Depends(get_db)):
    """
    1. 회사명 자동완성
    회사명의 일부만 들어가도 검색이 되어야 합니다.
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    return get_company_name_autocomplete_service(query, x_wanted_language, db)


@router.get("/companies/{company_name}", response_model=CompanyNameSchema)
def company_search(company_name: str, x_wanted_language: str = Header(...), db: Session = Depends(get_db)):
    """
    2. 회사 이름으로 회사 검색
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    company_name = get_company_search_service(company_name, x_wanted_language, db)
    return CompanyNameSchema.from_orm_with_tag_names(x_wanted_language, company_name)


@transactional
@router.post("/companies", response_model=CompanyNameSchema)
def new_company(company: CreateCompanySchema, x_wanted_language: str = Header(...), db: Session = Depends(get_db)):
    """
    3.  새로운 회사 추가
    새로운 언어(tw)도 같이 추가 될 수 있습니다.
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    company = create_company_service(company, db)
    company_name = get_company_name_service(company, x_wanted_language, db)
    return CompanyNameSchema.from_orm_with_tag_names(x_wanted_language, company_name)


@router.get("/tags", response_model=List[OnlyCompanyNameSchema])
def search_tag_name(query: str, x_wanted_language: str = Header(...), db: Session = Depends(get_db)):
    """
    4.  태그명으로 회사 검색
    태그로 검색 관련된 회사가 검색되어야 합니다.
    다국어로 검색이 가능해야 합니다.
    일본어 태그로 검색을 해도 language가 ko이면 한국 회사명이 노출이 되어야 합니다.
    ko언어가 없을경우 노출가능한 언어로 출력합니다.
    동일한 회사는 한번만 노출이 되어야합니다.
    """
    return get_search_tag_name_service(query, x_wanted_language, db)
    pass


@transactional
@router.put("/companies/{company_name}/tags", response_model=CompanyNameSchema)
def new_tag(company_name: str, tags: List[NewTagSchema], x_wanted_language: str = Header(...), db: Session = Depends(get_db)):
    """
    5.  회사 태그 정보 추가
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    new_tag_service(company_name, tags, db)
    company_name = get_company_search_service(company_name, x_wanted_language, db)
    return CompanyNameSchema.from_orm_with_tag_names(x_wanted_language, company_name)


@transactional
@router.delete("/companies/{company_name}/tags/{tag_name}", response_model=CompanyNameSchema)
def delete_tag(company_name: str, tag_name: str, x_wanted_language: str = Header(...), db: Session = Depends(get_db)):
    """
    6.  회사 태그 정보 삭제
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    delete_tag_service(company_name, tag_name, db)
    company_name = get_company_search_service(company_name, x_wanted_language, db)
    return CompanyNameSchema.from_orm_with_tag_names(x_wanted_language, company_name)
