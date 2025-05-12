# ingestion/embedders.py
import os
import time
import logging
import openai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configura a API key do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(
    text, model="text-embedding-ada-002", max_retries=3, backoff_factor=2
):
    """
    Gera um embedding para o texto usando a API do OpenAI,
    com retentativas e backoff exponencial
    """
    if not text or not text.strip():
        logger.warning("Texto vazio fornecido para embedding")
        return []

    retries = 0
    last_error = None

    while retries <= max_retries:
        try:
            response = openai.Embedding.create(model=model, input=text)
            embedding = response["data"][0]["embedding"]
            return embedding

        except openai.error.RateLimitError:
            wait_time = backoff_factor**retries
            logger.warning(f"Rate limit atingido. Aguardando {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
            last_error = "Rate limit"

        except openai.error.ServiceUnavailableError:
            wait_time = backoff_factor**retries
            logger.warning(f"Serviço indisponível. Aguardando {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
            last_error = "Serviço indisponível"

        except Exception as e:
            logger.error(f"Erro ao gerar embedding: {str(e)}")
            raise e

    logger.error(f"Falha após {max_retries} tentativas: {last_error}")
    raise Exception(f"Falha ao gerar embedding após {max_retries} tentativas")
