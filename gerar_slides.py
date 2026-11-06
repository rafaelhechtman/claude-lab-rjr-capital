"""
Case 3 - deck v3: 8 slides no formato do roteiro do repositório.

Estrutura (README do case + avancado/case3_resultados/roteiro_apresentacao.md):
 1 Capa  2 Resumo executivo  3 Tabela comparativa  4 Gráficos  5 Destaques por empresa
 6 Métricas do setor  7 Riscos e o que observar  8 Fontes e metodologia

Regras: título de cada slide = mensagem; todo número do ITR com a página do PDF, na forma [G72] (ITR da
Gerdau, pág. 72) ou [U26] (ITR da Usiminas, pág. 26); [calc] = cálculo nosso. Todo número dos slides é do ITR
ou calculado a partir dele: nenhum é digitado à mão, tudo vem de metricas_*.json (verificados contra os PDFs).
† e ‡ marcam só afirmações qualitativas de fora do ITR (release da Gerdau; analistas e dados setoriais), sem
números.

    python gerar_slides.py   ->  apresentacao.html (arquivo único) + notas_apresentador.md
"""
import base64
import json
from pathlib import Path

AQUI = Path(__file__).parent
def carregar(nome):
    return json.loads((AQUI / nome).read_text(encoding="utf-8"))
G = {m["metrica"]: m for m in carregar("metricas_gerdau.json")}
U = {m["metrica"]: m for m in carregar("metricas_usiminas.json")}

def br(x, c=1):
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def sg(x, c=1):
    return ("+" if x > 0 else "") + br(x, c) + "%"
def pct(a, b):
    return (a / b - 1) * 100
def mi(v):
    return v / 1000
def img(nome):
    return "data:image/png;base64," + base64.b64encode((AQUI / "graficos" / nome).read_bytes()).decode()
def p(*refs):
    return '<span class="pg">[' + " · ".join(refs) + "]</span>"
def par(d, k):
    return mi(d[k]["valor"]), mi(d[k]["anterior"])

# ------------------------------------------------------------------ números (R$ milhões)
g_rec, g_rec0 = par(G, "Receita líquida consolidada")
g_ebt, g_ebt0 = par(G, "EBITDA ajustado consolidado")
g_luc, g_luc0 = par(G, "Lucro líquido consolidado")
g_fin, g_fin0 = par(G, "Resultado financeiro líquido consolidado")
u_rec, u_rec0 = par(U, "Receita líquida consolidada")
u_ebt, u_ebt0 = par(U, "EBITDA ajustado consolidado")
u_luc, u_luc0 = par(U, "Lucro (prejuízo) líquido consolidado")
g_ebt9, g_rec9 = mi(G["EBITDA ajustado consolidado - 9 meses"]["valor"]), mi(G["Receita líquida consolidada - 9 meses"]["valor"])
u_ebt9 = mi(U["EBITDA ajustado consolidado - 9 meses"]["valor"])
mg = lambda e, r: e / r * 100
g_m, g_m0, u_m, u_m0 = mg(g_ebt, g_rec), mg(g_ebt0, g_rec0), mg(u_ebt, u_rec), mg(u_ebt0, u_rec0)

dv = lambda k: mi(G["Empréstimos, financiamentos e debêntures - circulante"][k] + G["Empréstimos, financiamentos e debêntures - não circulante"][k])
cx = lambda k: mi(G["Caixa e equivalentes de caixa (balanço consolidado)"][k] + G["Aplicações financeiras circulantes (balanço consolidado)"][k])
g_dl = dv("valor") - cx("valor")
u_dl = mi(U["Dívida líquida em R$ mil (negativo = caixa líquido)"]["valor"])
g_alav, u_alav = g_dl / (g_ebt9 * 4 / 3), u_dl / (u_ebt9 * 4 / 3)
g_pol = G["Política de alavancagem de longo prazo: dívida líquida/EBITDA abaixo de"]["valor"]
sens_preco = mi(G["Sensibilidade do resultado a 1% no preço dos produtos vendidos"]["valor"])
ajuste_nr = abs(mi(G["Ajuste não recorrente no EBITDA (recuperação de créditos / provisões)"]["valor"]))
g_hold = G["Receita líquida da HOLDING (NÃO usar na comparação - só controladora)"]["valor"] / 1000   # R$ bi

seg = {s: dict(rec=mi(G[f"Receita líquida - segmento {s}"]["valor"]), rec0=mi(G[f"Receita líquida - segmento {s}"]["anterior"]),
               ebt=mi(G[f"EBITDA ajustado - segmento {s}"]["valor"]), ebt0=mi(G[f"EBITDA ajustado - segmento {s}"]["anterior"]))
       for s in ("Brasil", "América do Norte", "América do Sul")}
