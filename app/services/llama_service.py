import subprocess
from app.config.settings import LLAMA_CPP_PATH, MODEL_PATH


class LlamaService:

    def __init__(self):
        self.llama_cpp = LLAMA_CPP_PATH
        self.llama_model = MODEL_PATH

    def generate_response(self, prompt: str):
        command = [
            self.llama_cpp,
            "-m", self.llama_model,
            "-n", "200",
            "-ngl", "0",
            prompt
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout

    def validate_reliability(self, text: str) -> str:
        prompt = (
            "Você é um verificador de fatos. Analise a seguinte afirmação e diga se ela parece confiável ou "
            "possivelmente falsa. Dê uma justificativa clara e objetiva:\n\n"
            f"\"{text}\"\n\n"
            "Resposta:"
        )
        command = [
            self.llama_cpp,
            "-m", self.llama_model,
            "-n", "200",
            "-ngl", "0",
            prompt
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip()


llama_service = LlamaService()
