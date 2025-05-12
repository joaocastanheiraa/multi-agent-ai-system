# ingestion/writers.py
import os
import logging
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
logger = logging.getLogger(__name__)


def get_supabase_client():
    """Retorna um cliente Supabase inicializado com as credenciais do .env"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL e SUPABASE_KEY devem estar definidos no arquivo .env"
        )

    return create_client(url, key)


def insert_chunks(chunks, table_name="knowledge_base", batch_size=100):
    """
    Insere chunks na tabela especificada do Supabase

    Args:
        chunks: lista de dicionários, cada um com 'content', 'embedding' e 'metadata'
        table_name: nome da tabela no Supabase
        batch_size: número de chunks a inserir de cada vez
    """
    if not chunks:
        logger.warning("Nenhum chunk para inserir")
        return []

    client = get_supabase_client()
    inserted_ids = []

    # Processar em lotes para melhor performance
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        try:
            response = client.table(table_name).insert(batch).execute()

            # Extrair IDs dos itens inseridos
            if response.data:
                batch_ids = [item.get("id") for item in response.data]
                inserted_ids.extend(batch_ids)
                logger.info(
                    f"Inseridos {len(batch_ids)} chunks (batch {i//batch_size + 1})"
                )

        except Exception as e:
            logger.error(f"Erro ao inserir batch {i//batch_size + 1}: {str(e)}")
            # Continua para tentar inserir os próximos lotes

    return inserted_ids
