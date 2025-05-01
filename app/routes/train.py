from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date
from app.services.opensearch_service import OpenSearchService

router = APIRouter()


class Noticia(BaseModel):
    titulo: str
    autor: str
    materia: str
    data_publicacao: date


@router.post("/train")
def train_noticias(noticias: List[Noticia]):
    search_service = OpenSearchService()
    docs = [noticia.dict() for noticia in noticias]
    return search_service.index_texts_full(docs)
