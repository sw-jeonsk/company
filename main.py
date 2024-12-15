from fastapi import FastAPI

from app import router

# FastAPI 인스턴스를 생성
app = FastAPI()


# 기본 라우트 설정


app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}