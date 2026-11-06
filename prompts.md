# Prompts principais que usamos com o Claude

São os prompts que sustentaram o trabalho, resumidos e na ordem em que foram usados. A redação exata variou durante a conversa; aqui estão na forma mais limpa, para quem quiser repetir o fluxo com outro trimestre ou outras empresas.

## 1. Plano de ataque
> Leia o README do case (cole o texto) e proponha um plano de ataque para a apresentação: etapas, o que entregar e em que ordem, e o que a banca vai olhar. Quero o resultado antes da execução.

## 2. Entender o negócio antes dos números
> Leia as notas de segmentos e o release de resultados dos dois ITRs. Resuma como cada empresa ganha dinheiro: produto, clientes, divisão por região ou unidade de negócio. Cite a página de cada afirmação e diga o que ainda não dá para saber pelo ITR.

## 3. Extração das métricas, com página e trecho
> Leia `saida/EMPRESA/` e gere `metricas_EMPRESA.json` no formato de `metricas_exemplo.json`, com `valor`, `valor_como_aparece`, `anterior`, `pagina` e `trecho` de cada número. Use só números consolidados, EBITDA ajustado e o valor como aparece no PDF (R$ mil ou R$ milhões, sem converter).

## 4. Verificação
> Rode `verificar_numeros.py` e corrija no JSON só os itens com ERRO, olhando a página indicada. Anote cada erro que o verificador pegou.

## 5. Conferência que o verificador não faz
> O verificador só confere se o trecho e o número existem na página. Some os segmentos mais as eliminações e compare com o consolidado, e recalcule as margens para comparar com as divulgadas. Se algo não bater, diga qual coluna foi atribuída errado.

## 6. Decomposição da diferença de margem
> Decomponha a margem consolidada da Gerdau por segmento. Quanto da diferença para a Usiminas vem da América do Norte? Mostre a ponte de margem (Usiminas, Gerdau sem América do Norte, efeito da América do Norte, Gerdau) e de onde veio o ganho de margem de um ano para o outro.

## 7. Contexto do setor, separando o que é fato do que é hipótese
> Pesquise o contexto recente do setor (importações, tarifas, minério, juros, automotivo, data centers) e cruze com os segmentos de cada empresa. Marque cada afirmação como [ITR p.X], [calc], [externo] ou [hipótese]. Se uma fonte não confirmar, diga que não achou; não preencha lacuna.

## 8. Gerar a apresentação
> Gere a apresentação seguindo `roteiro_apresentacao.md`, a partir só dos JSONs verificados (nenhum número digitado à mão). O título de cada slide é a mensagem. Todo número do ITR leva a página no formato [G72] ou [U26]; o que vier de fora do ITR leva marcador próprio. Inclua um slide de fontes e metodologia com contábil × ajustado, unidades e o aviso de que não é recomendação de investimento.

## 9. Revisão como o diretor
> Releia cada slide como o diretor de research: algum número sem página do ITR? Algum título que não diz nada? Alguma causa afirmada sem evidência? Alguma frase que o número desmente? Liste o que achar antes de corrigir.

## 10. Resumos de vídeo e relatórios de analistas
> Condense o que esse vídeo (ou relatório) diz sobre o trimestre e confira cada número contra o ITR. Aponte o que bate, o que não bate e o que é só opinião ou recomendação, que fica de fora do trabalho.

Onde o Claude errou ao longo desses passos e como cada erro foi pego está em [log_erros_claude.md](log_erros_claude.md).
