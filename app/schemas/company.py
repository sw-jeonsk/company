from typing import Dict, List
from pydantic import BaseModel, Field, ValidationError
from pydantic.v1 import root_validator


class CreateCompanySchema(BaseModel):
    code: str = Field(
        description="회사 이름을 대표하는 이름",
        example="라인"
    )
    company_name: Dict[str, str] = Field(
        description="나라별 회사 이름 정의",
        example={
            "ko": "라인 프레쉬",
            "tw": "LINE FRESH",
            "en": "LINE FRESH"
        }
    )
    tags: List = Field(
        description="나라별 회사 tag 정의",
        example=[
            {
                "tag_name": {
                    "ko": "태그_1",
                    "tw": "tag_1",
                    "en": "tag_1",
                }
            }
        ]
    )

    @root_validator
    def validate(cls, values):
        company_name = values.get("company_name")
        tags = values.get("tags")
        # 새로 생성되는 company의 tags에 국가코드가 다른 tag가 있으면 validation error 처리 진행
        for tag in tags:
            tag_name = tag.get("tag_name")
            if country := list((set(tag_name.keys()) - set(company_name.keys()))):
                raise ValidationError(f"잘못된 tag 국가 코드 입니다. {', '.join(country)}")
        return values
