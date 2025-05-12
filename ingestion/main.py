# ingestion/main.py
import os
import logging
import argparse
from tqdm import tqdm
from dotenv import load_dotenv

from ingestion.readers import read_markdown_file, find_files
from ingestion.chunkers import split_by_paragraphs
from ingestion.embedders import get_embedding
from ingestion.metadata import extract_metadata_from_path
from ingestion.writers import insert_chunks

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ingestion.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

load_dotenv()


def process_file(file_path, base_dir, max_tokens=500):
    """
    Processa um único arquivo: lê, divide em chunks, gera embeddings e metadados

    Args:
        file_path: caminho completo para o arquivo
        base_dir: diretório base para calcular caminho relativo
        max_tokens: número máximo de tokens por chunk

    Returns:
        list: Lista de chunks processados, cada um com content, embedding e metadata
    """
    logger.info(f"Processando arquivo: {file_path}")

    # Ler o conteúdo do arquivo
    content = read_markdown_file(file_path)
    if not content:
        logger.warning(f"Conteúdo vazio ou erro ao ler {file_path}")
        return []

    # Extrair metadados do caminho
    file_metadata = extract_metadata_from_path(file_path, base_dir)

    # Dividir em chunks
    chunks_text = split_by_paragraphs(content, max_tokens=max_tokens)
    logger.info(f"Arquivo dividido em {len(chunks_text)} chunks")

    # Processar cada chunk
    processed_chunks = []
    for i, chunk_text in enumerate(chunks_text):
        try:
            # Gerar embedding
            embedding = get_embedding(chunk_text)

            # Cria metadata específica do chunk (copia os metadados do arquivo)
            chunk_metadata = file_metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["chunk_count"] = len(chunks_text)

            # Criar objeto do chunk completo
            chunk = {
                "content": chunk_text,
                "embedding": embedding,
                "metadata": chunk_metadata,
            }
            processed_chunks.append(chunk)

        except Exception as e:
            logger.error(
                f"Erro ao processar chunk {i} do arquivo {file_path}: {str(e)}"
            )

    return processed_chunks


def run_ingestion(knowledge_dir, extensions=[".md"], max_tokens=500):
    """
    Executa o pipeline completo de ingestão para os arquivos especificados

    Args:
        knowledge_dir: diretório raiz da base de conhecimento
        extensions: extensões de arquivo a processar
        max_tokens: número máximo de tokens por chunk
    """
    logger.info(f"Iniciando ingestão de arquivos em {knowledge_dir}")

    # Encontrar todos os arquivos para processar
    files = find_files(knowledge_dir, extensions)
    logger.info(f"Encontrados {len(files)} arquivos para processar")

    all_chunks = []

    # Processar cada arquivo com barra de progresso
    for file_path in tqdm(files, desc="Processando arquivos"):
        chunks = process_file(file_path, knowledge_dir, max_tokens)
        all_chunks.extend(chunks)

    logger.info(f"Total de {len(all_chunks)} chunks gerados")

    # Inserir todos os chunks na base de dados
    if all_chunks:
        logger.info("Inserindo chunks no Supabase...")
        inserted_ids = insert_chunks(all_chunks)
        logger.info(
            f"Inserção concluída. {len(inserted_ids)} chunks inseridos com sucesso."
        )
    else:
        logger.warning("Nenhum chunk para inserir.")

    return all_chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pipeline de ingestão para a base de conhecimento"
    )
    parser.add_argument(
        "--knowledge_dir",
        default="knowledge_base_source",
        help="Diretório raiz da base de conhecimento",
    )
    parser.add_argument(
        "--max_tokens", type=int, default=500, help="Número máximo de tokens por chunk"
    )
    parser.add_argument(
        "--agent",
        help="Processar apenas arquivos de um agente específico (ex: neurohook)",
    )

    args = parser.parse_args()

    # Se um agente específico foi solicitado, ajuste o diretório
    if args.agent:
        knowledge_dir = os.path.join(args.knowledge_dir, f"{args.agent}_knowledge")
    else:
        knowledge_dir = args.knowledge_dir

    # Executar o pipeline
    run_ingestion(knowledge_dir, max_tokens=args.max_tokens)