rec_tot = sum(v["rec"] for v in seg.values()); ebt_tot = sum(v["ebt"] for v in seg.values())
an, br_, asul = seg["América do Norte"], seg["Brasil"], seg["América do Sul"]
sh = {k: v["rec"] / rec_tot * 100 for k, v in seg.items()}
sh_ebt_na = an["ebt"] / ebt_tot * 100
na_m, na_m0 = mg(an["ebt"], an["rec"]), mg(an["ebt0"], an["rec0"])
as_m, as_m0 = mg(asul["ebt"], asul["rec"]), mg(asul["ebt0"], asul["rec0"])
ex_r, ex_e = g_rec - an["rec"], g_ebt - an["ebt"]                      # Gerdau sem América do Norte
m_ex = ex_e / ex_r * 100
gap_tot = g_m - u_m
part_na = (g_m - m_ex) / gap_tot * 100

sd = {s: dict(rec=U[f"Receita líquida - {s}"]["valor"], rec0=U[f"Receita líquida - {s}"]["anterior"],
              ebt=U[f"EBITDA ajustado - {s}"]["valor"], ebt0=U[f"EBITDA ajustado - {s}"]["anterior"]) for s in ("Siderurgia", "Mineração")}
sid_m, sid_m0 = mg(sd["Siderurgia"]["ebt"], sd["Siderurgia"]["rec"]), mg(sd["Siderurgia"]["ebt0"], sd["Siderurgia"]["rec0"])
min_m = mg(sd["Mineração"]["ebt"], sd["Mineração"]["rec"])
u_int, u_int0 = par(U, "Receita líquida - mercado interno")
u_int_sh = u_int / u_rec * 100
min_sh = sd["Mineração"]["rec"] / (sd["Siderurgia"]["rec"] + sd["Mineração"]["rec"]) * 100
u_auto = U["Mercado interno de aço: participação do automotivo no volume"]["valor"]
u_dist = U["Mercado interno de aço: participação da grande rede (distribuição) no volume"]["valor"]
u_ind = U["Mercado interno de aço: participação da indústria no volume"]["valor"]
vol, vol0 = U["Volume de vendas de aço"]["valor"], U["Volume de vendas de aço"]["anterior"]
rt = sd["Siderurgia"]["rec"] * 1000 / vol
cpv_t = U["Custo por tonelada da Siderurgia (CPV/t)"]["valor"]
cpv_alta = U["Alta do custo por tonelada da Siderurgia, segundo a administração"]["valor"]
rec_t_queda = U["Queda da receita por tonelada da Siderurgia, segundo a administração"]["valor"]
u_ebt_tt = U["EBITDA ajustado consolidado - contra o 2T26"]
u_cpv, u_cpv0 = U["Custo dos produtos vendidos consolidado (negativo = custo)"]["valor"], U["Custo dos produtos vendidos consolidado (negativo = custo)"]["anterior"]
imp = mi(U["Impairment de ativos não financeiros (efeito pontual do 3T25)"]["valor"])
min_vol = U["Vendas de minério de ferro"]
min_preco = U["Queda do preço de referência do minério de ferro"]["valor"]
u_dbruta, u_dbruta_cp = mi(U["Dívida bruta total"]["valor"]), mi(U["Dívida bruta de curto prazo"]["valor"])
u_dur = U["Duração da dívida em reais (meses)"]["valor"]
n_metricas = len(G) + len(U)

# Marcadores de afirmações QUALITATIVAS de fora do ITR (nenhum número de fora do ITR entra nos slides):
# † = apresentação de resultados da Gerdau (release); ‡ = analistas e dados setoriais. Análises numéricas
# complementares com dados de fora do ITR ficam no README do GitHub, não no deck.
DAG, DAG2 = "†", "‡"
LEG = ("[G72] = ITR da Gerdau, pág. 72 · [U26] = ITR da Usiminas, pág. 26 (páginas do PDF) · [calc] = cálculo nosso · "
       "† e ‡ = afirmação qualitativa de fora do ITR (release da Gerdau; analistas e dados setoriais), sem números (slide 8)")

