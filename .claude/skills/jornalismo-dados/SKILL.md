---
name: jornalismo-dados
description: Analisa bases de dados e encontra historias jornalisticas. Use quando receber um CSV, Excel ou base de dados para analisar e encontrar pautas.
argument-hint: "[caminho para base de dados]"
allowed-tools: Read, Write, Glob, Grep, Bash, Edit
---

# Skill: Jornalismo de dados

## Ao receber uma base de dados

### 1. Reconhecimento (sempre primeiro)
- Leia as primeiras linhas para entender a estrutura
- Liste colunas, tipos de dados, volume de registros
- Identifique o que cada coluna representa
- Verifique qualidade: nulos, duplicatas, inconsistencias, encodings

### 2. Analise exploratoria
- Estatisticas descritivas: media, mediana, min, max, desvio padrao
- Distribuicao das variaveis principais
- Serie temporal se houver coluna de data
- Agrupamentos por categorias relevantes (regiao, tipo, orgao)

### 3. Caca as historias — Os 7 angulos do jornalismo de dados

Baseado na metodologia de Paul Bradshaw (Online Journalism Blog), que analisou
100 reportagens de dados e identificou 7 angulos recorrentes. Ao analisar
qualquer base de dados, passe sistematicamente por TODOS os 7 angulos abaixo
e avalie se ha historia em cada um.

---

#### ANGULO 1: ESCALA (Scale)

Identifica o TAMANHO de um problema ou fenomeno. E o angulo mais simples
e um dos mais eficazes.

**O que procurar:**
- Numeros absolutos grandes ou surpreendentes
- Totais que revelam a dimensao de um problema
- Somas que o publico desconhece

**Cuidado critico:** Um numero grande sozinho nao diz nada. SEMPRE contextualize:
- Use proporcoes: "1 em cada 5 paulistas..."
- Compare com algo tangivel: "o equivalente ao salario de 500 professores"
- Calcule per capita, por habitante, por escola, por leito
- Mostre a porcentagem do total

**Exemplo de lide:** "Sao Paulo gastou R$ 3,2 bilhoes com horas extras no funcionalismo em 2025 — o equivalente a construir 40 hospitais"

---

#### ANGULO 2: MUDANCA E ESTAGNACAO (Change & Stasis)

Mudanca e inerentemente noticia — ela fornece o verbo do titulo.
Mas a AUSENCIA de mudanca tambem pode ser noticia.

**O que procurar:**
- Comparacoes ano a ano, mes a mes, governo a governo
- Algo subindo ou caindo de forma acentuada?
- Algo que DEVERIA ter mudado mas NAO mudou? (estagnacao apos investimento)
- Algo que mudou quando nao deveria? (piora apos promessa)

**Cuidados criticos:**
- SAZONALIDADE: padroes sazonais mascaram mudancas reais. Prefira comparacao
  com mesmo periodo do ano anterior, nao com o mes anterior
- MARGEM DE ERRO: se a mudanca esta dentro da margem de erro estatistica,
  NAO reporte como mudanca real
- Sempre investigue o POR QUE da mudanca — o dado mostra O QUE mudou,
  a apuracao descobre POR QUE

**Exemplo de lide:** "Mortes no transito em SP caem 23% em um ano — mas interior concentra 7 em cada 10 obitos"

---

#### ANGULO 3: RANKING E OUTLIERS

Identifica QUEM esta no topo e QUEM esta na lanterna. Quem se destaca
positiva ou negativamente.

**O que procurar:**
- Top 10 e bottom 10 de cada metrica
- Quem gasta mais? Quem atende mais? Quem cresce mais?
- Municipios, orgaos ou categorias com desempenho extremo
- Outliers: valores que destoam muito da media

**Cuidado critico:** Rankings enganam sem contexto.
- A cidade com mais crimes pode ser simplesmente a mais populosa — use taxa per capita
- O hospital com mais mortes pode ser o que recebe os casos mais graves
- Datas de registro afetam dados (mortes por COVID puxavam nas tercas porque
  fins de semana subnotificavam)
- Sempre pergunte: "esse ranking muda se eu normalizar os dados?"

**Exemplo de lide:** "Guarulhos lidera ranking de filas no SUS em SP — pacientes esperam em media 87 dias por consulta com especialista"

---

#### ANGULO 4: VARIACAO E DESIGUALDADE (Variation)

Diferente do ranking (que mostra quem esta em cima/embaixo), a variacao
lidera pela PROPRIA EXISTENCIA de diferencas amplas. Funciona melhor quando
esperamos tratamento igual.

**O que procurar:**
- "Loterias do CEP": acesso desigual a servicos publicos por regiao
- Disparidades regionais: capital vs interior, centro vs periferia
- Tratamento desigual por genero, raca, renda, idade
- Vieses algoritmicos: sistemas que deveriam ser neutros mas discriminam
- Gaps de infraestrutura: demanda vs oferta por regiao

**Exemplo de lide:** "Chance de conseguir vaga em creche publica varia de 95% na zona oeste a 31% na zona leste de SP"

---

#### ANGULO 5: EXPLORATORIO

Historias que convidam o leitor a EXPLORAR os dados por conta propria
ou que examinam multiplos aspectos de uma questao.

**Duas categorias:**

1. **Interativos com call-to-action**: quizzes, calculadoras, mapas
   navegaveis, simuladores
   - "Descubra quanto seu municipio recebe do governo estadual"
   - "Calcule quanto voce economizaria com a nova lei"
   - "Veja como esta a escola do seu filho no ranking"

2. **Features exploratorios**: materias longas que combinam varios angulos
   e respondem multiplas perguntas sobre um tema
   - "Entenda em 5 graficos como mudou a seguranca publica em SP"
   - Materias que misturam escala + mudanca + ranking num pacote completo

