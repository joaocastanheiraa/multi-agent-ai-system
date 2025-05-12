# ingestion/chunkers.py
import tiktoken
import logging
import re

logger = logging.getLogger(__name__)


def num_tokens_from_string(string, encoding_name="cl100k_base"):
    """Retorna o número de tokens em uma string"""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def split_by_tokens(text, max_tokens=500, overlap=50):
    """
    Divide o texto em chunks com número máximo de tokens,
    mantendo uma sobreposição para preservar contexto
    """
    if not text:
        return []

    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    i = 0

    while i < len(tokens):
        # Determina o fim do chunk atual
        end = min(i + max_tokens, len(tokens))

        # Decodifica tokens para texto
        chunk_tokens = tokens[i:end]
        chunk = encoding.decode(chunk_tokens)

        # Remove espaços em branco no início e fim
        chunk = chunk.strip()

        if chunk:  # Adiciona apenas se não estiver vazio
            chunks.append(chunk)

        # Avança, considerando sobreposição
        i = end - overlap if end < len(tokens) else end

    return chunks


def split_by_paragraphs(text, max_tokens=500, overlap_paragraphs=1):
    """
    Divide o texto em chunks por parágrafos,
    tentando manter cada chunk abaixo do limite de tokens,
    e mantendo uma sobreposição de parágrafos
    """
    if not text:
        return []

    # Separa por parágrafos
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    current_chunk = []
    current_token_count = 0

    for para in paragraphs:
        para_token_count = num_tokens_from_string(para)

        # Se o parágrafo sozinho excede o limite, divida-o
        if para_token_count > max_tokens:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                # Overlap: mantém últimos paragraphs para o próximo chunk
                current_chunk = (
                    current_chunk[-overlap_paragraphs:]
                    if overlap_paragraphs > 0
                    else []
                )
                current_token_count = sum(
                    num_tokens_from_string(p) for p in current_chunk
                )

            # Divide o parágrafo grande em chunks menores
            sub_chunks = split_by_tokens(para, max_tokens, 50)
            chunks.extend(sub_chunks[:-1])  # Adiciona todos menos o último

            # O último sub-chunk vai para o current_chunk para continuar o processamento
            if sub_chunks:
                current_chunk.append(sub_chunks[-1])
                current_token_count = num_tokens_from_string(sub_chunks[-1])

        # Se adicionar o parágrafo excede o limite, finaliza o chunk atual
        elif current_token_count + para_token_count > max_tokens and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            # Overlap: mantém últimos paragraphs para o próximo chunk
            current_chunk = (
                current_chunk[-overlap_paragraphs:] if overlap_paragraphs > 0 else []
            )
            current_chunk.append(para)
            current_token_count = sum(num_tokens_from_string(p) for p in current_chunk)

        # Caso contrário, adiciona o parágrafo ao chunk atual
        else:
            current_chunk.append(para)
            current_token_count += para_token_count

    # Adiciona o último chunk se houver algo
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks
