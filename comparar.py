"""
Case 3 - Gerdau x Usiminas 3T26: tabela comparativa + gráficos.

Lê SOMENTE os JSONs já verificados (metricas_gerdau.json / metricas_usiminas.json),
converte tudo para R$ milhões, calcula as métricas derivadas (marcadas como
"calculado") e gera tabela_comparativa.md/.csv e graficos/*.png.

    python comparar.py
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
G = {m["metrica"]: m for m in json.loads((AQUI / "metricas_gerdau.json").read_text(encoding="utf-8"))}
U = {m["metrica"]: m for m in json.loads((AQUI / "metricas_usiminas.json").read_text(encoding="utf-8"))}

# ---- Paleta (skill dataviz, slots 1 e 2 validados em pares adjacentes) ----
AZUL, LARANJA = "#2a78d6", "#eb6834"
AZUL_CLARO, LARANJA_CLARO = "#9ec5f4", "#f5b79d"
INK, INK2, MUDO, GRADE, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"

def mi(v_mil):            # R$ mil -> R$ milhões
    return v_mil / 1000

def pct(a, b):            # variação %
    return (a / b - 1) * 100

def br(x, casas=1):       # 1234.5 -> '1.234,5'
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def sinal(x, casas=1):
    return ("+" if x > 0 else "") + br(x, casas) + "%"

# ---- Números base (R$ milhões) ----
g_rec, g_rec0 = mi(G["Receita líquida consolidada"]["valor"]), mi(G["Receita líquida consolidada"]["anterior"])
g_ebt, g_ebt0 = mi(G["EBITDA ajustado consolidado"]["valor"]), mi(G["EBITDA ajustado consolidado"]["anterior"])
g_lucro, g_lucro0 = mi(G["Lucro líquido consolidado"]["valor"]), mi(G["Lucro líquido consolidado"]["anterior"])
u_rec, u_rec0 = mi(U["Receita líquida consolidada"]["valor"]), mi(U["Receita líquida consolidada"]["anterior"])
u_ebt, u_ebt0 = mi(U["EBITDA ajustado consolidado"]["valor"]), mi(U["EBITDA ajustado consolidado"]["anterior"])
u_lucro, u_lucro0 = mi(U["Lucro (prejuízo) líquido consolidado"]["valor"]), mi(U["Lucro (prejuízo) líquido consolidado"]["anterior"])

g_rec9, g_rec90 = mi(G["Receita líquida consolidada - 9 meses"]["valor"]), mi(G["Receita líquida consolidada - 9 meses"]["anterior"])
g_ebt9, g_ebt90 = mi(G["EBITDA ajustado consolidado - 9 meses"]["valor"]), mi(G["EBITDA ajustado consolidado - 9 meses"]["anterior"])
u_rec9, u_rec90 = mi(U["Receita líquida consolidada - 9 meses"]["valor"]), mi(U["Receita líquida consolidada - 9 meses"]["anterior"])
u_ebt9, u_ebt90 = mi(U["EBITDA ajustado consolidado - 9 meses"]["valor"]), mi(U["EBITDA ajustado consolidado - 9 meses"]["anterior"])

# Gerdau: dívida líquida = (circulante + não circulante) - (caixa + aplicações); exclui arrendamentos
g_div = lambda k: mi(G["Empréstimos, financiamentos e debêntures - circulante"][k] + G["Empréstimos, financiamentos e debêntures - não circulante"][k])
g_cx = lambda k: mi(G["Caixa e equivalentes de caixa (balanço consolidado)"][k] + G["Aplicações financeiras circulantes (balanço consolidado)"][k])
g_dl, g_dl0 = g_div("valor") - g_cx("valor"), g_div("anterior") - g_cx("anterior")
u_dl, u_dl0 = mi(U["Dívida líquida em R$ mil (negativo = caixa líquido)"]["valor"]), mi(U["Dívida líquida em R$ mil (negativo = caixa líquido)"]["anterior"])
g_alav = g_dl / (g_ebt9 * 4 / 3)          # EBITDA 9M anualizado
u_alav = u_dl / (u_ebt9 * 4 / 3)

# Segmentos Gerdau
seg_g = {}
for s in ("Brasil", "América do Norte", "América do Sul"):
    r, e = G[f"Receita líquida - segmento {s}"], G[f"EBITDA ajustado - segmento {s}"]
    seg_g[s] = dict(rec=mi(r["valor"]), rec0=mi(r["anterior"]), ebt=mi(e["valor"]), ebt0=mi(e["anterior"]))
# Segmentos Usiminas (3T26 x 2T26, R$ milhões já)
seg_u = {}
for s, rk, ek in (("Siderurgia", "Receita líquida - Siderurgia", "EBITDA ajustado - Siderurgia"),
                  ("Mineração", "Receita líquida - Mineração", "EBITDA ajustado - Mineração")):
    seg_u[s] = dict(rec=U[rk]["valor"], rec0=U[rk]["anterior"], ebt=U[ek]["valor"], ebt0=U[ek]["anterior"])

vol, vol0 = U["Volume de vendas de aço"]["valor"], U["Volume de vendas de aço"]["anterior"]
rt = seg_u["Siderurgia"]["rec"] * 1000 / vol            # R$/t  (R$ mi / mil t * 1000)
rt_tt = seg_u["Siderurgia"]["rec0"] * 1000 / 989        # 2T26: volume 989 mil t (release, pág. 36)

margem = lambda e, r: e / r * 100
g_m, g_m0 = margem(g_ebt, g_rec), margem(g_ebt0, g_rec0)
u_m, u_m0 = margem(u_ebt, u_rec), margem(u_ebt0, u_rec0)
g_m9, g_m90 = margem(g_ebt9, g_rec9), margem(g_ebt90, g_rec90)
u_m9, u_m90 = margem(u_ebt9, u_rec9), margem(u_ebt90, u_rec90)

# ---- Tabela ----
linhas = [
    # (Métrica, Gerdau, Usiminas, origem)
    ("**3T26 contra 3T25 (A/A)**", "", "", ""),
    ("Receita líquida (R$ mi)", f"{br(g_rec)} ({sinal(pct(g_rec, g_rec0))})", f"{br(u_rec)} ({sinal(pct(u_rec, u_rec0))})", "ITR: Gerdau pág. 72; Usiminas pág. 26"),
    ("EBITDA ajustado (R$ mi)", f"{br(g_ebt)} ({sinal(pct(g_ebt, g_ebt0))})", f"{br(u_ebt)} ({sinal(pct(u_ebt, u_ebt0))})", "ITR: Gerdau pág. 72; Usiminas pág. 26"),
    ("Margem EBITDA ajustado", f"{br(g_m)}% (3T25: {br(g_m0)}%)", f"{br(u_m)}% (3T25: {br(u_m0)}%)", "calculado = EBITDA aj. / receita"),
    ("Lucro líquido consolidado (R$ mi)", f"{br(g_lucro)} ({sinal(pct(g_lucro, g_lucro0))})", f"{br(u_lucro)} (3T25: {br(u_lucro0)}; impairment de R$ 2.226 mi)", "ITR: Gerdau pág. 31; Usiminas pág. 29"),
    ("**Acumulado 9 meses (9M26 contra 9M25)**", "", "", ""),
    ("Receita líquida (R$ mi)", f"{br(g_rec9)} ({sinal(pct(g_rec9, g_rec90))})", f"{br(u_rec9)} ({sinal(pct(u_rec9, u_rec90))})", "ITR: Gerdau pág. 73; Usiminas pág. 45"),
    ("EBITDA ajustado (R$ mi)", f"{br(g_ebt9)} ({sinal(pct(g_ebt9, g_ebt90))})", f"{br(u_ebt9)} ({sinal(pct(u_ebt9, u_ebt90))})", "ITR: Gerdau pág. 73; Usiminas pág. 45"),
    ("Margem EBITDA ajustado", f"{br(g_m9)}% (9M25: {br(g_m90)}%)", f"{br(u_m9)}% (9M25: {br(u_m90)}%)", "calculado"),
    ("**Endividamento**", "", "", ""),
    ("Dívida líquida (R$ mi)", f"{br(g_dl)} em 30/09/26 (31/12/25: {br(g_dl0)})", f"{br(u_dl)} (caixa líquido; 3T25: {br(u_dl0)})", "Gerdau calculado (págs. 26-27); Usiminas pág. 32"),
    ("Dívida líquida / EBITDA (9M anualizado)", f"{br(g_alav, 2)}x", f"{br(u_alav, 2)}x", "calculado, mesmo critério para as duas"),
    ("**Siderurgia (só Usiminas divulga no ITR)**", "", "", ""),
    ("Volume de aço (mil t)", "não divulgado no ITR", f"{br(vol, 0)} ({sinal(pct(vol, vol0))} A/A)", "Usiminas pág. 24"),
    ("Receita líquida da Siderurgia por t (R$/t)", "n/d", f"{br(rt, 0)} ({sinal(pct(rt, rt_tt))} T/T)", "calculado = receita Siderurgia / volume"),
]

(AQUI / "tabela_comparativa.md").write_text(
    "# Gerdau × Usiminas — 3T26 (números consolidados, R$ milhões)\n\n"
    "EBITDA = EBITDA ajustado, conforme definição de cada empresa. Base A/A porque o ITR da Gerdau não traz o 2T26. "
    "Páginas = páginas do PDF do ITR.\n\n"
    "| Métrica | Gerdau | Usiminas | Origem |\n|---|---|---|---|\n"
    + "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in linhas) + "\n",
    encoding="utf-8")
with open(AQUI / "tabela_comparativa.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Métrica", "Gerdau", "Usiminas", "Origem"])
    w.writerows([[a.replace("**", ""), b, c, d] for a, b, c, d in linhas])

# ---- Gráficos ----
(AQUI / "graficos").mkdir(exist_ok=True)
plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "axes.edgecolor": GRADE, "text.color": INK})
AVISO = "Exercício acadêmico, não é recomendação de investimento."
FONTE = f"Fonte: ITR 3T26 (Gerdau, pág. 72; Usiminas, págs. 26 e 28), consolidado, EBITDA ajustado; margem calculada. {AVISO}"
FONTE_GERDAU = f"Fonte: ITR 3T26 da Gerdau, pág. 72 (nota 22, informações por segmento), em R$ milhões. {AVISO}"
FONTE_USIMINAS = f"Fonte: ITR 3T26 da Usiminas, pág. 33 (release, desempenho por unidade de negócio), em R$ milhões; margem calculada. {AVISO}"

def base(titulo, sub, w=11, h=6, fonte=None):
    fig, ax = plt.subplots(figsize=(w, h), dpi=160, facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRADE)
    ax.tick_params(colors=MUDO, length=0)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    fig.text(0.06, 0.94, titulo, fontsize=17, fontweight="bold", color=INK, ha="left")
    fig.text(0.06, 0.895, sub, fontsize=11, color=INK2, ha="left")
    fig.text(0.06, 0.02, fonte or FONTE, fontsize=8, color=MUDO, ha="left")
    return fig, ax

def barras_agrupadas(ax, grupos, series, cores, largura=0.34, fmt=lambda v: f"{br(v)}%"):
    """grupos: nomes no eixo x; series: [(rotulo, [valores por grupo])]"""
    n = len(series)
    for i, (rot, vals) in enumerate(series):
        xs = [k + (i - (n - 1) / 2) * (largura + 0.03) for k in range(len(grupos))]
        bars = ax.bar(xs, vals, width=largura, color=cores[i], label=rot, zorder=3)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + ax.get_ylim()[1] * 0.012, fmt(v), ha="center", va="bottom", fontsize=11, color=INK)
    ax.set_xticks(range(len(grupos))); ax.set_xticklabels(grupos, fontsize=12, color=INK2)

# 1) Margem EBITDA
fig, ax = base("Margem EBITDA: Gerdau subiu 5 p.p. e a Usiminas 2,4 p.p.", "Margem EBITDA ajustado = EBITDA ajustado / receita líquida, consolidado, 3T25 contra 3T26")
ax.set_ylim(0, 25); ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
xs = [0, 1]; larg = 0.30
for k, (m0, m1, cl, cs) in enumerate(((g_m0, g_m, AZUL_CLARO, AZUL), (u_m0, u_m, LARANJA_CLARO, LARANJA))):
    b0 = ax.bar(k - 0.17, m0, larg, color=cl, zorder=3); b1 = ax.bar(k + 0.17, m1, larg, color=cs, zorder=3)
    ax.text(k - 0.17, m0 + 0.3, f"{br(m0)}%", ha="center", fontsize=12, color=INK); ax.text(k + 0.17, m1 + 0.3, f"{br(m1)}%", ha="center", fontsize=12, color=INK, fontweight="bold")
    ax.text(k - 0.17, -1.6, "3T25", ha="center", fontsize=10, color=MUDO); ax.text(k + 0.17, -1.6, "3T26", ha="center", fontsize=10, color=MUDO)
ax.set_xticks(xs); ax.set_xticklabels(["Gerdau", "Usiminas"], fontsize=13, color=INK2); ax.tick_params(axis="x", pad=26)
fig.subplots_adjust(top=0.82, bottom=0.17, left=0.07, right=0.97)
fig.savefig(AQUI / "graficos" / "1_margem_ebitda.png"); plt.close(fig)

# 2) Variação A/A
fig, ax = base("Gerdau cresce receita e EBITDA; Usiminas perde receita, mas ganha EBITDA", "Variação 3T26 contra 3T25 (A/A), consolidado")
ax.yaxis.grid(False); ax.xaxis.grid(True, color=GRADE, linewidth=0.8)
rotulos = ["Gerdau: receita", "Gerdau: EBITDA aj.", "Usiminas: receita", "Usiminas: EBITDA aj."]
vals = [pct(g_rec, g_rec0), pct(g_ebt, g_ebt0), pct(u_rec, u_rec0), pct(u_ebt, u_ebt0)]
cores = [AZUL, AZUL, LARANJA, LARANJA]
ypos = [3, 2, 0.8, -0.2]
ax.barh(ypos, vals, height=0.6, color=cores, zorder=3)
for y, v in zip(ypos, vals):
    ax.text(v + (1 if v >= 0 else -1), y, sinal(v), va="center", ha="left" if v >= 0 else "right", fontsize=12, color=INK, fontweight="bold")
ax.set_yticks(ypos); ax.set_yticklabels(rotulos, fontsize=12, color=INK2)
ax.axvline(0, color=MUDO, linewidth=1, zorder=4); ax.set_xlim(-20, 50); ax.set_ylim(-0.9, 3.7)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.20, right=0.97)
fig.savefig(AQUI / "graficos" / "2_variacao_aa.png"); plt.close(fig)

# 3) Gerdau por segmento
nomes = ["Brasil", "América do Norte", "América do Sul"]
rec_tot = sum(seg_g[s]["rec"] for s in nomes); ebt_tot = sum(seg_g[s]["ebt"] for s in nomes)
fig, ax = base("A América do Norte gera 56% da receita da Gerdau e 76% do EBITDA", "Margem EBITDA ajustado por segmento, 3T25 contra 3T26 (R$ mi: receita / EBITDA)", fonte=FONTE_GERDAU)
ax.set_ylim(0, 33); ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
for k, s in enumerate(nomes):
    m0, m1 = margem(seg_g[s]["ebt0"], seg_g[s]["rec0"]), margem(seg_g[s]["ebt"], seg_g[s]["rec"])
    ax.bar(k - 0.17, m0, 0.30, color=AZUL_CLARO, zorder=3); ax.bar(k + 0.17, m1, 0.30, color=AZUL, zorder=3)
    ax.text(k - 0.17, m0 + 0.4, f"{br(m0)}%", ha="center", fontsize=12, color=INK); ax.text(k + 0.17, m1 + 0.4, f"{br(m1)}%", ha="center", fontsize=12, color=INK, fontweight="bold")
    ax.text(k, -4.6, f"{br(seg_g[s]['rec'], 0)} / {br(seg_g[s]['ebt'], 0)}", ha="center", fontsize=10, color=INK2)
    ax.text(k, -6.1, f"{seg_g[s]['rec']/rec_tot*100:.0f}% da receita · {seg_g[s]['ebt']/ebt_tot*100:.0f}% do EBITDA", ha="center", fontsize=9.5, color=MUDO)
ax.set_xticks(range(3)); ax.set_xticklabels(nomes, fontsize=13, color=INK2); ax.tick_params(axis="x", pad=8)
ax.text(0.99, 0.97, "claro = 3T25   escuro = 3T26", transform=ax.transAxes, ha="right", va="top", fontsize=10, color=MUDO)
fig.subplots_adjust(top=0.82, bottom=0.24, left=0.07, right=0.97)
fig.text(0.06, 0.055, "Participações calculadas sobre a soma dos três segmentos, antes das eliminações (EBITDA: Brasil + AmN + AmS).", fontsize=8, color=MUDO)
fig.savefig(AQUI / "graficos" / "3_gerdau_segmentos.png"); plt.close(fig)

# 4) Usiminas por segmento (T/T)
nomes_u = ["Siderurgia", "Mineração"]
fig, ax = base("Usiminas: margem cai 3 p.p. na Siderurgia e 5 p.p. na Mineração no trimestre", "Margem EBITDA ajustado por unidade de negócio, 2T26 contra 3T26 (comparação trimestre contra trimestre)", fonte=FONTE_USIMINAS)
ax.set_ylim(0, 18); ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
for k, s in enumerate(nomes_u):
    m0, m1 = margem(seg_u[s]["ebt0"], seg_u[s]["rec0"]), margem(seg_u[s]["ebt"], seg_u[s]["rec"])
    ax.bar(k - 0.17, m0, 0.30, color=LARANJA_CLARO, zorder=3); ax.bar(k + 0.17, m1, 0.30, color=LARANJA, zorder=3)
    ax.text(k - 0.17, m0 + 0.25, f"{br(m0)}%", ha="center", fontsize=12, color=INK); ax.text(k + 0.17, m1 + 0.25, f"{br(m1)}%", ha="center", fontsize=12, color=INK, fontweight="bold")
    ax.text(k, -2.3, f"EBITDA aj. R$ {br(seg_u[s]['ebt'], 0)} mi ({sinal(pct(seg_u[s]['ebt'], seg_u[s]['ebt0']), 0)} T/T)", ha="center", fontsize=10, color=INK2)
ax.set_xticks(range(2)); ax.set_xticklabels(nomes_u, fontsize=13, color=INK2); ax.tick_params(axis="x", pad=8)
ax.text(0.99, 0.97, "claro = 2T26   escuro = 3T26", transform=ax.transAxes, ha="right", va="top", fontsize=10, color=MUDO)
fig.subplots_adjust(top=0.82, bottom=0.17, left=0.07, right=0.97)
fig.savefig(AQUI / "graficos" / "4_usiminas_segmentos.png"); plt.close(fig)

print((AQUI / "tabela_comparativa.md").read_text(encoding="utf-8"))
print("margem Gerdau 3T26/3T25:", round(g_m, 2), round(g_m0, 2), "| Usiminas:", round(u_m, 2), round(u_m0, 2))
print("share NA receita/EBITDA:", round(seg_g["América do Norte"]["rec"] / rec_tot * 100, 1), round(seg_g["América do Norte"]["ebt"] / ebt_tot * 100, 1))
print("receita/t 3T26 e 2T26:", round(rt), round(rt_tt))
