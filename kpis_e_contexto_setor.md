# KPIs de Gerdau × Usiminas à luz do modelo de negócio e do momento do setor

Análise para o time (versão 2, atualizada com a apresentação de resultados da Gerdau). Toda afirmação traz uma etiqueta de origem:

- **[ITR p.X]**: número verificado contra o PDF do ITR (está nos `metricas_*.json`).
- **[calc]**: cálculo nosso a partir de números verificados.
- **[release†]**: vem da [apresentação de resultados 3T26 da Gerdau](https://www.sec.gov/Archives/edgar/data/0001073404/000110465926118998/tm2628297d3_ex99-1.htm) (6-K de 27/10/2026), **fora do ITR**. Receita e EBITDA por segmento dela batem com o ITR, mas volumes e mix **não passaram pelo verificador** e devem ser conferidos no slide original. Estão em `dados_release_gerdau.json`.
- **[externo]**: imprensa, casas de análise ou dados setoriais (busca na web, nov/2026). Conferir na fonte primária.
- **[hipótese]**: leitura nossa, a testar.

## O que mudou em relação à versão anterior
- O volume de aço da Gerdau, que o ITR não traz, está na apresentação de resultados. Isso permitiu calcular EBITDA e receita por tonelada.
- A inferência de que o Brasil da Gerdau é "majoritariamente aço longo" agora tem base: ~70% longo e ~30% plano, aproximado [release†].
- A hipótese de que a diferença de margem vem da América do Norte foi **quantificada**: 87% da diferença.
- A ideia de que a margem alta vem do "aço longo" foi **corrigida**: a América do Sul também é 100% longo e tem margem de 11,1%. O prêmio é do mercado americano, não do produto.
- A ideia de que a construção civil americana está crescendo forte **não se sustentou** nas fontes que achei (seção 3).

## 1. Em uma frase
A Gerdau tem **63% da receita fora do Brasil** [calc] e **76% do EBITDA dos segmentos na América do Norte** [ITR p.72], onde vende aço longo a preços bem mais altos num mercado protegido por tarifa. A Usiminas é uma siderúrgica quase toda brasileira de aço plano, com mineração pequena [ITR p.33] e 38% do volume indo para o automotivo [ITR p.37]. **Fora dos EUA, as duas têm margens e EBITDA por tonelada parecidos.**

## 2. Modelo de negócio, lado a lado

| | Gerdau | Usiminas |
|---|---|---|
| Produto | Brasil: ~70% longo, ~30% plano, mais especiais [release†, ITR p.71]. América do Norte e América do Sul: 100% aço longo [release†] | Aço plano (a quente, a frio, revestidos) e minério [ITR p.33] |
| Cliente | Brasil: ~45% indústria/agro/outros, ~40% construção civil, ~15% automotivo. América do Norte: ~40% construção não residencial e infraestrutura, ~60% manufatura, energia e automotivo [release†, aprox.] | Automotivo 38%, grande rede 32%, indústria 30% do volume interno [ITR p.37] |
| Matéria-prima | Sucata [ITR p.37]; forno elétrico [conhecimento geral] | Minério, carvão e energia; usina integrada [conhecimento geral] |
| Receita por região | Brasil 37%, América do Norte 56%, América do Sul 8% [calc, ITR p.72] | Mercado interno 85,7%, externo 14,3% [calc, ITR p.26] |
| Volume 3T26 | Brasil 1.351 mil t, América do Norte 1.313, América do Sul 309 [release†] | Aço 1.034 mil t [ITR p.24] |
| Regulação | Tarifa de 50% sobre aço importado nos EUA [externo]; antidumping em curso no Brasil [release†] | Antidumping e defesa comercial em andamento no Brasil [ITR p.23] |

## 3. O que aconteceu no setor

**Brasil: demanda fraca, importação alta e sob disputa** 
- O acumulado de janeiro a agosto mostra importações de aço -20,2% e consumo aparente -4,2% [externo: [Aço Brasil](https://www.acobrasil.org.br/site/wp-content/uploads/2026/08/AcoBrasil_EM_Julho_2026.pdf)]. Já a Gerdau diz que, no 3T26, as importações subiram 19,8% contra o 2T26 (aço plano +33,8%) e o consumo aparente subiu 6,3% no trimestre [release†]. **São bases diferentes** (sequencial contra acumulado no ano), não uma contradição.
- A penetração de importados em 2026 é maior no aço plano (~21,6%) do que no longo (~13,5%), pelo gráfico da Gerdau [release†; a ordem das séries foi inferida do texto extraído e deve ser conferida]. Isso pesa mais para a Usiminas.
- A Usiminas cita importações de Vietnã, Coreia do Sul e Egito e carros montados com aço importado [ITR p.23]. A decisão sobre o antidumping do laminado a quente fica para dezembro [release†; [Genial](https://analisa.genialinvestimentos.com.br/acoes/USIM5/Usiminas-USIM5--3T26-Call-Caminho-Mais-Longo-para-a-Margem-do-Aco/)].
- A Gerdau aponta consumo pressionado por inflação e juros altos [release†].

**Estados Unidos: preço alto e demanda seletiva, não construção em alta**
- Tarifa de 50% sobre aço importado sustenta o preço interno [externo: [Steel Market Update](https://www.steelmarketupdate.com/2026/01/23/cru-fewer-imports-tighten-us-steel-supply-supporting-domestic-prices/)].
- Gasto total com construção nos EUA cai cerca de 3% ao ano; construção privada não residencial sem data centers cai 7,9% e data centers sobem 46% [externo: [AGC, jul/2026](https://www.agc.org/sites/default/files/users/user21902/Construction%20Spending%20July%202026.pdf); [CemNet](https://www.cemnet.com/News/story/181836/us-construction-spending-falls-3-2-in-june.html)]. As fontes divergem em alguns meses; confirmar no Census.
- Na Gerdau, o volume da América do Norte subiu só 1,5% A/A e caiu 2,5% T/T. A carteira de pedidos está acima da média histórica, sustentada por construção não residencial, data centers e energia renovável. A receita por tonelada em dólar subiu 4,7% no trimestre [release†]. **O ganho de margem veio de preço, não de volume.**

**Global: minério em queda e excesso de capacidade chinês** [externo]
- Minério de ferro no menor nível em mais de dois anos em outubro de 2026 ([IstoÉ Dinheiro](https://istoedinheiro.com.br/minerio-ferro-minima-dois-anos-demanda-china)); Pequim anunciou controle mais rígido de capacidade em maio ([Forbes Brasil](https://forbes.com.br/forbes-money/2026/05/minerio-de-ferro-amplia-perdas-apos-china-revelar-controle-mais-rigido-da-capacidade-siderurgica/)). Bate com a Usiminas: preço de referência do minério -7,9% e uma planta parada [ITR p.23].

## 4. Matriz de KPIs

| KPI | Gerdau | Usiminas | O que o modelo explica | Comparável? |
|---|---|---|---|---|
| Margem EBITDA ajustado | **20,2%** (era 15,2%) [ITR p.72, calc] | **9,0%** (era 6,6%) [ITR p.26, p.28] | Quase toda a diferença vem dos EUA (seção 5, H1) | Sim, com ressalva de mix |
| Margem ex-América do Norte (Gerdau) | **10,5%** [calc] | 9,0% | A 1,5 p.p. da Usiminas | Aproximação (eliminações no ex-NA) |
| EBITDA A/A | +37,8% [ITR p.72] | +28,5% [ITR p.26] | Gerdau: preço nos EUA. Usiminas: custo menor com receita menor | Sim |
| Receita A/A | +3,9% [ITR p.72] | -6,1% [ITR p.26] | Gerdau: América do Norte +14,5%, Brasil -9,7% | Sim |
| Receita fora do Brasil | 63% [calc] | 14% (mercado externo) [calc] | Diversificação contra o ciclo brasileiro | Sim, como risco |
| **EBITDA por tonelada** | **América do Norte R$ 2.217; Brasil R$ 549; América do Sul R$ 517** [calc, release†] | **Siderurgia R$ 520** [calc, ITR p.33, p.24] | Os EUA rendem ~4 vezes o resto; Brasil e Usiminas são equivalentes | Sim (volume da Gerdau é †) |
| Receita por tonelada | América do Norte R$ 8.006; Brasil R$ 5.143 (inclui minério e coprodutos) [calc, release†] | Siderurgia R$ 5.426 [calc] | Preço nos EUA ~56% acima do Brasil | Direção sim; nível com cautela |
| Volume A/A | Brasil -14,6%; América do Norte +1,5%; América do Sul +6,9% [calc, release†] | Aço -6,3% [ITR p.24] | Brasil encolhe nas duas; EUA estável | Direção |
| Margem do Brasil | Segmento Brasil 10,7% [ITR p.72] | Siderurgia 9,6% [ITR p.33] | Quase empatadas; mix diferente | Parcialmente |
| Depreciação / receita | 5,0% (Brasil 8,4%) [calc, ITR p.72] | 3,8% (Siderurgia 3,1%) [calc] | Explica margem bruta pior na Gerdau Brasil | Sim, para a margem bruta |
| Dívida líquida / EBITDA | 0,57x [calc]; a empresa reporta 0,58x [release†] | -0,18x (caixa líquido) [calc] | Folga de portfólio contra folga de balanço | Sim, critérios diferentes |
| Perspectiva 4T26 | América do Norte: margem estável. Brasil: compressão [release†] | "Moderada redução" na Siderurgia [ITR p.23] | As duas esperam pressão no Brasil | Direção |

## 5. Leitura integrada

**H1. A diferença de margem consolidada vem da América do Norte. [confirmada com números]**
Ponte de margem: Usiminas 9,0% → Gerdau sem América do Norte 10,5% (+1,5 p.p.) → efeito da América do Norte +9,7 p.p. → Gerdau 20,2%. **87% da diferença de 11,2 p.p. vem dos EUA.** No ano, a margem consolidada da Gerdau subiu 5,0 p.p.: +4,2 pela margem da América do Norte (19,8% → 27,7%), +0,7 por ela pesar mais na receita (51% → 56%) e ~0 pelo resto (10,4% → 10,5%). Detalhes em `estimativa_margem_segmentos.md`. *Ressalva:* o ex-América do Norte é consolidado menos o segmento, com as eliminações entre segmentos todas no resto.

**H2. O prêmio é do mercado americano, não do aço longo. [novo]** A América do Sul é 100% aço longo e tem margem de 11,1% e EBITDA de R$ 517/t. O Brasil, ~70% longo, tem 10,7% e R$ 549/t. Só os EUA fogem do padrão. Estimativa para o aço longo no Brasil: ~11% (9,8% a 12,7% conforme a margem assumida para o plano), muito abaixo dos 27,7% dos EUA. Não depende do peso do plano.

**H3. Poder de preço nos EUA, mas com tarifa e pico de ciclo. [parcialmente sustentada]** A América do Norte vende a R$ 8.006/t contra R$ 5.143/t no Brasil, e o volume mal subiu. Já havia um prêmio estrutural no 3T25 (19,8% contra ~10,4% do resto), mas cerca de 8 p.p. a mais vieram em um ano, e a margem de 27,7% é a maior em quatro anos [release†]. A tarifa de 50% é política pública. O USMCA está em negociação, sem indicação concreta de mudança [release†]. *Não dá para separar poder de barganha estrutural de proteção tarifária só com esses dados.*

**H4. "Construção civil crescendo forte nos EUA" não é o motor. [não sustentada]** O gasto com construção está em queda; só data centers crescem forte [externo]. Na Gerdau, só ~40% das vendas da América do Norte vão para construção não residencial e infraestrutura [release†]. O ganho veio de preço, com volume +1,5% A/A.

**H5. A Usiminas melhorou margem A/A com receita consolidada menor, e veio de preço e de custo por tonelada, na Siderurgia.** Custo dos produtos vendidos -9,7% contra receita -6,1% [ITR p.26]. Pela tabela da BTG [externo, lida de imagem], a receita da Siderurgia por tonelada subiu 4% A/A (R$ 5.240 para R$ 5.426) e o custo por tonelada caiu 3% (R$ 4.982 para R$ 4.850); a receita consolidada caiu por volume (-6%), exportação (-51%) e mineração. O EBITDA da Siderurgia foi de R$ 308 mi para R$ 538 mi (+75%). Em T/T, o EBITDA da Siderurgia cai 22% e a margem vai de 12,8% para 9,6% [ITR p.33].

**H6. Demanda brasileira fraca; a Usiminas está mais exposta.** 85,7% da receita no mercado interno, 38% do volume para o automotivo e penetração de importados maior no plano (~21,6% contra ~13,5%) [calc, ITR p.37, release†]. O Brasil da Gerdau também sofre (receita -9,7%, volume -14,6%), mas tem os EUA para compensar.

**H7. Dois tipos de resiliência.** A Usiminas tem folga de balanço (caixa líquido de R$ 471 mi). A Gerdau tem folga de portfólio (63% da receita fora do Brasil) e alavancagem de 0,57x.

**H8. Riscos distintos.** Gerdau: tarifa americana e USMCA, preço do aço (1% = ~R$ 187 mi [ITR p.51]), insumos (carvão e sucata). Usiminas: defesa comercial no Brasil, minério e custo de insumos [ITR p.23].

## 6. O que não comparar
- **Margem bruta** entre as duas: a depreciação entra no custo e pesa diferente.
- **Variação do lucro líquido** contra o 3T25 da Usiminas: há impairment de R$ 2.226 mi [ITR p.28].
- **Receita por tonelada em nível** entre Gerdau Brasil e Usiminas: a da Gerdau inclui minério e coprodutos.
- **"Aço plano da Gerdau no Brasil" como número exato:** o mix de 30% é aproximado e a própria empresa ressalva que não se refere aos volumes do 3T26. O "465 mil t" de outra análise não tem fonte; 30% × 1.351 mil t dá ~405 mil t em ordem de grandeza.

## 7. Pontos de atenção sobre as fontes
- **Volumes e mix da Gerdau** vêm de texto extraído da apresentação. Conferir no slide original (volumes: slides 9, 11 e 12; mix: slides 9 e 11; importados: slide 10; perspectiva: slide 5).
- **Penetração de importados:** a ordem das três séries (plano, longo, total) foi inferida do texto extraído.
- **Genial:** cita queda de 12,9% no EBITDA da Siderurgia da Usiminas "sem extraordinários"; o release mostra -22% (538 contra 688). Usar o do ITR.
- **Causa da queda de volume do Brasil da Gerdau contra o 3T25 (-14,6%):** a apresentação só explica a variação contra o 2T26 (mercado interno +5,9%, exportação menor). Não afirmar a causa anual.
- **Reportagem da Argus** sobre carteira de pedidos: data incerta; usei a apresentação oficial no lugar.

## 8. O que ainda falta
- Capex e caixa livre das duas (a Gerdau reporta caixa livre de R$ 1,4 bi no 3T26 [release†]; falta o equivalente da Usiminas e a conferência).
- Decomposição do custo da Usiminas.
- Spreads de aço contra sucata (Gerdau) e contra minério e carvão (Usiminas).
- Margem do aço plano da Gerdau: não divulgada; só a estimativa por cenário.

## 9. Atualização com os relatórios da BTG (fonte externa, `dados_btg.json`)
Relatórios de equity research da BTG sobre os dois resultados do 3T26. Recomendações e preços-alvo foram ignorados.

**Confirmam números nossos:** EBITDA da Gerdau de R$ 3,77 bi e margem da América do Norte de 27,7%; dívida líquida da Gerdau de R$ 7,69 bi (nosso cálculo deu R$ 7.685,8 mi); FCF de R$ 1,44 bi e capex de R$ 1,1 bi; preço de R$ 5.426/t e custo de R$ 4.849/t da Siderurgia da Usiminas; EBITDA da Mineração de R$ 19 mi; FCF de -R$ 36 mi e caixa líquido de R$ 471 mi.

**Dados novos:**
- **Gerdau, América do Norte:** preço realizado de **US$ 1.570/t, +5% T/T e +19% A/A**, com vendas -3% T/T. Isso responde de onde veio a margem: preço em dólar.
- **Gerdau, câmbio:** a receita por tonelada em reais subiu só ~13% A/A [calc: R$ 8.006 contra R$ 7.104], contra +19% em dólar. O real mais forte **tirou** parte do ganho; não ajudou. (Corrige a frase anterior do deck, "preço e câmbio".)
- **Gerdau, Brasil:** mercado interno de 1,18 Mt (+6% T/T, ~87% do volume) e exportação de 172 mil t (-28% T/T), por decisão estratégica de exportar menos. Preço no mercado interno +2% T/T. A BTG não abre a queda de 14,6% A/A.
- **Gerdau, EUA:** carteira de pedidos acima de 100 dias (o release diz só "acima da média histórica"). Para a BTG, uma depreciação de 10% do real aumentaria o EBITDA em ~15%, porque mais de 75% do EBITDA vem dos EUA.
- **Usiminas, Siderurgia:** EBITDA **+75% A/A** (R$ 538 mi), dado que não tínhamos por unidade. O ITR só traz a comparação com o 2T26.
- **Usiminas, minério:** preço realizado de US$ 64,5/t úmida (-6% T/T), pressionado pelo frete; custo caixa de US$ 23,8/t; o preço do minério piorou mais no 4T26.
- **Perspectiva:** a BTG também vê pressão no 4T26 nas duas, com espaço limitado de recuperação da Usiminas pela concorrência de importados.

**Tabelas da página 3 (lidas de imagem, `dados_btg.json`):**
- **Volume do Brasil da Gerdau A/A (-15%):** a exportação caiu 48% (330 para 172 mil t, -158 mil t) e o mercado interno caiu 6% (1.252 para 1.179 mil t, -73 mil t). **A exportação explica ~68% da queda.** Isso resolve a pendência sobre a causa da queda anual.
- **Exportar menos melhora o mix:** a exportação do Brasil vende a R$ 4.000/t e o mercado interno a R$ 5.310/t (+33%). O preço doméstico subiu 2% T/T e 2% A/A.
- **Câmbio médio:** R$ 5,14 no 3T26 contra R$ 5,38 no 3T25. O real mais forte reduz a receita em reais da operação americana; confirma que o câmbio atrapalhou.
- **Resultado financeiro da Gerdau:** -R$ 431 mi (era -R$ 308 mi no 2T26 e -R$ 223 mi no 3T25), bem pior que o estimado pela BTG (-R$ 220 mi). Por isso o lucro líquido de R$ 1.563 mi ficou 13% abaixo da estimativa, enquanto o EBITDA ficou em linha.
- **Mineração da Usiminas A/A:** EBITDA de R$ 130 mi para R$ 19 mi (-85%), com volume -20% e preço realizado -7%.
- **Preço doméstico da Usiminas:** R$ 5.412/t, +3% A/A e -1% T/T. O da Gerdau Brasil sobe 2% nos dois períodos.

**O que a BTG não explica:** a causa da alta de custo da Usiminas. Ela só fala em "pressões de custos contínuas".

**Divergência aparente, sem conflito:** a Genial cita preço doméstico da Usiminas de R$ 5.412/t (-0,7% T/T), e a BTG, R$ 5.426/t (estável). O primeiro é só mercado interno; o segundo, a média com exportação, que bate com o nosso cálculo.
