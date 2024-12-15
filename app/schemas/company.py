from typing import Dict, List
from pydantic import BaseModel, Field


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

