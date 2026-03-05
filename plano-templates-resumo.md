# Plano de Templates - Agencia SP

## Resumo

6 templates HTML interativos, single-file, baseados nos infograficos ja publicados pela Agencia SP e nos dados de exemplo disponiveis.

## Templates Planejados

### 1. Barras Verticais - Serie Historica (Prioridade: ALTA)
- **Base**: info_barras.jpeg, info_barras_2.jpeg
- **Uso**: Series temporais longas (ex: evolucao de roubos 2001-2026)
- **Destaque**: Ano atual em verde, demais em cinza

### 2. Barras Horizontais - Comparativo por Ano (Prioridade: ALTA)
- **Base**: bar_horizontal.jpeg
- **Uso**: Comparar porcentagens entre periodos (ex: participacao Saresp)
- **Destaque**: Colunas lado a lado por ano, ultimo ano em verde

### 3. Barras Empilhadas - Composicao Percentual (Prioridade: ALTA)
- **Base**: bar_stacked.jpeg
- **Uso**: Distribuicao em categorias (ex: niveis de proficiencia)
- **Destaque**: Grid 2 colunas, cores graduais do cinza ao verde

### 4. Tabela Comparativa com Variacao (Prioridade: MEDIA)
- **Base**: tabela.jpeg
- **Uso**: Comparar dois periodos com variacao absoluta e percentual
- **Destaque**: Celulas coloridas, variacao negativa em vermelho

### 5. Grafico de Linhas - Evolucao Temporal (Prioridade: MEDIA)
- **Base**: CSV de proficiencias Saresp
- **Uso**: Multiplas series ao longo do tempo
- **Destaque**: Linhas coloridas com pontos interativos

### 6. Cards KPI - Destaque Numerico (Prioridade: NORMAL)
- **Base**: Padrao comum em dashboards
- **Uso**: Destacar indicadores-chave com variacao
- **Destaque**: Numeros grandes com animacao de contagem

## Identidade Visual Aplicada
- Verde destaque: #0B9247
- Cinza neutro: #808080
- Vermelho negativo: #FF161F
- Fonte: Montserrat (Google Fonts)
- Fundo branco, design minimalista, titulos com keyword em verde

## Interatividade Padrao
- Tooltip ao hover com valor exato
- Animacao de entrada (crescimento/contagem)
- Hover effects suaves
- 100% responsivo
- Acessivel (aria-labels, contraste WCAG AA)
