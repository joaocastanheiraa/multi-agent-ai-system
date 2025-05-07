# run_ingestion.py
import os
import sys
import argparse
from ingestion.main import run_ingestion

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de ingestão para a base de conhecimento")
    parser.add_argument(
        "--knowledge_dir", 
        default="knowledge_base_source",
        help="Diretório raiz da base de conhecimento"
    )
    parser.add_argument(
        "--max_tokens", 
        type=int, 
        default=500,
        help="Número máximo de tokens por chunk"
    )
    parser.add_argument(
        "--agent", 
        help="Processar apenas arquivos de um agente específico (ex: neurohook)"
    )
    
    args = parser.parse_args()
    
    # Se um agente específico foi solicitado, ajuste o diretório
    if args.agent:
        knowledge_dir = os.path.join(args.knowledge_dir, f"{args.agent}_knowledge")
    else:
        knowledge_dir = args.knowledge_dir
    
    # Executar o pipeline
    run_ingestion(knowledge_dir, max_tokens=args.max_tokens)

