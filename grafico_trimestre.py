"""
Gráfico exigido pelo roteiro do case: receita, EBITDA e margem, 3T26 contra 3T25, por empresa.
Lê só os JSONs verificados. Saída: graficos/7_receita_ebitda_margem.png
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
def sg(x, c=1):
    return ("+" if x > 0 else "") + br(x, c) + "%"

g_rec, g_rec0 = G["Receita líquida consolidada"]["valor"] / 1e6, G["Receita líquida consolidada"]["anterior"] / 1e6   # R$ bi
g_ebt, g_ebt0 = G["EBITDA ajustado consolidado"]["valor"] / 1e6, G["EBITDA ajustado consolidado"]["anterior"] / 1e6
u_rec, u_rec0 = U["Receita líquida consolidada"]["valor"] / 1e6, U["Receita líquida consolidada"]["anterior"] / 1e6
u_ebt, u_ebt0 = U["EBITDA ajustado consolidado"]["valor"] / 1e6, U["EBITDA ajustado consolidado"]["anterior"] / 1e6
dados = {
    "Receita líquida (R\\$ bi)": ((g_rec0, g_rec), (u_rec0, u_rec), 1.18, lambda v: br(v, 1)),
    "EBITDA ajustado (R\\$ bi)": ((g_ebt0, g_ebt), (u_ebt0, u_ebt), 1.22, lambda v: br(v, 2)),
    "Margem EBITDA ajustado (%)": ((g_ebt0 / g_rec0 * 100, g_ebt / g_rec * 100), (u_ebt0 / u_rec0 * 100, u_ebt / u_rec * 100), 1.22, lambda v: br(v, 1) + "%"),
}

INK, INK2, MUDO, GRADE, SUP = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
AZ, AZC, LA, LAC = "#2a78d6", "#9ec5f4", "#eb6834", "#f5b79d"
plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "text.color": INK})
fig, axes = plt.subplots(1, 3, figsize=(11, 5.6), dpi=160, facecolor=SUP)
for ax, (titulo, (g, u, folga, fmt)) in zip(axes, dados.items()):
    ax.set_facecolor(SUP)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRADE); ax.tick_params(colors=MUDO, length=0)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    ax.set_yticks([]); ax.set_ylim(0, max(g[1], u[1], g[0], u[0]) * folga)
    top = ax.get_ylim()[1]
    for k, (v0, v1, cl, cs) in enumerate(((g[0], g[1], AZC, AZ), (u[0], u[1], LAC, LA))):
        ax.bar(k - 0.2, v0, 0.36, color=cl, zorder=3); ax.bar(k + 0.2, v1, 0.36, color=cs, zorder=3)
        ax.text(k - 0.2, v0 + top * 0.015, fmt(v0), ha="center", fontsize=10, color=INK2)
        ax.text(k + 0.2, v1 + top * 0.015, fmt(v1), ha="center", fontsize=10.5, color=INK, fontweight="bold")
        var = (v1 / v0 - 1) * 100 if "Margem" not in titulo else (v1 - v0)
        rot = (sg(var) if "Margem" not in titulo else ("+" if var > 0 else "") + br(var) + " p.p.")
        ax.text(k, -top * 0.17, rot, ha="center", fontsize=10.5, color=INK, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Gerdau", "Usiminas"], fontsize=11.5, color=INK2); ax.tick_params(axis="x", pad=4)
    ax.set_title(titulo, fontsize=12.5, fontweight="bold", color=INK, loc="left", pad=10)
fig.text(0.015, 0.955, "claro = 3T25   escuro = 3T26   (variação contra o 3T25 abaixo de cada empresa)", fontsize=9.5, color=MUDO, ha="left")
fig.subplots_adjust(top=0.82, bottom=0.2, left=0.02, right=0.99, wspace=0.12)
fig.text(0.015, 0.015, "Fonte: ITR 3T26, Gerdau pág. 72; Usiminas págs. 26 e 28. Consolidado, EBITDA ajustado de cada empresa; margem calculada.", fontsize=8, color=MUDO, ha="left")
fig.savefig(AQUI / "graficos" / "7_receita_ebitda_margem.png"); plt.close(fig)
print("ok")
