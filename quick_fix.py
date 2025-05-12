#!/usr/bin/env python3
# quick_fix.py ─ Correção imediata de YAML e agent_generator.py
# Necessita: pip install ruamel.yaml

import re
import shutil
import argparse
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()


# ─────────────────────────────────────────────────────────────
# 1. Funções de reparo YAML
# ─────────────────────────────────────────────────────────────
def _indent_block(lines, start_idx, indent="  "):
    """
    Adiciona 'indent' às linhas seguintes até encontrar uma quebra de bloco.
    Critério de parada: linha vazia OU contém ':' na coluna 0 OU começa por '#'.
    """
    i = start_idx + 1
    while i < len(lines):
        line = lines[i]
        if (
            (not line.strip())
            or (re.match(r"^[A-Za-z0-9_-]+:", line))
            or line.startswith("#")
        ):
            break
        if not line.startswith(indent):
            lines[i] = indent + line.lstrip("\t ")
        i += 1
    return lines


def fix_yaml_file(path: Path):
    src = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = False

    # 1-A  corrigir TAB → 4 espaços
    for i, ln in enumerate(src):
        if "\t" in ln:
            src[i] = ln.replace("\t", "    ")
            changed = True

    # 1-B  blocos '|' ou '>'
    for idx, ln in enumerate(src):
        if re.search(r":\s*[|>]\s*$", ln):
            src = _indent_block(src, idx)
            changed = True

    if not changed:
        print("YAML: nada a corrigir.")
        return

    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    path.write_text("".join(src), encoding="utf-8")
    print(f"YAML: correções aplicadas, backup em {bak}")

    # 1-C  Validação ruamel
    try:
        yaml.load(Path(path).read_text(encoding="utf-8"))
        print("YAML: ✅ válido após correção.")
    except Exception as e:
        print("YAML: ⚠️  ainda inválido:", e)


# ─────────────────────────────────────────────────────────────
# 2. Funções de reparo agent_generator.py
# ─────────────────────────────────────────────────────────────
def fix_agent_generator(path: Path):
    code = path.read_text(encoding="utf-8").splitlines(keepends=True)
    txt = "".join(code)

    # 2-A  verificar sobrescrita da classe
    if re.search(r"^AgentGenerator\s*=", txt, flags=re.M):
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)
        code = [ln for ln in code if not re.match(r"^AgentGenerator\s*=", ln)]
        path.write_text("".join(code), encoding="utf-8")
        print("PY: Removida redefinição de AgentGenerator (backup criado).")

    # 2-B  garantir método run dentro da classe
    class_pat = re.compile(r"^class\s+AgentGenerator\b.*?:", re.M)
    m_class = class_pat.search(txt)
    if not m_class:
        print("PY: classe AgentGenerator não encontrada, pulando.")
        return
    class_start = m_class.end()

    # existe 'def run(' após início da classe, indentado?
    run_inside = re.search(r"^\s{4}def\s+run\(", txt[class_start:], re.M)
    if run_inside:
        print("PY: método run() já está correto.")
        return

    # existe run fora da classe?
    run_outside = re.search(r"^def\s+run\(", txt, re.M)
    if not run_outside:
        print("PY: método run() ausente – não será criado automaticamente.")
        return

    # Reindentar bloco 'run'
    run_start = run_outside.start()
    run_indent_pat = re.compile(r"^(def\s+run\(.*?)(\n(?: {0,3}\S.*\n?)*)", re.S)
    m_block = run_indent_pat.search(txt[run_start:])
    block = m_block.group(0).splitlines()
    block_indented = ["    " + ln if ln.strip() else ln for ln in block]

    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)

    new_code = (
        txt[:run_start]
        + "".join(block_indented)
        + txt[run_start + len("".join(block)) :]
    )
    path.write_text(new_code, encoding="utf-8")
    print("PY: método run() reindentado para dentro da classe (backup criado).")


# ─────────────────────────────────────────────────────────────
# 3. CLI
# ─────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Corrige YAML e agent_generator.py de forma automática"
)
parser.add_argument(
    "--yaml", type=Path, required=True, help="Caminho do arquivo YAML a corrigir"
)
parser.add_argument(
    "--agent", type=Path, required=True, help="Caminho do agent_generator.py"
)
args = parser.parse_args()

fix_yaml_file(args.yaml)
fix_agent_generator(args.agent)
print("\n✅  Processo de correção concluído.")
