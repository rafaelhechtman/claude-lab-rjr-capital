"""
Engenharia reversa da margem consolidada da Gerdau por segmento.

Usa SÓ números verificados (metricas_gerdau.json / metricas_usiminas.json).
Responde: quanto da diferença de margem Gerdau x Usiminas vem da América do Norte?
E: se o ITR não abre longo x plano, o que dá para dizer do Brasil por cenário?

    python decomposicao_margem.py   ->  estimativa_margem_segmentos.md + graficos/5_ponte_margem.png
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
G = {m["metrica"]: m for m in json.loads((AQUI / "metricas_gerdau.json").read_text(encoding="utf-8"))}
U = {m["metrica"]: m for m in json.loads((AQUI / "metricas_usiminas.json").read_text(encoding="utf-8"))}

def br(x, c=1):
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---- insumos (R$ milhões) ----
def v(k, campo="valor"):
    return G[k][campo] / 1000
rec, rec0 = v("Receita líquida consolidada"), v("Receita líquida consolidada", "anterior")
ebt, ebt0 = v("EBITDA ajustado consolidado"), v("EBITDA ajustado consolidado", "anterior")
na_r, na_r0 = v("Receita líquida - segmento América do Norte"), v("Receita líquida - segmento América do Norte", "anterior")
na_e, na_e0 = v("EBITDA ajustado - segmento América do Norte"), v("EBITDA ajustado - segmento América do Norte", "anterior")
br_r, br_e = v("Receita líquida - segmento Brasil"), v("EBITDA ajustado - segmento Brasil")
u_rec, u_ebt = U["Receita líquida consolidada"]["valor"] / 1000, U["EBITDA ajustado consolidado"]["valor"] / 1000

# Ex-América do Norte = consolidado - América do Norte (a NA não tem vendas entre segmentos, pág. 72;
# as eliminações estão todas no resto, então o ex-NA já é líquido delas)
ex_r, ex_e, ex_r0, ex_e0 = rec - na_r, ebt - na_e, rec0 - na_r0, ebt0 - na_e0
M, M0 = ebt / rec * 100, ebt0 / rec0 * 100
mna, mna0 = na_e / na_r * 100, na_e0 / na_r0 * 100
mex, mex0 = ex_e / ex_r * 100, ex_e0 / ex_r0 * 100
s, s0 = na_r / rec, na_r0 / rec0                       # peso da NA na receita
mu = u_ebt / u_rec * 100

# ---- 1) ponte Usiminas -> Gerdau (3T26) ----
gap_total = M - mu
gap_exna = mex - mu
efeito_na = M - mex
part_na = efeito_na / gap_total * 100

# ---- 2) decomposição A/A da margem consolidada (exata, pontos médios) ----
sm, mnam, mexm = (s + s0) / 2, (mna + mna0) / 2, (mex + mex0) / 2
ef_na_margem = sm * (mna - mna0)                        # margem da NA subiu
ef_ex_margem = (1 - sm) * (mex - mex0)                  # margem do resto subiu
ef_mix = (s - s0) * (mnam - mexm)                       # NA ganhou peso na receita
dM = M - M0

# ---- 3) cenários: se o Brasil tem uma fatia de aço plano, qual a margem implícita do longo? ----
cen = []
for m_plano in (6.0, 9.6, 12.8):
    linha = []
    for fatia in (0.10, 0.20, 0.30, 0.40):
        e_plano = fatia * br_r * m_plano / 100
        m_longo = (br_e - e_plano) / ((1 - fatia) * br_r) * 100
        linha.append(m_longo)
    cen.append((m_plano, linha))

md = f"""# Engenharia reversa: quanto da margem da Gerdau vem da América do Norte

Só números verificados do ITR (págs. 72 e 29) mais cálculos. Nada aqui é dado de produto: o ITR não abre aço longo x plano.

## 1. Ponte de margem EBITDA ajustado, Usiminas -> Gerdau (3T26)
| Passo | Margem | Diferença |
|---|---|---|
| Usiminas consolidada | {br(mu)}% | |
| Gerdau **sem** América do Norte (consolidado - segmento NA) | {br(mex)}% | +{br(gap_exna)} p.p. |
| Efeito da América do Norte | | +{br(efeito_na)} p.p. |
| Gerdau consolidada | {br(M)}% | +{br(gap_total)} p.p. no total |

**{br(part_na, 0)}% da diferença de margem entre as duas vem da América do Norte.** A Gerdau sem a América do Norte fica a {br(gap_exna)} p.p. da Usiminas.

