from fastapi import APIRouter
from pydantic import BaseModel
from app.services.opensearch_service import OpenSearchService
from app.services.llama_service import llama_service

router = APIRouter()


class Pergunta(BaseModel):
    texto: str


@router.post("/ask")
def ask(pergunta: Pergunta):
    search_service = OpenSearchService()
    texto = pergunta.texto
    fake_match = search_service.search_fake_news_match(texto)
    if fake_match:
        return {
            "answer": "Essa pergunta é muito semelhante a uma notícia identificada como falsa.",
            "fake_news_match": fake_match
        }

    best_match = search_service.search_best_match(texto)
    response = llama_service.generate_response(best_match)
    return {"answer": response}
