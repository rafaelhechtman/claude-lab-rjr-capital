"""
Extrai o texto de cada página dos ITRs para a estrutura que o verificador espera:

    saida/gerdau/pagina_01.txt ... pagina_80.txt
    saida/usiminas/pagina_01.txt ... pagina_110.txt

Uso:
    python extrair_paginas.py <pasta_com_os_PDFs> [pasta_de_saida]

Exemplo (PDFs do repositório do case):
    python extrair_paginas.py data/case3_resultados/itrs saida

Procura arquivos cujo nome comece com "gerdau" e "usiminas". A numeração das páginas é a do PDF,
a mesma usada no mapa do README do case e em todas as citações do projeto (ex.: [G72], [U26]).
Atenção: no ITR da Usiminas, o número impresso no rodapé de cada página é uma unidade menor que a
página do PDF (a "PÁGINA 62 de 109" é a página 63 do PDF).
"""
import sys
from pathlib import Path

import pypdf


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    pasta = Path(sys.argv[1])
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("saida")
    for empresa in ("gerdau", "usiminas"):
        pdfs = sorted(pasta.glob(f"{empresa}*.pdf"))
        if not pdfs:
            print(f"[aviso] nenhum PDF começando com '{empresa}' em {pasta}")
            continue
        destino = saida / empresa
        destino.mkdir(parents=True, exist_ok=True)
        leitor = pypdf.PdfReader(str(pdfs[0]))
        for i, pagina in enumerate(leitor.pages, 1):
            (destino / f"pagina_{i:02d}.txt").write_text(pagina.extract_text() or "", encoding="utf-8")
        print(f"{empresa}: {len(leitor.pages)} páginas de {pdfs[0].name} -> {destino}")


if __name__ == "__main__":
    main()
