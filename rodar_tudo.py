"""
Um comando só: PDFs dos ITRs -> verificação dos números -> cálculos e gráficos -> apresentação.

    python rodar_tudo.py data/case3_resultados/itrs

O deck SÓ é gerado se TODOS os números dos metricas_*.json passarem no verificador. Se algum falhar, o
fluxo para e mostra os itens com ERRO: corrija o JSON olhando a página indicada (ou peça ao Claude Code:
"corrija no JSON só os itens com ERRO, olhando a página indicada") e rode de novo.

Para um novo trimestre: troque os PDFs, refaça metricas_gerdau.json e metricas_usiminas.json (prompt 3 de
prompts.md) e rode este comando. A extração das métricas pelo Claude é a única etapa que ainda é manual.
"""
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).parent


def passo(titulo, *args, parar_se_falhar=True):
    print(f"\n=== {titulo} ===", flush=True)
    r = subprocess.run([sys.executable, "-I", *map(str, args)], cwd=AQUI)
    if r.returncode != 0 and parar_se_falhar:
        print(f"\n[PARADO] '{titulo}' falhou (código {r.returncode}). O deck não foi gerado.", flush=True)
        raise SystemExit(r.returncode)
    return r.returncode


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    pdfs = sys.argv[1]
    passo("1. Extrair o texto de cada página dos ITRs", "extrair_paginas.py", pdfs, "saida")
    passo("2. Verificar os números da Gerdau contra o PDF", "verificar_numeros.py", "saida/gerdau", "metricas_gerdau.json")
    passo("3. Verificar os números da Usiminas contra o PDF", "verificar_numeros.py", "saida/usiminas", "metricas_usiminas.json")
    passo("4. Tabela comparativa e gráficos de segmento", "comparar.py")
    passo("5. Ponte de margem (quanto da diferença vem da América do Norte)", "decomposicao_margem.py")
    passo("6. Gráfico de receita, EBITDA e margem", "grafico_trimestre.py")
    passo("7. EBITDA por tonelada (análise complementar, volumes de fora do ITR)", "ebitda_por_tonelada.py")
    passo("8. Gerar a apresentação e as notas do apresentador", "gerar_slides.py")
    print("\nPronto: apresentacao.html e notas_apresentador.md gerados com todos os números verificados.")


if __name__ == "__main__":
    main()