# ------------------------------------------------------------------ notas do apresentador (o que falar)
NOTAS = {
    1: ["Abra com a resposta, em uma frase: a Gerdau teve o melhor trimestre operacional e isso vem dos EUA; a Usiminas tem o balanço mais forte e depende do Brasil.",
        "Diga o escopo: ITRs do 3T26, números consolidados, comparação para o comitê. Não é recomendação de investimento."],
    2: ["Três conclusões, cada uma com um número: resultado (20,2% contra 9,0% de margem), causa (87% da diferença vem da América do Norte) e o que vem (caixa líquido da Usiminas, pressão no 4T).",
        "Se perguntarem 'quem é melhor': depende do critério. Em margem e crescimento do EBITDA, Gerdau. Em balanço, Usiminas."],
    3: ["Mesma unidade (R$ milhões), mesmo critério (consolidado, EBITDA ajustado de cada empresa), mesma base (A/A).",
        "Explique o asterisco: o lucro da Usiminas no 3T25 foi negativo por um impairment de R$ 2,2 bi, então a variação do lucro não é comparável.",
        "Mostre a coluna de páginas: todo número tem a página do ITR."],
    4: ["Esquerda: a margem sobe nas duas, 5,0 p.p. na Gerdau e 2,4 p.p. na Usiminas. A Usiminas melhora a margem com a receita caindo.",
        "Direita: a ponte. Sem a América do Norte, a Gerdau teria 10,5%, a 1,5 p.p. da Usiminas. Os EUA explicam 87% da diferença.",
        "Frase-chave: a diferença é geografia, não produto. A América do Sul, também de aço longo, tem margem de 11%."],
    5: ["Modelos diferentes: Gerdau é multirregional de aço longo; Usiminas é aço plano para o mercado brasileiro, com uma mineração pequena.",
        "Diferencial competitivo da Gerdau: a posição nos EUA, onde a margem é de 27,7%. Chame de diferencial de posicionamento com componente de proteção tarifária, não de 'moat' sem ressalva: parte do prêmio veio no último ano, com preço.",
        "Diferencial da Usiminas: o balanço (caixa líquido, pouca dívida no curto prazo). O ponto fraco é que o preço do aço plano não acompanha o custo.",
        "Negativos honestos: Brasil da Gerdau encolhe e a América do Sul perde margem; na Usiminas, custo por tonelada sobe, minério fraco."],
    6: ["Mensagem: os negócios são diferentes. A Gerdau tem 63% da receita fora do Brasil e a América do Norte com margem de 27,7%; a Usiminas tem 86% da receita no mercado interno e uma mineração com margem de 2,8%.",
        "Métricas do setor: o ITR da Gerdau não divulga volume nem preço por tonelada. Diga isso e mostre o que dá para medir na Usiminas: volume (-6,3%), receita por tonelada (R$ 5.426), custo por tonelada (R$ 4.849, +2,4% T/T).",
        "Dívida líquida / EBITDA: 0,57x contra -0,18x (caixa líquido), com o mesmo critério nas duas.",
        "A comparação por tonelada que fizemos com dados de fora do ITR está no README do GitHub, como análise complementar."],
    7: ["Setor: nos EUA, tarifa e demanda de data centers e energia sustentam preço; construção em geral está fraca. No Brasil, juros altos e importação pesam.",
        "Para a Gerdau, a construção brasileira é só uma parte do Brasil, que por sua vez é 37% da receita; então juros altos importam menos do que parece. Para a Usiminas, quase tudo é mercado interno.",
        "O que acompanhar: decisão do antidumping em dezembro, USMCA, 4T da Usiminas (moderada redução), minério."],
    8: ["Mostre o método: ITRs consolidados, EBITDA ajustado, R$ milhões, A/A. Mostre como verificamos: 54 números conferidos contra os PDFs.",
        "Seja franco sobre limites: todo número dos slides é do ITR; o que vem de fora do ITR (†, ‡) é só contexto qualitativo. Cite exemplos de onde o Claude errou e como pegamos.",
        "Pergunta provável: 'como vocês sabem que o número está certo?' Resposta: verificador, soma dos segmentos igual ao consolidado e margens recalculadas batem."],
}

# ------------------------------------------------------------------ HTML
def slide(n, titulo, corpo, fonte=""):
    notas = "<ul>" + "".join(f"<li>{x}</li>" for x in NOTAS[n]) + "</ul>"
    f = f'<div class="fonte">{fonte}</div>' if fonte else ""
    return (f'<section class="slide" id="s{n}"><h2>{titulo}</h2><div class="corpo">{corpo}</div>{f}'
            f'<div class="num">{n} / 8</div><aside class="notes"><b>O que falar</b>{notas}</aside></section>')

def dot(cor):
    return f'<span class="dot" style="background:{cor}"></span>'
AZ, LA = "#2a78d6", "#eb6834"

# 1 ---- capa
s1 = f"""<section class="slide capa" id="s1">
<div class="kicker">Claude Lab · Economia &amp; Finanças · PUC-Rio · 06/11/2026</div>
<h1>A Gerdau teve o melhor trimestre operacional porque tem os EUA; a Usiminas tem o balanço mais forte, mas depende do Brasil</h1>
<p class="sub">{dot(AZ)}Gerdau &nbsp;×&nbsp; {dot(LA)}Usiminas &nbsp;·&nbsp; Siderurgia, 3T26 (até 30/09/2026) &nbsp;·&nbsp; ITRs consolidados &nbsp;·&nbsp; material para o comitê de investimentos</p>
<p class="time">Time: RJR Capital</p>
<p class="aviso">Exercício acadêmico. Não constitui recomendação de investimento.</p>
<div class="num">1 / 8</div>
<aside class="notes"><b>O que falar</b><ul>{''.join(f'<li>{x}</li>' for x in NOTAS[1])}</ul></aside></section>"""

# 2 ---- resumo executivo
def card(titulo, grande, legenda, linhas, tam=None):
    st = f' style="font-size:{tam}px"' if tam else ""
    li = "".join(f"<li>{x}</li>" for x in linhas)
    return f'<div class="card"><h3>{titulo}</h3><div class="grande"{st}>{grande}</div><div class="leg">{legenda}</div><ul>{li}</ul></div>'
