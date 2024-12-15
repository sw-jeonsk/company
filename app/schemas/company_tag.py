from pydantic import BaseModel, Field
from typing_extensions import Dict


class CompanyTag(BaseModel):
    name: str

    class Config:
        from_attributes = True


class NewTag(BaseModel):
    tag_name: Dict[str, str] = Field(
        description="나라별 회사 tag 정의",
        example={
            "ko": "태그_1",
            "tw": "tag_1",
            "en": "tag_1",
        }
    )