**Quando usar:** Quando os dados sao ricos demais para uma unica historia
e o leitor ganha ao poder personalizar a consulta.

---

#### ANGULO 6: RELACAO E CORRELACAO

Busca conexoes entre diferentes conjuntos de dados. MAXIMO CUIDADO aqui.

**O que procurar:**
- Duas variaveis que sobem ou descem juntas
- Cruzamento entre bases diferentes (ex: investimento em educacao vs notas do IDEB)
- Redes: conexoes entre pessoas, empresas, doacoes, cargos

**Cuidado critico ESSENCIAL:**
- CORRELACAO NAO E CAUSALIDADE. Nunca escreva "X causou Y" baseado apenas
  em dados. Duas coisas podem subir juntas por coincidencia
- Para sugerir relacao, voce precisa de: dados + apuracao + fontes especialistas
- Analise de redes (quem conhece quem, quem doou para quem) revela conexoes
  mas raramente prova causalidade — use como direcao de investigacao

**Exemplo de lide (cauteloso):** "Municipios que mais investiram em saneamento nos ultimos 5 anos tiveram queda de ate 40% nas internacoes por doencas hidricas, aponta levantamento"

---

#### ANGULO 7: DADOS RUINS, DADOS AUSENTES E "CRIE O DADO"

As vezes a propria QUALIDADE ou AUSENCIA dos dados e a historia.

**Tres subcategorias:**

1. **Dados ruins (bad data):** bases com erros que afetam politicas publicas
   - Estatisticas manipuladas ou subnotificadas
   - Vieses em algoritmos de decisao publica
   - Dados que nao refletem a realidade

2. **Dados ausentes (no data):** a falta de dados revela negligencia institucional
   - "Governo nao monitora X" e noticia
   - Lidere com "preocupacoes levantadas", nao com a ausencia em si
   - A falta de registro nao significa que o problema nao existe — significa
     que o governo falhou em medi-lo

3. **Crie o dado (get the data):** quando o dado nao existe, construa-o
   - Compilar bases proprias a partir de documentos dispersos
   - Raspagem de dados de portais publicos
   - Pedidos de LAI sistematicos para construir series historicas
   - Bases abertas geram engajamento e credibilidade

**Exemplo de lide:** "Estado de SP nao tem dados unificados sobre tempo de espera em UPAs — levantamento da Agencia SP revela filas de ate 6 horas"

---

### 4. Bonus: Dado como direcao de investigacao

Dados podem apontar para PESSOAS, LUGARES ou ORGANIZACOES que merecem
reportagem tradicional. O dado identifica o outlier, o reporter vai ate la.

- Use outliers para escolher estudos de caso
- "A escola com pior nota do IDEB em SP" → visite, ouça professores, entenda o contexto
- O dado abre a porta; a apuracao conta a historia

---

### 5. Checklist obrigatorio

Ao analisar qualquer base, responda:

- [ ] **ESCALA:** Os numeros totais surpreendem? Como contextualizar?
- [ ] **MUDANCA:** O que mudou? O que nao mudou e deveria?
- [ ] **RANKING:** Quem lidera e quem esta na lanterna?
- [ ] **VARIACAO:** Ha desigualdades ou "loterias do CEP"?
- [ ] **EXPLORATORIO:** Os dados rendem interativo ou feature longo?
- [ ] **RELACAO:** Ha correlacoes? (cuidado com causalidade!)
- [ ] **META-DADOS:** Os dados sao confiaveis? Falta algo? Vale construir base propria?

---

## Output

```markdown
# Analise de dados: [nome da base]
**Data:** [YYYY-MM-DD]
**Fonte:** [origem da base]
**Periodo:** [periodo coberto pelos dados]
**Registros:** [quantidade]

## Estrutura da base
| Coluna | Tipo | Descricao | Exemplo |
|--------|------|-----------|---------|
| ... | ... | ... | ... |

## Qualidade dos dados
- Registros completos: [X%]
- Problemas encontrados: [listar]
- Ha dados ausentes que sao noticia por si so? [sim/nao — explicar]

## Historias encontradas (por angulo)

### ESCALA
- [historia ou "nenhuma historia relevante neste angulo"]

### MUDANCA
- [historia]

### RANKING
- [historia]

### VARIACAO
- [historia]

### EXPLORATORIO
- [possibilidade de interativo ou feature?]

### RELACAO
- [correlacoes encontradas — com ressalvas]

### META-DADOS
- [qualidade dos dados, ausencias, possibilidade de construir base propria]

## Top 3 historias recomendadas

### 1. [Titulo da historia]
- **Angulo:** [qual dos 7]
- **Dado-chave:** [numero ou comparacao]
- **Por que importa:** [relevancia para o leitor]
- **Lide sugerido:** [uma frase]

### 2. [Titulo da historia]
...

### 3. [Titulo da historia]
...

## Dados de apoio
[Tabelas resumidas, agrupamentos, comparacoes que sustentam as historias]

## Sugestao de proximos passos
- [Cruzamento com outra base?]
- [Fonte para ouvir?]
- [Pedido de LAI necessario?]
- [Vale construir base propria?]
- [Vale um interativo?]
```

Salve em `outputs/analises-dados/YYYY-MM-DD-nome-base.md`

---

*Referencia metodologica: "7 types of stories most often found in data"
por Paul Bradshaw, Online Journalism Blog (2020).
Parte 1: https://onlinejournalismblog.com/2020/08/11/here-are-the-7-types-of-stories-most-often-found-in-data/
Parte 2: https://onlinejournalismblog.com/2020/08/12/3-more-angles-most-often-used-to-tell-data-stories-explorers-relationships-and-bad-data-stories/*
