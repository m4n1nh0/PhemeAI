from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
from app.config.settings import INDEX_NAME


class OpenSearchService:
    def __init__(self):
        self.client = OpenSearch(
            hosts=["http://localhost:9200"],
            http_auth=("admin", "admin")
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self._create_index()
        self._create_fake_news_index()

    def _create_index(self):
        if not self.client.indices.exists(index=INDEX_NAME):
            index_body = {
                "settings": {"index": {"knn": True}},
                "mappings": {
                    "properties": {
                        "titulo": {"type": "text"},
                        "autor": {"type": "text"},
                        "materia": {"type": "text"},
                        "data_publicacao": {"type": "date"},
                        "fake": {"type": "boolean"},
                        "confiabilidade": {"type": "float"},
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": 384,
                            "method": {
                                "name": "hnsw",
                                "space_type": "l2",
                                "engine": "faiss"
                            }
                        }
                    }
                }
            }
            self.client.indices.create(index=INDEX_NAME, body=index_body)
            print(f"Índice '{INDEX_NAME}' criado com sucesso!")

    def _create_fake_news_index(self):
        if not self.client.indices.exists(index="fake_news"):
            index_body = {
                "settings": {"index": {"knn": True}},
                "mappings": {
                    "properties": {
                        "titulo": {"type": "text"},
                        "autor": {"type": "text"},
                        "materia": {"type": "text"},
                        "data_publicacao": {"type": "date"},
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": 384,
                            "method": {
                                "name": "hnsw",
                                "space_type": "l2",
                                "engine": "faiss"
                            }
                        }
                    }
                }
            }
            self.client.indices.create(index="fake_news", body=index_body)
            print("Índice 'fake_news' criado com sucesso!")

    def index_texts_full(self, noticias: list[dict]):
        for noticia in noticias:
            embedding = self.embedding_model.encode(noticia["materia"]).tolist()
            doc = noticia.copy()
            doc["embedding"] = embedding
            self.client.index(index=INDEX_NAME, body=doc)
        return {"message": "Notícias completas indexadas com sucesso"}

    def index_fake_texts_full(self, noticias: list[dict]):
        for noticia in noticias:
            embedding = self.embedding_model.encode(noticia["materia"]).tolist()
            doc = noticia.copy()
            doc["embedding"] = embedding
            self.client.index(index="fake_news", body=doc)
        return {"message": "Fake news completas indexadas com sucesso"}

    def atualizar_confiabilidade(self, titulo: str, fake: bool, confiabilidade: float):
        script = {
            "source": """
                ctx._source.fake = params.fake;
                ctx._source.confiabilidade = params.confiabilidade;
            """,
            "params": {
                "fake": fake,
                "confiabilidade": confiabilidade
            }
        }

        query = {
            "query": {
                "match": {
                    "titulo": titulo
                }
            }
        }

        search = self.client.search(index=INDEX_NAME, body=query)
        hits = search.get("hits", {}).get("hits", [])

        if hits:
            doc_id = hits[0]["_id"]
            self.client.update(index=INDEX_NAME, id=doc_id, body={"script": script})
            return {"message": "Notícia atualizada com sucesso!"}
        return {"message": "Notícia não encontrada para atualização."}

    def search_best_match(self, query: str):
        embedding = self.embedding_model.encode(query).tolist()
        search_result = self.client.search(index=INDEX_NAME, body={
            "size": 1,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": 1
                    }
                }
            }
        })
        hits = search_result.get("hits", {}).get("hits", [])
        if hits:
            return hits[0]["_source"]
        return None

    def search_fake_news_match(self, query: str, threshold: float = 0.85):
        embedding = self.embedding_model.encode(query).tolist()
        search_result = self.client.search(index="fake_news", body={
            "size": 1,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": 1
                    }
                }
            }
        })
        hits = search_result.get("hits", {}).get("hits", [])
        if hits:
            score = hits[0]["_score"]
            if score >= threshold:
                return hits[0]["_source"]
        return None