s2 = slide(2, "Três coisas que o comitê precisa saber",
    '<div class="grid3">'
    + card("1 · O resultado", f"{br(g_m)}% × {br(u_m)}%", f"margem EBITDA ajustado, Gerdau × Usiminas {p('G72', 'U26', 'U28')}",
           [f"EBITDA ajustado A/A: Gerdau {sg(pct(g_ebt, g_ebt0))} {p('G72')}; Usiminas {sg(pct(u_ebt, u_ebt0))} {p('U26')}",
            f"Receita A/A: Gerdau {sg(pct(g_rec, g_rec0))}; Usiminas {sg(pct(u_rec, u_rec0))}, com menos volume de aço ({sg(pct(vol, vol0))}) {p('G72', 'U26', 'U24')}"], tam=42)
    + card("2 · A causa", f"{br(part_na, 0)}%", f"da diferença de margem vem da América do Norte {p('G72', 'calc')}",
           [f"Sem os EUA, a margem da Gerdau seria {br(m_ex)}%, a {br(m_ex - u_m)} p.p. da Usiminas {p('G72', 'calc')}",
            f"É geografia, não produto: a América do Sul, também de aço longo {p('G74')}, tem margem de {br(as_m)}% {p('G72')}"])
    + card("3 · O que vem", f"R$ {br(abs(u_dl), 0)} mi", f"caixa líquido da Usiminas {p('U32')}",
           [f"Mas o EBITDA da Usiminas cai {br(abs(pct(u_ebt_tt['valor'], u_ebt_tt['anterior'])), 0)}% contra o 2T26 e a empresa espera nova queda no aço no 4T26 {p('U24', 'U23')}",
            f"Gerdau: dívida líquida de {br(g_alav, 2)}x o EBITDA {p('G26', 'G27', 'calc')}; margem estável nos EUA e menor no Brasil no 4T{DAG}"])
    + "</div>",
    LEG)

# 3 ---- tabela comparativa
def linha(rot, a, b, pg):
    return f"<tr><th>{rot}</th><td>{a}</td><td>{b}</td><td class=\"pgc\">{pg}</td></tr>"
tab = ('<table><thead><tr><th>3T26 contra 3T25 (A/A) · R$ milhões · consolidado</th><th>' + dot(AZ) + 'Gerdau</th><th>' + dot(LA) + 'Usiminas</th><th>Páginas do ITR</th></tr></thead><tbody>'
    + linha("Receita líquida", f"<b>{br(g_rec)}</b> <i>{sg(pct(g_rec, g_rec0))}</i>", f"<b>{br(u_rec)}</b> <i>{sg(pct(u_rec, u_rec0))}</i>", "G72 · U26")
    + linha("EBITDA ajustado", f"<b>{br(g_ebt)}</b> <i>{sg(pct(g_ebt, g_ebt0))}</i>", f"<b>{br(u_ebt)}</b> <i>{sg(pct(u_ebt, u_ebt0))}</i>", "G72 · U26")
    + linha("Margem EBITDA ajustado", f"<b>{br(g_m)}%</b> <i>era {br(g_m0)}%</i>", f"<b>{br(u_m)}%</b> <i>era {br(u_m0)}%</i>", "calc. de G72 · U26, U28")
    + linha("Lucro líquido", f"<b>{br(g_luc)}</b> <i>{sg(pct(g_luc, g_luc0))}</i>", f"<b>{br(u_luc)}</b> <i>era {br(u_luc0)}*</i>", "G31 · U29")
    + linha("Dívida líquida", f"<b>{br(g_dl)}</b> <i>calculada</i>", f"<b>{br(u_dl)}</b> <i>caixa líquido</i>", "G26, G27 · U32")
    + linha("Dívida líquida / EBITDA", f"<b>{br(g_alav, 2)}x</b>", f"<b>{br(u_alav, 2)}x</b>", "calc. de G73 · U45")
    + "</tbody></table>")
s3 = slide(3, "A Gerdau lidera em margem e no crescimento do EBITDA; a Usiminas, em caixa líquido", tab,
    f"* Prejuízo no 3T25 da Usiminas por impairment de R$ {br(imp, 0)} mi {p('U28')}: a variação do lucro não é comparável. "
    f"EBITDA = ajustado, definição de cada empresa; o da Gerdau inclui um ajuste de R$ {br(ajuste_nr)} mi {p('G72')}. "
    "Dívida líquida da Gerdau = empréstimos e debêntures menos caixa e aplicações. Dívida líquida / EBITDA com o EBITDA de 9 meses anualizado, mesmo critério nas duas. "
    "Base A/A porque o ITR da Gerdau não traz o 2T26. " + LEG)

# 4 ---- gráficos
s4 = slide(4, f"A margem da Gerdau é mais que o dobro da Usiminas, e {br(part_na, 0)}% dessa diferença vem da América do Norte",
    '<div class="duo w">'
    f'<div class="col"><img src="{img("7_receita_ebitda_margem.png")}" alt="Receita, EBITDA e margem, 3T26 e 3T25">'
    f'<p class="take">A margem sobe nas duas (Gerdau {br(g_m - g_m0)} p.p., Usiminas {br(u_m - u_m0)} p.p.); a da Usiminas melhora com a receita caindo {p("G72", "U26", "U28")}.</p></div>'
    f'<div class="col"><img src="{img("5_ponte_margem.png")}" alt="Ponte de margem da Usiminas até a Gerdau">'
    f'<p class="take">Sem a América do Norte, a Gerdau teria {br(m_ex)}% de margem, a {br(m_ex - u_m)} p.p. da Usiminas {p("G72", "calc")}.</p></div></div>',
    "Gerdau sem América do Norte = consolidado menos o segmento (cálculo nosso; as eliminações entre segmentos ficam no resto). " + LEG)

