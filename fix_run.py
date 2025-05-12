#!/usr/bin/env python3
# fix_run.py  --  garante que 'run()' esteja dentro da classe AgentGenerator
import re
import sys
import shutil
import pathlib

path = pathlib.Path("scripts/agent_generator.py")
src = path.read_text().splitlines(keepends=True)

txt = "".join(src)
m_cls = re.search(r"^class\s+AgentGenerator\b.*?:", txt, re.M)
m_run = re.search(r"^def\s+run\(", txt, re.M)

if not (m_cls and m_run):
    print("Classe ou método não encontrados.")
    sys.exit()

# run fora da classe?
if m_run.start() < m_cls.end():
    print("run() já está dentro da classe.")
    sys.exit()

print("→ Reindentando método run() dentro da classe…")
# isola bloco run
start = m_run.start()
block = []
i = start
while i < len(txt) and not re.match(r"^\S", txt[i:]):  # simples
    line = txt[i : txt.find("\n", i) + 1]
    block.append(line)
    i += len(line)

# backup
shutil.copy2(path, path.with_suffix(".py.bak"))

# monta arquivo novo
indent = " " * 4
new_txt = txt[:start] + "".join(indent + l if l.strip() else l for l in block) + txt[i:]
path.write_text(new_txt)
print("✔ run() reindentado.  Backup em", path.with_suffix(".py.bak"))
