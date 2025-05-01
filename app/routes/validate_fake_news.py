from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from app.services.opensearch_service import OpenSearchService
from app.services.llama_service import llama_service

router = APIRouter()


class Noticia(BaseModel):
    titulo: str
    autor: str
    materia: str
    data_publicacao: date


@router.post("/validate-fake-news")
def validate_fake_news(noticia: Noticia):
    search_service = OpenSearchService()

    texto_completo = f"{noticia.titulo}. {noticia.materia}"

    noticia_existente = search_service.search_best_match(texto_completo)

    prompt = (
        "A seguinte notícia é falsa ou verdadeira? Responda apenas com FALSA ou VERDADEIRA:\n\n"
        f"{texto_completo}"
    )
    resposta = llama_service.generate_response(prompt)

    fake = "falsa" in resposta.lower()
    confiabilidade = 0.9 if fake else 0.7

    resultado = search_service.atualizar_confiabilidade(
        noticia.titulo, fake, confiabilidade
    )

    return {
        "noticia": noticia_existente,
        "avaliacao": "Fake News" if fake else "Notícia Verdadeira",
        "confiabilidade": confiabilidade,
        "resultado": resultado
    }
