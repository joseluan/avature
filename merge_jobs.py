import json
import os
from glob import glob

PASTA = "subdomain_jobs"
SAIDA = "jobs.json"

all_jobs = []

for file in glob(os.path.join(PASTA, "*.json")):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                all_jobs.extend(data)
            else:
                print(f"Aviso: {file} não é lista, ignorado")
    except Exception as e:
        print(f"Erro ao ler {file}: {e}")

with open(SAIDA, "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=4, ensure_ascii=False)

print(f"Arquivo gerado: {SAIDA}")
print(f"Total de jobs: {len(all_jobs)}")