# 5 ---- destaques por empresa (qualitativo)
def sec(t):
    return f'<div class="mini">{t}</div>'
gerdau = (f'<div class="col txt"><h3>{dot(AZ)}Gerdau</h3>'
    + sec("Modelo")
    + f'<p>Líder em aço longo nas Américas; no Brasil também faz aço plano e minério para uso próprio {p("G37")}. Receita: {br(sh["América do Norte"], 0)}% EUA, {br(sh["Brasil"], 0)}% Brasil, {br(sh["América do Sul"], 0)}% América do Sul {p("G72", "calc")}.</p>'
    + sec("Diferencial competitivo")
    + f'<p>Nos EUA, a margem é de {br(na_m)}% (era {br(na_m0)}%) e responde por {br(sh_ebt_na, 0)}% do EBITDA dos segmentos {p("G72", "calc")}. É diferencial de posicionamento, com componente de proteção tarifária{DAG2}.</p>'
    + f'<p class="pos"><b>+</b> EBITDA ajustado {sg(pct(g_ebt, g_ebt0))} A/A e alavancagem baixa, de {br(g_alav, 2)}x o EBITDA {p("G72", "G26", "G27", "calc")}</p>'
    + f'<p class="neg"><b>−</b> Brasil: receita {sg(pct(br_["rec"], br_["rec0"]))} A/A {p("G72")}. América do Sul: margem de {br(as_m0)}% para {br(as_m)}% {p("G72")}. Resultado financeiro: {br(g_fin)} contra {br(g_fin0)} mi {p("G71")}</p></div>')
usim = (f'<div class="col txt"><h3>{dot(LA)}Usiminas</h3>'
    + sec("Modelo")
    + f'<p>Aço plano para o mercado interno ({br(u_int_sh, 0)}% da receita; automotivo {br(u_auto)}%, distribuição {br(u_dist)}% e indústria {br(u_ind)}% do volume interno) e minério ({br(min_sh, 0)}% da receita das duas unidades) {p("U26", "U33", "U37")}.</p>'
    + sec("Diferencial competitivo")
    + f'<p>Balanço: caixa líquido de R$ {br(abs(u_dl), 0)} mi, dívida bruta de R$ {br(u_dbruta / 1000)} bi com só R$ {br(u_dbruta_cp, 0)} mi no curto prazo {p("U32")} e hedge do preço do minério {p("U63")}. Mas a duração da dívida em reais é de só {br(u_dur, 0)} meses {p("U32")}.</p>'
    + f'<p class="pos"><b>+</b> EBITDA ajustado {sg(pct(u_ebt, u_ebt0))} A/A e margem de {br(u_m)}% (era {br(u_m0)}%) {p("U26", "U28")}; custo dos produtos vendidos {sg(pct(u_cpv, u_cpv0))} contra receita {sg(pct(u_rec, u_rec0))} {p("U26")}</p>'
    + f'<p class="neg"><b>−</b> Contra o 2T26, EBITDA {sg(pct(u_ebt_tt["valor"], u_ebt_tt["anterior"]), 0)}: custo por tonelada +{br(cpv_alta)}% (R$ {br(cpv_t, 0)}/t) e receita por tonelada −{br(rec_t_queda)}% {p("U23", "U38")}. Margem da Siderurgia de {br(sid_m0)}% para {br(sid_m)}% e da Mineração em {br(min_m)}%, com vendas de minério {sg(pct(min_vol["valor"], min_vol["anterior"]))} e uma planta parada {p("U33", "U34", "U23")}</p></div>')
s5 = slide(5, "Gerdau: os EUA compensam um Brasil que encolhe. Usiminas: caixa líquido, mas o custo sobe e o preço não acompanha",
    f'<div class="duo">{gerdau}{usim}</div>',
    "Margens da Siderurgia e da Mineração da Usiminas: EBITDA ajustado sobre receita de cada unidade, contra o 2T26 (a pág. 33 não traz o 3T25 por unidade). " + LEG)

# 6 ---- métricas do setor
def tile(grande, rot, nota, tam=None):
    st = f' style="font-size:{tam}px"' if tam else ""
    return f'<div class="tile"><div class="grande"{st}>{grande}</div><div class="rot">{rot}</div><div class="nota">{nota}</div></div>'
