from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class BaseError(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    description = "A base para todas as exceções personalizadas"

    def __init__(self, description=None, code=None):
        self.description = description or self.description
        self.code = code or self.code
        super().__init__(status_code=self.code, detail=self.description)

    def to_response(self):
        return JSONResponse(
            status_code=self.code,
            content={
                "error": self.__class__.__name__,
                "message": self.description,
            },
        )

class AuthenticationError(BaseError):
    code = status.HTTP_401_UNAUTHORIZED
    description = "Não autorizado. Por favor, verifique suas credenciais."
    
class InternalServerError(BaseError):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    description = "Erro interno do servidor. Tente novamente mais tarde."

class ConflictError(BaseError):
    code = status.HTTP_409_CONFLICT
    description = "Não é possivel criar esse usuário."

class BadRequestError(BaseError):
    code = status.HTTP_400_BAD_REQUEST
    description = "Requisição mal formatada. Tente novamente."