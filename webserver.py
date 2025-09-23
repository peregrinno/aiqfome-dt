from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import logging

from settings import api_settings
from src import (
    AuthenticationError,
    BaseError,
    InternalServerError,
)
from src.gateway import api_router
from src.init_db import init_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=api_settings.TITLE,
    version=api_settings.VERSION,
    openapi_url="/openapi.json",
    description="API AiQfome - Desafio técnico - API para adicionar favoritar produtos",
    contact={
        "name": "AiQfome",
        "url": "https://github.com/peregrinno/aiqfome-dt",
        "email": "joseluan74@gmail.com",
    }
)

origins = api_settings.CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("Inicializando o banco de dados...")
    init_db()
    logger.info("Aplicação inicializada com sucesso!")

@app.exception_handler(BaseError)
async def handle_base_error(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.description,
        },
    )

@app.exception_handler(AuthenticationError)
async def handle_authentication_error(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.description,
        },
    )

@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"validation_errors": exc.errors()},
    )

@app.exception_handler(InternalServerError)
async def handle_internal_server_error(request: Request, exc: InternalServerError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.description,
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "webserver:app",
        host=api_settings.HOST,
        port=api_settings.PORT,
        reload=api_settings.LOG_LEVEL == "debug"
    )