u_exp, u_exp0 = U["Exportações de aço (volume)"]["valor"], U["Exportações de aço (volume)"]["anterior"]
s6 = slide(6, f"Os negócios são diferentes: a Gerdau tem {br(100 - sh['Brasil'], 0)}% da receita fora do Brasil; a Usiminas, {br(u_int_sh, 0)}% no mercado interno",
    '<div class="duo">'
    f'<div class="col"><img src="{img("3_gerdau_segmentos.png")}" alt="Margem EBITDA por segmento da Gerdau"></div>'
    f'<div class="col"><img src="{img("4_usiminas_segmentos.png")}" alt="Margem EBITDA por unidade da Usiminas"></div></div>'
    '<div class="grid3 tiles3">'
    + tile(f"{sg(pct(vol, vol0))}", "Volume de aço vendido, Usiminas (A/A)", f"{br(vol, 0)} mil t {p('U24')}; exportação de aço {sg(pct(u_exp, u_exp0), 0)} {p('U36')}. O ITR da Gerdau não divulga volume")
    + tile(f"R$ {br(rt, 0)}/t", "Receita por tonelada, Siderurgia da Usiminas", f"{p('U24', 'U33', 'calc')}; custo por tonelada de R$ {br(cpv_t, 0)}, {sg(cpv_alta)} contra o 2T26 {p('U23', 'U38')}")
    + tile(f"{br(g_alav, 2)}x | {br(u_alav, 2)}x", "Dívida líquida / EBITDA, Gerdau | Usiminas", f"EBITDA de 9 meses anualizado, mesmo critério {p('G73', 'U45', 'calc')}")
    + '</div>',
    "Gráfico da esquerda: margem EBITDA ajustado por segmento da Gerdau, 3T25 e 3T26 (pág. 72). Gráfico da direita: margem por unidade da Usiminas, 2T26 e 3T26 (pág. 33, que não traz o 3T25 por unidade). "
    "Receita por tonelada = receita da Siderurgia ÷ volume de aço. Gerdau não divulga volume nem preço por tonelada no ITR. " + LEG)

# 7 ---- riscos e o que observar
def bl(t):
    return f"<li>{t}</li>"
s7 = slide(7, "O que observar no 4T26: o Brasil pressiona as duas; nos EUA, a margem da Gerdau depende de preço e tarifa",
    '<div class="duo riscos">'
    f'<div class="col txt"><h3>{dot(AZ)}Gerdau</h3>{sec("Drivers do setor")}<ul>'
    + bl(f"<b>EUA:</b> aço longo protegido por tarifa sobre o importado{DAG2}; a demanda é sustentada por data centers e energia{DAG}, não pela construção em geral{DAG2}")
    + bl(f"<b>Brasil:</b> a construção civil é um mercado relevante do segmento{DAG}; juros altos e importação limitam o crescimento{DAG}")
    + f'</ul>{sec("O que observar")}<ul>'
    + bl(f"<b>4T26:</b> margem estável nos EUA e compressão no Brasil (a empresa diz que não é guidance){DAG}")
    + bl(f"<b>Tarifas:</b> negociações do USMCA em curso, sem indicação concreta de mudança{DAG}; Midlothian deve começar a operar até o fim do ano, com mais oferta{DAG2}")
    + bl(f"<b>Sensibilidade:</b> cada 1% no preço do aço mexe ~R$ {br(sens_preco)} mi no resultado {p('G51')}")
    + '</ul></div>'
    f'<div class="col txt"><h3>{dot(LA)}Usiminas</h3>{sec("Drivers do setor")}<ul>'
    + bl(f"<b>Preço:</b> o aço plano segue o preço de importação{DAG2}; o antidumping do laminado a quente tem decisão em dezembro{DAG} e não alcança o aço embutido em bens importados{DAG2}")
    + bl(f"<b>Custo:</b> parte relevante em dólar (coque, placas) com receita em real; o repasse é lento porque o automotivo reajusta uma vez por ano{DAG2}")
    + f'</ul>{sec("O que observar")}<ul>'
    + bl(f"<b>Siderurgia:</b> a administração espera \"moderada redução\" no 4T26, com mix pior e custos pressionados {p('U23')}")
    + bl(f"<b>Minério:</b> preço de referência −{br(min_preco)}% e frete alto; vendas menores e uma planta parada {p('U23')}")
    + bl(f"<b>Automotivo ({br(u_auto)}% do volume interno {p('U37')}):</b> a produção de veículos cresce, mas importados e montagem com kits importados limitam o ganho para o aço nacional{DAG2}")
    + '</ul></div></div>',
    "Perspectiva da Gerdau: apresentação de resultados 3T26, que informa não constituir guidance. " + LEG)

