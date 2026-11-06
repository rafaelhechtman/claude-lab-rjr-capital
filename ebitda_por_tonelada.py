"""
EBITDA e receita por tonelada: Gerdau por região x Usiminas Siderurgia (3T26).

ATENÇÃO À ORIGEM:
- EBITDA e receita da Gerdau: ITR 3T26 (pág. 72), via metricas_gerdau.json (verificado).
- VOLUME da Gerdau: NÃO está no ITR. Vem da apresentação de resultados 3T26 da Gerdau
  (6-K, Exhibit 99.1, 27/10/2026), lida por texto. Receita e EBITDA do mesmo documento
  batem com o ITR nos 3 segmentos, o que valida a leitura das colunas. Conferir os volumes
  no slide original antes de publicar.
- Usiminas: EBITDA da Siderurgia (pág. 33) e volume de aço (pág. 24), via metricas_usiminas.json.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
G = {m["metrica"]: m for m in json.loads((AQUI / "metricas_gerdau.json").read_text(encoding="utf-8"))}
U = {m["metrica"]: m for m in json.loads((AQUI / "metricas_usiminas.json").read_text(encoding="utf-8"))}

def br(x, c=0):
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Volumes da Gerdau (mil t), apresentação 3T26. Formato: (3T26, 3T25)
VOL = {"Brasil": (1351, 1582), "América do Norte": (1313, 1293), "América do Sul": (309, 289)}
# Mix de produto aproximado do Brasil (apresentação, "não se refere aos volumes do 3T26")
MIX_BRASIL_PLANO = 0.30

linhas = []
for seg, nome in (("América do Norte", "Gerdau\nAmérica do Norte"), ("Brasil", "Gerdau\nBrasil"), ("América do Sul", "Gerdau\nAmérica do Sul")):
    rec = G[f"Receita líquida - segmento {seg}"]["valor"] / 1000
    ebt = G[f"EBITDA ajustado - segmento {seg}"]["valor"] / 1000
    t = VOL[seg][0]
    linhas.append((nome, seg, ebt * 1000 / t, rec * 1000 / t, t))
u_ebt = U["EBITDA ajustado - Siderurgia"]["valor"]
u_rec = U["Receita líquida - Siderurgia"]["valor"]
u_t = U["Volume de vendas de aço"]["valor"]
linhas.append(("Usiminas\nSiderurgia", "Usiminas", u_ebt * 1000 / u_t, u_rec * 1000 / u_t, u_t))

print("Operação                | EBITDA R$/t | Receita R$/t | Volume mil t")
for nome, seg, e, r, t in linhas:
    print(f"{seg:<23} | {br(e):>11} | {br(r):>12} | {br(t):>10}")
na, brz, sa, us = [l[2] for l in linhas]
print(f"NA / Brasil = {na/brz:.1f}x ; NA / Usiminas = {na/us:.1f}x ; Brasil / Usiminas = {brz/us:.2f}x")
print(f"Receita/t NA vs Brasil: +{(linhas[0][3]/linhas[1][3]-1)*100:.0f}%")
print("Volume A/A:", {k: f"{(a/b-1)*100:+.1f}%" for k, (a, b) in VOL.items()}, "| Usiminas aço:", f"{(U['Volume de vendas de aço']['valor']/U['Volume de vendas de aço']['anterior']-1)*100:+.1f}%")
print("Escala do aço plano no Brasil (30% do mix aprox. x 1.351 mil t):", br(MIX_BRASIL_PLANO * 1351), "mil t (ordem de grandeza)")

# ---- gráfico ----
INK, INK2, MUDO, GRADE, SUP = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
AZ, AZC, LA = "#2a78d6", "#9ec5f4", "#eb6834"
plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "text.color": INK})
fig, ax = plt.subplots(figsize=(11, 6), dpi=160, facecolor=SUP)
ax.set_facecolor(SUP)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GRADE); ax.tick_params(colors=MUDO, length=0)
ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
ax.set_ylim(0, 2600); ax.yaxis.set_major_formatter(lambda x, _: br(x))
cores = [AZ, AZC, AZC, LA]
for k, ((nome, seg, e, r, t), c) in enumerate(zip(linhas, cores)):
    ax.bar(k, e, 0.55, color=c, zorder=3)
    ax.text(k, e + 45, f"R\\$ {br(e)}/t", ha="center", fontsize=14, fontweight="bold")
ax.set_xticks(range(4)); ax.set_xticklabels([f"{l[0]}\n{br(l[4])} mil t" for l in linhas], fontsize=12, color=INK2); ax.tick_params(axis="x", pad=6)
fig.text(0.06, 0.94, f"A América do Norte gera mais de {int(na/brz)} vezes o EBITDA por tonelada das demais operações", fontsize=17, fontweight="bold", ha="left")
fig.text(0.06, 0.895, "EBITDA ajustado por tonelada vendida, 3T26 (R\\$/t). Brasil, América do Sul e Usiminas ficam todos perto de R\\$ 500-550/t", fontsize=11, color=INK2, ha="left")
fig.text(0.06, 0.02, "Fonte: EBITDA, ITR 3T26 (Gerdau pág. 72; Usiminas pág. 33).\nVolume: Gerdau, apresentação de resultados 3T26 (6-K de 27/10/2026, fora do ITR); Usiminas pág. 24. Cálculo nosso. Exercício acadêmico, não é recomendação de investimento.", fontsize=7.5, color=MUDO, ha="left")
fig.subplots_adjust(top=0.82, bottom=0.24, left=0.08, right=0.97)
fig.savefig(AQUI / "graficos" / "6_ebitda_por_tonelada.png"); plt.close(fig)
