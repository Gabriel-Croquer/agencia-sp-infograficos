---
paths:
  - "outputs/analises-dados/**"
  - "dados/**"
  - "REPORTAGENS/**"
---

# Regras para jornalismo de dados

Referencia: Piramide Invertida do Jornalismo de Dados (Paul Bradshaw).
O processo vai de dados brutos a historia publicavel em etapas sequenciais.

## 1. Conceber — de onde vem a pauta?

Antes de tocar nos dados, identifique a origem da pauta:
- Divulgacoes publicas de dados (orcamentos, censos, indicadores)
- Acesso exclusivo a bases ineditas
- Replicacao de materias anteriores com dados atualizados
- Acompanhamento de noticias (dado que complementa um fato)
- Perguntas investigativas ("quanto custa X?", "quantos casos de Y?")
- Denuncias e vazamentos
- Exploracao livre de bases abertas

Analise quais medidas os dados contem e, tao importante quanto, o que falta.

## 2. Compilar — reunir os dados

Fontes possiveis:
- Portais de dados abertos e publicacoes periodicas
- APIs governamentais e de servicos publicos
- Pesquisa avancada (Google Dataset Search, repositorios)
- Web scraping (quando nao ha alternativa estruturada)
- Conversao de dados nao estruturados (PDFs, imagens, tabelas em HTML)
- Crowdsourcing e levantamentos proprios

## 3. Limpar — tratar dados sujos

Ao receber uma base de dados:
1. Descreva a estrutura: colunas, tipos, volume de registros
2. Identifique problemas de qualidade:
   - Entradas duplicadas ou vazias
   - Formatacao incorreta (datas, numeros, textos misturados)
   - Nomes inconsistentes para a mesma entidade (ex: "SP", "S.P.", "Sao Paulo")
   - Dados corrompidos ou fora de faixa
3. Calcule estatisticas descritivas basicas
4. Documente o que foi limpo e como

## 4. Contextualizar — questionar a origem

Nunca use dados sem entender o contexto:
- Quem coletou esses dados? Com que proposito?
- Quando e como foram coletados? Qual a metodologia?
- O que mudou na forma de coleta ao longo do tempo?
- Adicione contexto relevante: populacao, inflacao, historico, demografia
- Um numero sozinho nao diz nada — sempre contextualize

## 5. Combinar — cruzar bases

- Cruze dados antigos com novos para identificar tendencias
- Combine bases diferentes para enriquecer a analise (ex: gastos + populacao = per capita)
- Correlacoes entre bases diferentes sao pautas poderosas

## 6. Questionar — prevenir vies

Esta etapa permeia TODAS as anteriores:
- Questione seus proprios pressupostos continuamente
- Evite vies de confirmacao: nao busque apenas dados que confirmem sua tese
- Pergunte: "o que poderia refutar minha hipotese?"
- Se o dado parece bom demais, desconfie e verifique

## Angulos jornalisticos com dados

Sempre pense em pelo menos 3 destes 7 angulos:
- **Escala**: Qual o tamanho disso? Quantifique o fenomeno
- **Mudanca/Tendencia**: Esta subindo ou caindo? Desde quando? Compare periodos
- **Ranking**: Quem lidera? Quem esta por ultimo? (top 10, piores 10)
- **Variacao/Desigualdade**: Ha disparidades regionais, de genero, raca, renda?
- **Exploracao**: O que os dados revelam que ninguem contou ainda?
- **Correlacao**: Dois fenomenos andam juntos? (cuidado: correlacao ≠ causalidade)
- **Problemas nos dados**: Os proprios erros e lacunas sao pauta (ex: falta de transparencia, dados incompletos)

Alem disso, sempre pense:
- **Impacto no cidadao**: O que isso significa para a vida da pessoa?
- **Comparacao**: Como SP se compara a outros estados/cidades?
- **Anomalia**: Algum dado foge do padrao? Por que?

## 7. Comunicar — do dado a historia

### Apresentacao de dados no texto
- Nunca jogue uma tabela crua no texto
- Traduza numeros em frases: "7 em cada 10 paulistas..." em vez de "70%"
- Use comparacoes concretas: "equivale a 3 estadios do Morumbi"
- Contextualize sempre: um numero sozinho nao diz nada
- Arredonde quando a precisao nao importa: "cerca de 2 milhoes" > "1.987.432"

### Formatos de comunicacao alem do texto
- Visualizacoes de dados (graficos, mapas) — use `/sugerir-viz`
- Estudos de caso pessoais: humanize o dado com historias reais
- Ferramentas interativas: calculadoras, simuladores ("descubra quanto voce...")
- Narrativas em formato passo-a-passo para dados complexos