# 8 ---- fontes e metodologia
s8 = slide(8, "Como chegamos aos números",
    '<div class="duo met"><div class="col txt"><h3>Fontes e critérios</h3><ul>'
    + bl("<b>Fonte:</b> ITRs do 3T26, consolidados, até 30/09/2026: Gerdau (80 págs.) e Usiminas (110 págs.). As páginas citadas são as do PDF")
    + bl(f"<b>Contábil × ajustado:</b> usamos o EBITDA ajustado de cada empresa. Gerdau: inclui o EBITDA proporcional das controladas em conjunto e exclui R$ {br(ajuste_nr)} mi de recuperação de créditos {p('G72')}. Usiminas: exclui a equivalência, inclui o EBITDA proporcional e exclui o impairment {p('U28')}")
    + bl("<b>Unidade e base:</b> R$ milhões (os ITRs estão em R$ mil). A/A é a base comum; T/T aparece só na Usiminas e sempre rotulado")
    + bl(f"<b>Efeitos pontuais:</b> impairment de R$ {br(imp, 0)} mi no 3T25 da Usiminas {p('U28')}; recuperação de R$ {br(ajuste_nr)} mi no EBITDA da Gerdau {p('G72')}")
    + bl(f"<b>Holding × consolidado:</b> o comentário de desempenho do ITR da Gerdau é da holding (receita de R$ {br(g_hold)} bi) {p('G3')}; usamos o consolidado (R$ {br(g_rec / 1000)} bi) {p('G72')}")
    + bl("<b>Só o ITR tem número:</b> todo número destes slides é do ITR (com página) ou calculado a partir dele. † e ‡ marcam só afirmações qualitativas de fora do ITR: † = apresentação de resultados da Gerdau; ‡ = analistas e dados setoriais")
    + '</ul></div>'
    '<div class="col txt"><h3>Como verificamos</h3><ul>'
    + bl(f"<b>{n_metricas} números do ITR</b> extraídos com página e trecho e conferidos pelo <code>verificar_numeros.py</code> contra o PDF")
    + bl("A soma dos segmentos da Gerdau mais as eliminações dá o consolidado (receita e EBITDA, nos dois anos); as margens recalculadas batem com as divulgadas pela Usiminas")
    + bl("<b>Onde o Claude errou e como pegamos:</b> título de gráfico que contradizia os números; câmbio como causa do ganho dos EUA (o relatório mostrou que atrapalhou); fonte de aço plano usada como evidência para aço longo")
    + bl("<b>Limite:</b> o ITR da Gerdau não traz volume nem mix de produto, então não comparamos por tonelada nem por tipo de aço nestes slides. Análises complementares com dados de fora do ITR estão no README do GitHub")
    + '</ul></div></div>'
    '<div class="aviso-box">Exercício acadêmico (Claude Lab · PUC-Rio). <b>Não constitui recomendação de investimento.</b></div>',
    "Fontes de fora do ITR, só para contexto qualitativo: apresentação de resultados 3T26 da Gerdau (6-K de 27/10/2026); relatórios da BTG Pactual (26/10 e 30/10/2026) e da Genial (30/10/2026); dados setoriais (AGC, Anfavea, Aço Brasil). " + LEG)

