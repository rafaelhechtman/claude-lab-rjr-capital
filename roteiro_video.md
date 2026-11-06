# Roteiro do vídeo (até 2 minutos)

Segue o roteiro do `entrega/CHECKLIST_ENTREGA.md` do repositório: **problema (~20s), solução funcionando (~60s), como verificamos (~20s), impacto e próximos passos (~20s)**. Todos os números abaixo são do ITR (com a página nos slides). O texto tem cerca de 290 palavras, que cabem em 2 minutos falando com calma. A banca assiste só até 2:00.

**Antes de gravar:** abra o artefato em tela cheia, ensaie uma vez e grave com qualquer gravador de tela (Loom, OBS, gravador do sistema ou celular). Uma gravação simples vale mais que uma editada. Mostre, não conte.

## 0:00 a 0:20 · O problema (na tela: slide 1)
> "O diretor de research pediu para comparar Gerdau e Usiminas no terceiro trimestre de 2026, em poucos slides, para o comitê de investimentos, com a página do ITR em cada número. O risco é comparar os consolidados e dizer que uma empresa é melhor, sem ver que os negócios são muito diferentes."

## 0:20 a 1:20 · A solução funcionando (na tela: slides 2, 4, 5 e 7)
> "Nossa resposta: a Gerdau teve o melhor trimestre operacional. Margem EBITDA ajustado de 20,2%, contra 9,0% da Usiminas, e EBITDA crescendo 37,8% contra 28,5%." *(slide 2)*
>
> "Mas o ponto central é por quê. 87% dessa diferença vem da América do Norte. Sem ela, a margem da Gerdau seria 10,5%, a 1,5 ponto da Usiminas. É geografia, não produto: a América do Sul, também de aço longo, tem margem de 11%." *(slide 4, gráfico da ponte)*
>
> "A Usiminas tem o balanço mais forte, com caixa líquido de 471 milhões, mas depende do Brasil: 86% da receita no mercado interno. Contra o segundo trimestre, o EBITDA caiu 27%, com o custo por tonelada subindo e a receita por tonelada parada." *(slide 5)*
>
> "Para o quarto trimestre, a Usiminas espera nova queda no aço, e a Gerdau, margem menor no Brasil." *(slide 7)*

## 1:20 a 1:40 · Como verificamos (na tela: slide 8, ou o terminal com o verificador)
> "Cada número foi extraído com página e trecho e conferido por um verificador automático contra o PDF: 55 números. Plantamos três erros de propósito e ele pegou os três. Somamos os segmentos da Gerdau e deu exatamente o consolidado. E pegamos erros do próprio Claude, como um título que dizia que a margem da Siderurgia da Usiminas se mantinha, quando tinha caído."

## 1:40 a 2:00 · Impacto e próximos passos (na tela: slide 8 ou o GitHub)
> "Para o comitê, isso responde quem foi melhor e por quê, sem esconder os limites. O fluxo roda com outros PDFs: é só trocar os ITRs e refazer as métricas. O próximo passo é automatizar tudo em um comando e incluir outros pares do setor. Não é recomendação de investimento."

## Se virem a pergunta "como vocês sabem que esse número está certo?" (finalistas)
Resposta curta: "O verificador confere trecho, valor, unidade e variação contra o PDF; a soma dos segmentos fecha com o consolidado; e as margens recalculadas batem com as divulgadas." Exemplo para mostrar: receita da Gerdau de R$ 18.690,5 mi (págs. 72 e 29) e margem da Usiminas de 9,0% (págs. 26 e 28).
