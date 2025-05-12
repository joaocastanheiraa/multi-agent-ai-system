# ingestion/readers.py
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_markdown_file(file_path):
    """Lê um arquivo markdown e retorna seu conteúdo"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except Exception as e:
        logger.error(f"Erro ao ler arquivo {file_path}: {str(e)}")
        return None


def find_files(root_dir, extensions=[".md"]):
    """
    Encontra todos os arquivos com as extensões especificadas recursivamente
    na pasta root_dir e retorna uma lista de caminhos completos
    """
    files = []
    root_path = Path(root_dir)

    for ext in extensions:
        files.extend(list(root_path.glob(f"**/*{ext}")))

    return [str(f) for f in files]


def get_relative_path(file_path, base_dir):
    """Obtém o caminho relativo do arquivo em relação ao diretório base"""
    return os.path.relpath(file_path, base_dir)


def get_domain_from_path(rel_path):
    """Extrai o domínio (agente principal) do caminho relativo"""
    parts = rel_path.split(os.sep)
    if len(parts) > 0:
        return parts[0].replace("_knowledge", "")
    return None


def get_subdomain_from_path(rel_path):
    """Extrai o subdomínio do caminho relativo"""
    parts = rel_path.split(os.sep)
    if len(parts) > 1:
        return "/".join(parts[1:])
    return None
