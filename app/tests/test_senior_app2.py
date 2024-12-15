import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, event
from app.models import CompanyModel, CompanyNameModel, CompanyTagModel
from db.database import get_db, Base
from db.test_database import engine, TestingSessionLocal
from main import app
import polars as pl


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    set_init_db(db)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # app에서 사용하는 DB를 오버라이드하는 부분
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def query_counter():
    """Counts the number of queries executed in a test."""
    queries_executed = []

    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        queries_executed.append(statement)

    event.listen(Engine, "before_cursor_execute", before_cursor_execute)

    yield queries_executed  # Provide the executed queries to the test

    event.remove(Engine, "before_cursor_execute", before_cursor_execute)


def set_init_db(db):
    # CSV 파일 읽기
    df = pl.read_csv("app/tests/company_tag_sample.csv")
    countries = ["ko", "en", "ja"]
    for row in df.iter_rows():
        row = dict(zip(df.columns, row))
        _company = CompanyModel(code=row.get("code"))
        db.add(_company)
        db.flush()
        db.add_all([
            CompanyNameModel(company_id=_company.id, country=country, name=row.get(f"company_{country}")) for country in countries if row.get(f"company_{country}")
        ])
        company_tags = []
        for country in countries:
            if tags := row.get(f"tag_{country}"):
                company_tags.extend([CompanyTagModel(company_id=_company.id, country=country, name=tag) for tag in tags.split("|")])
        db.add_all(company_tags)
    db.commit()


def test_company_name_autocomplete(client, query_counter):
    """
    1. 회사명 자동완성
    회사명의 일부만 들어가도 검색이 되어야 합니다.
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """

    response = client.get("/search?query=링크", headers=[("x-wanted-language", "ko")])
    response_json = response.json()

    assert len(query_counter) == 1
    assert response.status_code == 200
    assert response_json == [
        {"company_name": "주식회사 링크드코리아"},
        {"company_name": "스피링크"},
    ]

    response = client.get("/search?query=없는회사", headers=[("x-wanted-language", "ko")])
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == []


def test_company_search(client, query_counter):
    """
    2. 회사 이름으로 회사 검색
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """

    response = client.get(
        "/companies/Wantedlab", headers=[("x-wanted-language", "ko")]
    )
    response_json = response.json()
    assert len(query_counter) == 4
    assert response.status_code == 200
    assert response_json == {
        "company_name": "원티드랩",
        "country": "ko",
        "tags": [
            "태그_4",
            "태그_20",
            "태그_16",
        ],
    }

    # 검색된 회사가 없는경우 404를 리턴합니다.
    resp = client.get(
        "/companies/없는회사", headers=[("x-wanted-language", "ko")]
    )

    assert resp.status_code == 404


def test_new_company(client, query_counter):
    """
    3.  새로운 회사 추가
    새로운 언어(tw)도 같이 추가 될 수 있습니다.
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """

    response = client.post(
        "/companies",
        json={
            "code": "라인",
            "company_name": {
                "ko": "라인 프레쉬",
                "tw": "LINE FRESH",
                "en": "LINE FRESH",
            },
            "tags": [
                {
                    "tag_name": {
                        "ko": "태그_1",
                        "tw": "tag_1",
                        "en": "tag_1",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_8",
                        "tw": "tag_8",
                        "en": "tag_8",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_15",
                        "tw": "tag_15",
                        "en": "tag_15",
                    }
                }
            ]
        },
        headers=[("x-wanted-language", "tw")],
    )

    response_json = response.json()
    assert len(query_counter) == 6
    assert response.status_code == 200
    assert response_json.get("company_name") == "LINE FRESH"
    assert response_json.get("country") == "tw"
    assert response_json.get("tags") == ["tag_1", "tag_8", "tag_15"]


# def test_search_tag_name(client):
#     """
#     4.  태그명으로 회사 검색
#     태그로 검색 관련된 회사가 검색되어야 합니다.
#     다국어로 검색이 가능해야 합니다.
#     일본어 태그로 검색을 해도 language가 ko이면 한국 회사명이 노출이 되어야 합니다.
#     ko언어가 없을경우 노출가능한 언어로 출력합니다.
#     동일한 회사는 한번만 노출이 되어야합니다.
#     """
#     response = client.get("/tags?query=タグ_22", headers=[("x-wanted-language", "ko")])
#     response_json = response.json()
#     pass
#     # assert [company["company_name"] for company in searched_companies] == [
#     #     "딤딤섬 대구점",
#     #     "마이셀럽스",
#     #     "Rejoice Pregnancy",
#     #     "삼일제약",
#     #     "투게더앱스",
#     # ]


def test_new_tag(client):
    """
    5.  회사 태그 정보 추가
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    response = client.put(
        "/companies/원티드랩/tags",
        json=[
            {
                "tag_name": {
                    "ko": "태그_50",
                    "jp": "タグ_50",
                    "en": "tag_50",
                }
            },
            {
                "tag_name": {
                    "ko": "태그_4",
                    "tw": "tag_4",
                    "en": "tag_4",
                }
            }
        ],
        headers=[("x-wanted-language", "en")],
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("company_name") == "Wantedlab"
    assert response_json.get("tags") == ["tag_4", "tag_20", "tag_16", "tag_50"]


def test_delete_tag(client):
    """
    6.  회사 태그 정보 삭제
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    response = client.delete(
        "/companies/원티드랩/tags/태그_16",
        headers=[("x-wanted-language", "en")],
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("company_name") == "Wantedlab"
    assert response_json.get("tags") == [
        "tag_4",
        "tag_20",
        "tag_16"
    ]
