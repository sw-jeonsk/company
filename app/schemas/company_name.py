from typing import List

from pydantic import BaseModel, Field

from app.schemas.company_tag import CompanyTagSchema


class CompanyNameSchema(BaseModel):
    company_name: str
    country: str
    tags: List[CompanyTagSchema] | List[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_tag_names(cls, country, company_name):
        return cls(
            id=company_name.id,
            country=company_name.country,
            company_name=company_name.name,
            tags=[tag.name for tag in company_name.company.tags if tag.country == country]
        )


class OnlyCompanyNameSchema(BaseModel):
    name: str = Field(..., alias="company_name")

    class Config:
        populate_by_name = True

