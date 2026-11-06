---
name: apresentacao-resultados-trimestrais
description: Monta uma apresentação executiva de 8 slides comparando os resultados trimestrais de duas empresas a partir dos ITRs, com título-mensagem, página do ITR em cada número e verificação automática. Use quando pedirem para comparar resultados de duas empresas do mesmo setor para um comitê ou diretor.
---

# Apresentação de resultados trimestrais (padrão do time RJR Capital)

Formato que usamos no Case 3 do Claude Lab (Gerdau × Usiminas, 3T26). Siga as regras abaixo sempre.

## Regras de ouro
1. **Número só entra no slide depois de verificado.** Cada número vem de um JSON com `valor`, `valor_como_aparece`, `pagina` e `trecho` e passa no `verificar_numeros.py` contra o PDF. O texto do slide é escrito a partir dos JSONs, nunca de memória.
2. **Todo número com a página do ITR**, na forma `[G72]` (empresa G, pág. 72 do PDF) e `[calc]` quando for cálculo. Use a página do PDF, não a impressa no rodapé (em alguns ITRs elas diferem em uma unidade).
3. **Título de cada slide é a mensagem**, não o assunto ("A margem da Gerdau é mais que o dobro da Usiminas, e 87% da diferença vem da América do Norte", não "Margem EBITDA").
4. **Só consolidado, mesma unidade, mesmo critério.** Nunca holding. EBITDA ajustado de cada empresa, com o critério explicado. R$ milhões. Diga se a comparação é A/A ou T/T e mantenha uma base comum.
5. **Dado de fora do ITR não entra como número nos slides.** Contexto de release, analistas e setor entra só como afirmação qualitativa marcada (†, ‡). Números de fora do ITR ficam em análise complementar no README.
6. **Não afirmar causa sem evidência.** Separe fato [ITR], cálculo [calc], externo e hipótese. Releia cada slide como o diretor: número sem página? título vazio? frase que o número desmente?
7. **Aviso em toda entrega:** exercício acadêmico, não constitui recomendação de investimento. Ignore recomendações e preços-alvo de analistas.

## Os 8 slides
1. **Capa:** quem foi melhor no trimestre e por quê, em uma frase.
2. **Resumo executivo:** 3 conclusões, cada uma com um número (resultado, causa, o que vem).
3. **Tabela comparativa:** poucas linhas (receita, EBITDA ajustado, margem, lucro, dívida líquida, dívida líquida/EBITDA) com coluna de páginas e nota sobre efeitos pontuais.
4. **Gráficos:** receita, EBITDA e margem no trimestre e contra o mesmo trimestre do ano anterior, mais a ponte de margem (quanto da diferença vem de cada segmento).
5. **Destaques por empresa:** modelo de negócio, diferencial competitivo, um positivo e um negativo de cada.
6. **Métricas do setor:** volume, receita por tonelada (ou unidade equivalente) e dívida líquida/EBITDA; diga o que o ITR não divulga.
7. **Riscos e o que observar:** drivers do setor e o que acompanhar no próximo trimestre, por empresa.
8. **Fontes e metodologia:** páginas, contábil × ajustado, unidades, efeitos pontuais, holding × consolidado, como verificamos, erros do Claude pegos e aviso.

## Fluxo (um comando)
`python rodar_tudo.py <pasta_dos_PDFs>` extrai o texto por página, verifica os `metricas_*.json` contra o PDF, calcula e gera o deck. O deck só sai se **todos** os números passarem no verificador. Para outro trimestre ou outras empresas: troque os PDFs, refaça os `metricas_*.json` (extrair cada número com página e trecho) e rode de novo.

## Armadilhas que já pegamos
- Título de gráfico que contradiz os números.
- Câmbio ou custo apontado como causa sem a fonte dizer isso.
- Fonte de um tipo de produto usada como evidência para outro.
- Rótulo de "mercado externo" que inclui outra unidade de negócio.
- Página citada com a numeração do rodapé em vez da do PDF.
- O verificador só confere se o trecho e o número existem na página: some também os segmentos e recalcule as margens.
