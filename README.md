# company

- ## version
  - python:3.11.9

- ## command
  - host run
    - ```uvicorn main:app --reload```
    - api 명세 : http://127.0.0.1:8000/docs
  - docker-compose run
    - ```docker-compose   up --build -d```
    - api 명세 : http://127.0.0.1:9090/docs

- ## 요구사항 분석
  - 나라는 자유롭게 추가가 가능한 것으로 보임
  - x-wanted-language는 테스트코드를 보니, 필수로 넣어주는 내용으로 보임
  - company에 code를 추가하여, 회사별 unique 한것을 구별하기 위해 필수요소로 생각한다.
  - **테스트코드 app > tests > test_senior_app2.py 참조**

- ## ddl
  - header 기준 (x-wanted-language)의 (ko, ja, 등)으로 우선 filter를 진행하고, 포함된 단어를 name에서 찾기 때문에 name은 index 설정하지 않고, country만 index 설정하는게 좋다고 판단함.
  - ### migration
    - ```alembic revision --autogenerate```