## 2. De onde veio o ganho de margem da Gerdau em um ano (3T25 -> 3T26)
Margem consolidada: {br(M0)}% -> {br(M)}% ({br(dM)} p.p. a mais).
| Efeito | p.p. |
|---|---|
| Margem da América do Norte subiu ({br(mna0)}% -> {br(mna)}%) | +{br(ef_na_margem, 2)} |
| Margem do resto (Brasil, América do Sul, eliminações) praticamente parada ({br(mex0)}% -> {br(mex)}%) | {'+' if ef_ex_margem >= 0 else ''}{br(ef_ex_margem, 2)} |
| Mix: a América do Norte pesa mais na receita ({br(s0*100, 0)}% -> {br(s*100, 0)}%) | +{br(ef_mix, 2)} |
| **Total** | **+{br(ef_na_margem + ef_ex_margem + ef_mix, 2)}** |

## 3. E o Brasil por tipo de aço? Cenários (não é dado, é sensibilidade)
Segmento Brasil da Gerdau: margem {br(br_e / br_r * 100)}% (EBITDA R$ {br(br_e, 0)} mi sobre receita R$ {br(br_r, 0)} mi). Se uma fatia dessa receita fosse aço plano com margem parecida com a de plano da Usiminas, qual seria a margem implícita do aço longo?

| Margem assumida do plano \\ fatia de plano no Brasil | 10% | 20% | 30% | 40% |
|---|---|---|---|---|
""" + "\n".join(f"| {br(mp)}% | " + " | ".join(f"{br(x)}%" for x in l) + " |" for mp, l in cen) + f"""

A apresentação de resultados da Gerdau (fora do ITR) indica um portfólio aproximado de ~70% longo e ~30% plano no Brasil, mas ressalva que não se refere aos volumes do 3T26. Na coluna de 30%, o longo fica entre {br(min(l[2] for _, l in cen))}% e {br(max(l[2] for _, l in cen))}% conforme a margem assumida para o plano.

Leitura: mesmo variando bastante a fatia e a margem do plano, o longo no Brasil fica na casa de ~{br(min(min(l) for _, l in cen), 0)}% a ~{br(max(max(l) for _, l in cen), 0)}%, muito abaixo dos {br(mna)}% da América do Norte. A conclusão não depende da hipótese sobre o plano.
Limites: o segmento Brasil também inclui aços especiais e a operação de minério (pág. 71), e o EBITDA inclui a parte proporcional de controladas em conjunto.
"""
(AQUI / "estimativa_margem_segmentos.md").write_text(md, encoding="utf-8")

# ---- gráfico: ponte ----
INK, INK2, MUDO, GRADE, SUP = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
AZ, AZC, LA = "#2a78d6", "#9ec5f4", "#eb6834"
plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "text.color": INK})
fig, ax = plt.subplots(figsize=(11, 6), dpi=160, facecolor=SUP)
ax.set_facecolor(SUP)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GRADE); ax.tick_params(colors=MUDO, length=0)
ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
ax.set_ylim(0, 25); ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0f}%")
w = 0.55
ax.bar(0, mu, w, color=LA, zorder=3)
ax.bar(1, gap_exna, w, bottom=mu, color=AZC, zorder=3)
ax.bar(2, efeito_na, w, bottom=mex, color=AZ, zorder=3)
ax.bar(3, M, w, color=AZ, zorder=3)
ax.text(0, mu + 0.4, f"{br(mu)}%", ha="center", fontsize=13, fontweight="bold")
ax.text(1, mex + 0.4, f"+{br(gap_exna)} p.p.", ha="center", fontsize=13)
ax.text(2, M + 0.4, f"+{br(efeito_na)} p.p.", ha="center", fontsize=13, fontweight="bold")
ax.text(3, M + 0.4, f"{br(M)}%", ha="center", fontsize=13, fontweight="bold")
for x0, x1, y in ((0, 1, mu), (1, 2, mex), (2, 3, M)):
    ax.plot([x0 + w / 2, x1 - w / 2], [y, y], color=MUDO, linewidth=1, linestyle=(0, (3, 3)), zorder=2)
ax.set_xticks(range(4))
ax.set_xticklabels(["Usiminas\nconsolidada", "Gerdau sem\nAmérica do Norte\n(" + br(mex) + "%)", "Efeito da\nAmérica do Norte", "Gerdau\nconsolidada"], fontsize=12, color=INK2)
fig.text(0.06, 0.94, f"Sem a América do Norte, a margem da Gerdau seria {br(mex)}%, a {br(gap_exna)} p.p. da Usiminas", fontsize=17, fontweight="bold", ha="left")
fig.text(0.06, 0.895, f"Margem EBITDA ajustado, 3T26. A América do Norte explica {br(part_na, 0)}% da diferença de {br(gap_total)} p.p.", fontsize=11, color=INK2, ha="left")
fig.text(0.06, 0.02, "Fonte: ITR 3T26, Gerdau págs. 29 e 72; Usiminas pág. 26. Gerdau sem América do Norte = consolidado menos o segmento (cálculo nosso). Exercício acadêmico, não é recomendação de investimento.", fontsize=8, color=MUDO, ha="left")
fig.subplots_adjust(top=0.82, bottom=0.2, left=0.07, right=0.97)
fig.savefig(AQUI / "graficos" / "5_ponte_margem.png"); plt.close(fig)
print(md)
