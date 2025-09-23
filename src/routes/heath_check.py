from datetime import datetime

from fastapi import APIRouter

from settings import api_settings

route = APIRouter()

@route.get("/", description="Verifica se a API está funcionando")
async def health_check():
    return {
        "version": api_settings.VERSION,
        "title": api_settings.TITLE,
        "message": "API funcionando corretamente",
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
    