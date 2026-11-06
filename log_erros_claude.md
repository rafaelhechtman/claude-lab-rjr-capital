# Log: onde o Claude errou e como pegamos

Material para o vídeo e para o README do time (critério "rigor e verificação"). Só entram aqui erros que realmente aconteceram. Armadilhas que foram evitadas ficam em seção separada.

## Erros do Claude (aconteceram e foram corrigidos)

| # | O erro | Como foi pego | Correção |
|---|---|---|---|
| 1 | **Título de gráfico contradizia os números.** O gráfico 4 dizia "Usiminas: Siderurgia segura a margem", mas a margem da Siderurgia caiu de 12,8% para 9,6% e o EBITDA caiu 22% T/T. | Revisão visual do gráfico renderizado, comparando título com as barras | Título trocado por "margem cai 3 p.p. na Siderurgia e 5 p.p. na Mineração no trimestre" |
| 2 | **Dois números diferentes para a mesma conclusão.** Na conversa o Claude disse que a América do Norte é "~77%" do EBITDA da Gerdau. O gráfico calculava 76,4%. As duas bases são legítimas (sobre o consolidado ou sobre a soma dos segmentos), mas misturá-las dá número inconsistente. | Comparar o título do gráfico com a anotação calculada dentro dele | Padronizado na soma dos segmentos (76%), com nota de rodapé |
| 3 | **Afirmação sem evidência no slide.** O rascunho do resumo executivo dizia que o EBITDA da Usiminas "sobe com custo menor, não com receita maior". Era só uma hipótese levantada antes, nunca verificada. | Revisão do texto do slide contra o que está nos JSONs verificados | Frase trocada por fato verificado: custo dos produtos vendidos cai 9,7% enquanto a receita cai 6,1% (pág. 26) |
| 4 | **Destaque enganoso no slide 5.** O texto dizia que a Siderurgia da Usiminas "sustenta o resultado" e entrega "97% do total das duas unidades". O número é verdadeiro, mas esconde que o EBITDA da Siderurgia caiu 22% contra o 2T26. | Leitura do slide como o diretor leria, procurando o que o número esconde | Slide reescrito com a queda de margem das duas unidades |
| 5 | **Números digitados à mão no código** (EBITDA e volume do 2T26 no script dos slides), fora do JSON verificado. | Revisão do código do gerador de slides | Os dois números entraram no JSON, passaram no verificador e o script passou a ler de lá |

| 6 | **Causa afirmada sem evidência.** Ao incluir os volumes da Gerdau, o slide 6 dizia que o Brasil "vendeu menos por exportar menos". A apresentação só explica a variação contra o 2T26 (mercado interno +5,9%, exportação menor), não a queda de 14,6% contra o 3T25. | Releitura do slide contra o que a fonte diz de fato | Frase trocada pelo que a fonte sustenta, com a base (T/T) explícita |
| 7 | **Número sem fonte tratado como se tivesse.** Uma análise externa citava "465 mil t de aço plano da Gerdau no Brasil". Não está no ITR e não achei confirmação. | Busca no texto das 80 páginas do ITR e na apresentação de resultados | Não usado. Ordem de grandeza por conta própria: 30% do mix × 1.351 mil t ≈ 405 mil t, com a ressalva da empresa de que o mix é aproximado |

| 8 | **Fonte de aço plano usada como evidência para aço longo.** Uma matéria da Argus sobre pedidos ligados a data centers foi citada a favor da demanda pelo aço longo da Gerdau, mas ela trata de aço plano. | Releitura do título da matéria na hora de escrever o documento de drivers | Mantida só como sinal geral de demanda, com a ressalva de que é plano e de data incerta |
| 9 | **"Mercado externo" da Usiminas tratado como exportação de aço.** Os 14,3% da receita do ITR (pág. 26) incluem R$ 574 mi de minério; a exportação de aço é R$ 312 mi, ~5% da receita (pág. 33). | Conferência do segmento contra a tabela por unidade de negócio | Tabela de drivers corrigida |

| 10 | **Câmbio atribuído como causa sem evidência.** O slide 5 dizia que o ganho da América do Norte veio de "preço (e câmbio)". O relatório da BTG mostra preço em dólar +19% A/A, e a receita por tonelada em reais subiu só ~13%: o câmbio foi contra, não a favor. | Cruzar o relatório da BTG com a nossa receita por tonelada | Frase corrigida: preço em dólar +19%, em reais +13% por causa do real mais forte |

| 11 | **Conclusão incompleta e leitura parcial dos relatórios.** Eu disse que a melhora de margem A/A da Usiminas "veio do custo" e que a causa da queda de volume do Brasil da Gerdau não estava documentada. Também resumi os relatórios da BTG só pelo texto, sem notar que a página 3 era uma tabela em imagem. | Pergunta do usuário sobre a leitura dos relatórios; extração das imagens do PDF | A tabela mostra receita por tonelada +4% e custo por tonelada -3% (os dois contribuíram), e a exportação explica ~68% da queda de volume do Brasil da Gerdau |

| 12 | **Página do ITR citada com a numeração errada.** No PDF da Usiminas, o número impresso no rodapé é uma unidade menor que a página do PDF (a "PÁGINA 62 de 109" é a pág. 63 do PDF). Em mensagens da conversa citei o hedge do minério como "pág. 62" e as obras do imobilizado como "pág. 77"; as páginas do PDF são 63 e 78. Os arquivos e o deck sempre usaram a numeração do PDF. | Conferência do rodapé impresso nos textos extraídos, antes de fechar o deck, porque o case exige a página do ITR em cada número | Regra fixada: toda página citada é a do PDF (a mesma do mapa do README) |

| 13 | **Deck com números de fora do ITR, contra a regra do diretor.** O pedido do case diz "todo número precisa ter a página do ITR". A versão do deck publicada às 14h36 trazia volumes da Gerdau, preços de analistas e dados setoriais com marcador †/‡, mas ainda números sem página do ITR. Também deixamos passar que o formulário de entrega é um issue do GitHub (`entrega.yml`). | O usuário pediu para reler o README do repositório e seguir à risca; a releitura do README raiz, do formulário e do guia avançado mostrou as lacunas | Slides só com número do ITR (com página) ou calculado dele; contexto de fora do ITR só qualitativo; números externos ficaram na análise complementar do README; texto do formulário e roteiro do vídeo preparados |

## Verificador: limite que descobrimos
O `verificar_numeros.py` aprovou tudo de primeira, mas ele só confere se o trecho e o número existem na página. Não confere se o número está na linha ou coluna certa. Conferência extra que fizemos: segmentos + eliminações = consolidado (receita e EBITDA, 3T26 e 3T25) e margens recalculadas batem com as divulgadas pela Usiminas.

## Armadilha evitada (não foi erro)
**Holding ≠ consolidado.** O "comentário de desempenho" da Gerdau no ITR mostra receita de R$ 1.078,8 mi (pág. 3): é só a controladora. A consolidada é R$ 18.690,5 mi (pág. 29). O README do case já avisava disso. Usamos só a consolidada, e a da holding ficou no JSON marcada "NÃO usar".

Adicionar aqui qualquer novo erro que aparecer. Um erro por linha, com a evidência.
