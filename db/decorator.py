from functools import wraps


def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.get("db")
        try:
            result = func(*args, **kwargs)
            db.commit()  # 커밋
            return result
        except Exception as e:
            db.rollback()  # 롤백
            raise e
    return wrapper
