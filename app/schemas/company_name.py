from pydantic import BaseModel, Field


class CompanyName(BaseModel):
    id: int
    company_id: int
    country: str
    name: str = Field(..., alias="company_name")


class OnlyCompanyName(BaseModel):
    name: str

    class Config:
        populate_by_name = True
