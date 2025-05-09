#!/usr/bin/env python3
# scripts/upload_to_supabase.py

import os
import sys
import json
import time
import argparse
import openai
from tqdm import tqdm
from supabase import create_client
from dotenv import load_dotenv
import signal
import atexit

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de argumentos
parser = argparse.ArgumentParser(description='Upload embeddings para Supabase')
parser.add_argument('jsonl_file', help='Arquivo JSONL com os dados para embeddings')
parser.add_argument('--supabase_url', help='URL do Supabase', default=os.environ.get('SUPABASE_URL'))
parser.add_argument('--supabase_key', help='Chave do Supabase', default=os.environ.get('SUPABASE_KEY'))
parser.add_argument('--openai_key', help='Chave da OpenAI', default=os.environ.get('OPENAI_API_KEY'))
parser.add_argument('--model', help='Modelo de embedding', default='text-embedding-ada-002')
parser.add_argument('--batch_size', type=int, help='Tamanho do lote para processamento', default=10)
parser.add_argument('--resume', action='store_true', help='Retomar upload de onde parou')
parser.add_argument('--table', help='Tabela do Supabase', default='knowledge_base')
args = parser.parse_args()

# Verificar argumentos obrigatórios
if not args.supabase_url or not args.supabase_key:
    print("❌ ERRO: URL e chave do Supabase são obrigatórios. Configure via variáveis de ambiente ou argumentos.")
    sys.exit(1)

if not args.openai_key:
    print("❌ ERRO: Chave da OpenAI é obrigatória. Configure via variável de ambiente OPENAI_API_KEY ou argumento --openai_key.")
    sys.exit(1)

# Configurar OpenAI
openai.api_key = args.openai_key

# Configurar cliente Supabase
supabase = create_client(args.supabase_url, args.supabase_key)

# Arquivo para acompanhar o progresso
progress_file = f"{args.jsonl_file}.progress"

# Iniciar de onde parou
start_from = 0
if args.resume and os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        try:
            start_from = int(f.read().strip())
            print(f"📝 Retomando do item {start_from}")
        except:
            print("⚠️ Arquivo de progresso inválido. Iniciando do começo.")

# Função para salvar progresso
def save_progress(line_num):
    with open(progress_file, 'w') as f:
        f.write(str(line_num))

# Garantir que o progresso seja salvo ao sair
atexit.register(lambda: print("✅ Progresso salvo. Para retomar, use o argumento --resume."))

# Manipulador de sinais para salvar progresso ao cancelar
def signal_handler(sig, frame):
    print("\n⚙️ Interrompido pelo usuário. Salvando progresso...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Ler e processar o arquivo JSONL
with open(args.jsonl_file, 'r') as f:
    lines = f.readlines()
    total = len(lines)
    
    print(f"📊 Total de itens: {total}")
    print(f"🔄 Processando em lotes de {args.batch_size}")
    
    # Pular itens já processados
    lines = lines[start_from:]
    
    # Criar barra de progresso
    with tqdm(total=len(lines), initial=0, desc="Processando") as pbar:
        # Processar em lotes
        for i in range(0, len(lines), args.batch_size):
            batch = lines[i:i+args.batch_size]
            batch_data = []
            
            # Preparar dados do lote
            for line in batch:
                try:
                    item = json.loads(line)
                    batch_data.append(item)
                except json.JSONDecodeError:
                    print(f"⚠️ Erro ao decodificar JSON na linha {start_from + i}")
                    continue
            
            # Obter embeddings do lote
            texts = [item['text'] for item in batch_data]
            try:
                response = openai.Embedding.create(
                    model=args.model,
                    input=texts
                )
                embeddings = [data['embedding'] for data in response['data']]
            except Exception as e:
                print(f"❌ Erro ao obter embeddings: {e}")
                # Salvar progresso antes de sair
                save_progress(start_from + i)
                sys.exit(1)
            
            # Inserir no Supabase
            for j, (item, embedding) in enumerate(zip(batch_data, embeddings)):
                try:
                    result = supabase.table(args.table).insert({
                        "content": item['text'],
                        "embedding": embedding,
                        "metadata": item['metadata']
                    }).execute()
                    
                    # Verificar se houve erro
                    if hasattr(result, 'error') and result.error:
                        print(f"⚠️ Erro ao inserir item {start_from + i + j}: {result.error}")
                except Exception as e:
                    print(f"⚠️ Erro ao inserir no Supabase: {e}")
            
            # Atualizar barra de progresso
            pbar.update(len(batch))
            
            # Salvar progresso
            save_progress(start_from + i + len(batch))
            
            # Evitar limite de taxa da API
            time.sleep(0.5)

print("✅ Upload concluído com sucesso!")
if os.path.exists(progress_file):
    os.remove(progress_file)
    print("🧹 Arquivo de progresso removido.")

