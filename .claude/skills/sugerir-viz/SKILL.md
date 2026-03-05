---
name: sugerir-viz
description: Sugere visualizacoes e infograficos a partir de dados ou briefing. Use quando precisar decidir que tipo de grafico, mapa ou infografico usar para contar uma historia com dados.
argument-hint: "[base de dados ou briefing de dados]"
---

# Skill: Sugestao de visualizacoes e infograficos

## Ao receber dados ou briefing

### 1. Identifique o tipo de historia

Antes de escolher qualquer grafico, responda: "O que estou tentando comunicar com esses dados?"
A resposta determina todas as escolhas. Nunca escolha o tipo de grafico antes de entender a historia.

- **Mudanca ao longo do tempo**: Tendencias, padroes, flutuacoes → linhas, areas, line chart race
- **Magnitude**: Comparacoes de tamanho relativo ou absoluto → barras, lollipop
- **Composicao (partes de um todo)**: Como cada parte contribui para o total → stacked bars, treemap, pizza (max 5 fatias), grafico de arco
- **Distribuicao**: Como valores se espalham e com que frequencia → histograma, box plot, beeswarm, piramide populacional
- **Correlacao**: Relacao entre duas ou mais variaveis → scatter plot (correlacao ≠ causalidade!)
- **Geografico**: Padroes espaciais → mapa coropletico, mapa de bolhas, cartograma. ATENCAO: ter dados geograficos NAO significa que mapa e a melhor opcao
- **Ranking**: Posicao ordinal importa mais que valor absoluto → barras horizontais, bar chart race (ranking ao longo do tempo)
- **Desvio**: Variacoes em relacao a um ponto de referencia (zero, meta, media) → barra divergente, linha de superavit/deficit
- **Fluxo**: Movimento entre estados ou condicoes → Sankey, alluvial, grafico de rede

### 2. Regras de ouro para visualizacao jornalistica

- **Menos e mais**: um grafico, uma mensagem
- **Titulo conta a historia**: "SP lidera ranking de vacinacao" > "Vacinacao por estado"
- **Eixo Y comeca em zero** para barras (evitar distorcao visual)
- **Maximo 7 categorias** por grafico; agrupe o resto em "Outros"
- **Cores com proposito**: destaque o dado principal, cinza para o resto
- **Acessibilidade**: nao dependa so de cor; use rotulos diretos
- **Mobile first**: o grafico precisa funcionar em tela de celular

### 3. Templates Flourish por tipo de historia

Ao recomendar Flourish, indique o template especifico:

| Tipo de historia | Template Flourish | Quando usar |
|-----------------|-------------------|-------------|
| Evolucao temporal | Line, Bar & Pie (com time slider) | Series temporais, animacao ano a ano |
| Ranking animado | Bar Chart Race | Rankings que mudam ao longo do tempo |
| Composicao ao longo do tempo | 100% Stacked Bar/Column | Partes de um todo evoluindo (ex: niveis de proficiencia) |
| Composicao (comparacao) | Survey / Diverging Bar | Dados tipo Likert, pesquisas de opiniao, escalas ordinais |
| Trajetorias individuais | Slope Chart | 2-3 pontos no tempo, mostrar quem subiu/caiu |
| Fluxo proporcional | Area Bump Chart (proporcional) | Ribbons que mostram mudanca de composicao — forte impacto visual |
| Geografico | Projection Map / Symbol Map | Dados por regiao, estado, municipio |
| Hierarquia | Treemap | Partes de um todo com muitas categorias |

### 4. Ferramentas sugeridas

| Ferramenta | Melhor para | Custo |
|-----------|-------------|-------|
| Datawrapper | Graficos rapidos, mapas, tabelas | Gratis (basico) |
| Flourish | Graficos interativos, storytelling | Gratis (basico) |
| Infogram | Infograficos completos, dashboards | Pago |
| RAWGraphs | Graficos nao-convencionais | Gratis |
| Canva | Infograficos estaticos simples | Freemium |

## Output

```markdown
# Sugestoes de visualizacao: [tema]
**Data:** [YYYY-MM-DD]

## Dados disponiveis
[Resumo dos dados que temos]

## Visualizacao 1 (principal)
- **Tipo:** [ex: grafico de barras horizontais]
- **O que mostra:** [descricao clara]
- **Titulo sugerido:** [titulo que conta a historia]
- **Eixos/dimensoes:** [X = ..., Y = ..., Cor = ...]
- **Ferramenta recomendada:** [Datawrapper / Flourish / etc.]
- **Por que esse tipo:** [justificativa]

## Visualizacao 2 (complementar)
...

## Visualizacao 3 (se aplicavel)
...

## Dados que faltam
[O que seria necessario para melhorar as visualizacoes]

## Briefing para designer/infografista
[Descricao em linguagem simples do que precisa ser feito]
```

Salve em `outputs/analises-dados/YYYY-MM-DD-viz-tema.md`
