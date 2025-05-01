from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date
from app.services.opensearch_service import OpenSearchService

router = APIRouter()


class FakeNews(BaseModel):
    titulo: str
    autor: str
    materia: str
    data_publicacao: date


@router.post("/train-fake-news")
def train_fake_news(noticias: List[FakeNews]):
    search_service = OpenSearchService()
    docs = [noticia.dict() for noticia in noticias]
    return search_service.index_fake_texts_full(docs)
