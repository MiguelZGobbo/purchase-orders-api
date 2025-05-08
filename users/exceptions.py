from werkzeug.exceptions import HTTPException

class UserAlreadyExistException(HTTPException):
    code = 400

class UserEmailOrPasswordInvalidException(HTTPException):
    code = 404