# ------------------------------------------------------------------ CSS / JS
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#1a1a19;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#0b0b0b;overflow:hidden}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center center}
.slide{position:absolute;inset:0;width:1280px;height:720px;background:#fcfcfb;padding:40px 60px 64px;display:none;flex-direction:column}
.slide.on{display:flex}
.kicker{font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:#898781;margin-bottom:10px}
h1{font-size:42px;line-height:1.15;font-weight:800;max-width:1120px}
h2{font-size:29px;line-height:1.18;font-weight:800;margin-bottom:16px;max-width:1160px}
h3{font-size:22px;margin-bottom:6px;font-weight:700}
.corpo{flex:1;display:flex;flex-direction:column;gap:14px;min-height:0}
.fonte{position:absolute;left:60px;right:130px;bottom:16px;font-size:10.5px;line-height:1.32;color:#898781}
.num{position:absolute;right:60px;bottom:16px;font-size:13px;color:#898781}
.pg{font-size:.7em;color:#898781;white-space:nowrap;font-weight:500}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;margin-right:8px;vertical-align:-1px}
.capa{justify-content:center;padding-left:80px}
.capa .kicker{margin-bottom:26px}
.capa .sub{font-size:21px;color:#52514e;margin-top:28px;max-width:1100px;line-height:1.35}
.capa .time{font-size:19px;margin-top:40px;color:#0b0b0b;font-weight:600}
.capa .aviso{font-size:15px;color:#898781;margin-top:12px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.corpo>.grid3{flex:1;margin-bottom:4px}
.card,.tile{background:#fff;border:1px solid #e1e0d9;border-radius:10px}
.card{display:flex;flex-direction:column;padding:24px 26px}
.card h3{color:#52514e;font-size:17px;text-transform:uppercase;letter-spacing:.04em}
.grande{font-size:50px;font-weight:800;line-height:1.05;margin:6px 0 4px;white-space:nowrap}
.leg{font-size:17px;color:#52514e;margin-bottom:16px;line-height:1.3}
.card ul,.col ul{list-style:none}
.card li,.col li{font-size:19px;line-height:1.35;margin-bottom:12px;padding-left:18px;position:relative}
.card li{font-size:21.5px;line-height:1.38;margin-bottom:16px}
.card .leg{font-size:18.5px}
.card li:before,.col li:before{content:"";position:absolute;left:0;top:.62em;width:7px;height:7px;border-radius:50%;background:#898781}
table{width:100%;border-collapse:collapse;font-size:22px}
th,td{padding:15px 14px;text-align:left;border-bottom:1px solid #e1e0d9}
thead th{font-size:16px;border-bottom:2px solid #c3c2b7;vertical-align:bottom}
tbody th{font-weight:500;color:#52514e;width:28%}
td b{font-weight:700}td i{font-style:normal;color:#52514e;font-size:17px;margin-left:6px}
td.pgc{font-size:15px;color:#898781;width:20%}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
.duo.w{grid-template-columns:1.32fr 1fr}
.duo img,.split img{width:100%;border:1px solid #e1e0d9;border-radius:8px;display:block}
.col img{margin-bottom:10px}
.col p{font-size:17px;line-height:1.35;margin-bottom:8px}
.take{font-size:20px!important;line-height:1.4;color:#0b0b0b;margin-top:8px}
.txt p,.txt li{font-size:16px;line-height:1.38}
.txt li{margin-bottom:8px}
#s5 .txt p{font-size:18px;margin-bottom:10px}
#s5 .mini{font-size:12.5px;margin:12px 0 4px}
#s7 .txt li{font-size:19px;margin-bottom:12px}
#s7 .mini{font-size:12.5px;margin:12px 0 5px}
#s8 .txt li{font-size:17px;margin-bottom:10px}
.txt p.pos b{color:#006300}.txt p.neg b{color:#d03b3b}
.mini{font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:#898781;margin:9px 0 3px;font-weight:700}
.split{display:grid;grid-template-columns:1.3fr 1fr;gap:24px;align-items:start}
.tiles{display:flex;flex-direction:column;gap:12px}
.tile{padding:18px 22px}
.tile .grande{font-size:40px;margin:0}
.tile .rot{font-size:17px;font-weight:600;margin-top:5px}
.tile .nota{font-size:15px;color:#52514e;margin-top:5px;line-height:1.38}
.corpo>.grid3.tiles3{flex:0 0 auto;margin-top:2px;gap:16px}
.tiles3 .tile{padding:12px 16px}
.tiles3 .grande{font-size:34px;margin:0}
.tiles3 .rot{font-size:15px;margin-top:3px}
.tiles3 .nota{font-size:13px;margin-top:3px;line-height:1.35}
.aviso-box{background:#f4f3ef;border-radius:8px;padding:12px 18px;font-size:16px;line-height:1.4}
code{background:#f4f3ef;padding:1px 5px;border-radius:4px;font-size:.92em}
.notes{display:none}
body.nt .slide.on .notes{display:block;position:absolute;left:60px;right:60px;bottom:44px;background:rgba(11,11,11,.93);color:#fff;padding:12px 18px 6px;border-radius:8px;font-size:14.5px;line-height:1.35;z-index:5}
.notes b{display:block;margin-bottom:5px;color:#9ec5f4}
.notes li{list-style:disc;margin:0 0 5px 18px;padding:0;font-size:14.5px}.notes li:before{display:none}
#hint{position:fixed;left:14px;bottom:10px;font-size:12px;color:#898781}
@media print{
 @page{size:1280px 720px;margin:0}
 html,body{background:#fff;overflow:visible;height:auto}
 #stage{position:static;transform:none!important;width:1280px;height:auto}
 .slide{display:flex!important;position:relative;page-break-after:always;break-after:page}
 .notes,#hint{display:none!important}
}
"""
JS = """
const slides=[...document.querySelectorAll('.slide')];let i=0;const st=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1280,innerHeight/720);st.style.transform='translate(-50%,-50%) scale('+s+')'}
function show(n){i=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,k)=>s.classList.toggle('on',k===i));try{history.replaceState(null,'','#'+(i+1))}catch(err){}}
addEventListener('resize',fit);fit();
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();show(i+1)}if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();show(i-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key==='n'||e.key==='N')document.body.classList.toggle('nt')});
st.addEventListener('click',e=>{const r=st.getBoundingClientRect();show(e.clientX<r.left+r.width/3?i-1:i+1)});
const fromHash=()=>(parseInt(location.hash.slice(1))||1)-1;
addEventListener('hashchange',()=>{const n=fromHash();if(n!==i)show(n)});
new ResizeObserver(fit).observe(document.documentElement);
show(fromHash());
"""
doc = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       f'<title>Gerdau × Usiminas, 3T26 | Claude Lab PUC-Rio</title><style>{CSS}</style></head><body>'
       f'<div id="stage">{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}</div>'
       f'<div id="hint">← → ou clique nas laterais navegam · N mostra o que falar</div><script>{JS}</script></body></html>')
(AQUI / "apresentacao.html").write_text(doc, encoding="utf-8")

titulos = ["Capa", "Resumo executivo", "Tabela comparativa", "Gráficos", "Destaques por empresa", "Métricas do setor", "Riscos e o que observar", "Fontes e metodologia"]
md = ["# Notas do apresentador: o que falar em cada slide", "",
      "Roteiro de fala (também aparece no deck: aperte N). Para o vídeo de 2 minutos, siga o checklist do repositório: problema (20s), solução funcionando (60s), como verificamos (20s), impacto e próximos passos (20s).", ""]
for n in range(1, 9):
    md += [f"## Slide {n}: {titulos[n - 1]}"] + [f"- {x}" for x in NOTAS[n]] + [""]
(AQUI / "notas_apresentador.md").write_text("\n".join(md), encoding="utf-8")
print("ok:", len(doc) // 1024, "KB;", n_metricas, "métricas verificadas")
