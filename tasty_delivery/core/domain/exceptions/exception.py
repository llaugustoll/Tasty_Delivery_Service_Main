from fastapi import HTTPException


class DuplicateObject(HTTPException):
    def __init__(self, msg: str, status_code: int):
        super(DuplicateObject, self).__init__(status_code=status_code, detail=msg)


class ObjectNotFound(HTTPException):
    def __init__(self, msg: str, status_code: int):
        super(ObjectNotFound, self).__init__(status_code=status_code, detail=msg)


class InvalidEmail(HTTPException):
    def __init__(self, msg: str, status_code: int):
        super(InvalidEmail, self).__init__(status_code=status_code, detail=msg)


class InvalidStatus(HTTPException):
    def __init__(self, msg: str, status_code: int):
        super(InvalidStatus, self).__init__(status_code=status_code, detail=msg)
