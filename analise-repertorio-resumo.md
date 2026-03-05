# Analise de Repertorio - Agencia SP

**Data da analise:** 2026-03-05
**Base:** Manual de Identidade Visual v1.7 (Out 2025) + 5 infograficos de referencia

---

## 1. Identidade Visual

### Paleta Principal
| Cor | Hex | Pantone |
|-----|-----|---------|
| Vermelho | #FF161F | 485 C |
| Preto | #000000 | BLACK |
| Branco | #FFFFFF | - |
| Cinza Escuro | #808080 | K50 |
| Cinza Claro | #BFBFBF | K25 |

### Paleta Secundaria
| Cor | Hex | Pantone |
|-----|-----|---------|
| Amarelo | #FBB900 | 123 C |
| Azul Institucional | #034EA2 | 2955 C |
| Verde | #0B9247 | 347 C |
| Azul Claro 1 | #A1DDF7 | - |
| Azul Claro 2 | #62C9E0 | - |
| Azul Medio | #4297D3 | - |
| Azul Escuro | #005992 | - |
| Azul Marinho | #233254 | - |
| Verde Oliva | #94AA5A | - |
| Vermelho Escuro | #842519 | - |

### Tipografia
- **Principal:** Futura PT (Medium, Bold)
- **Secundaria:** Montserrat (Medium, Bold)
- **Sistema:** Verdana (Regular, Italic, Bold)

### Logo
- Formato pilula arredondada com texto "AGENCIA" e icone "SP"
- Versoes: positiva (preta) e negativa (branca)

---

## 2. Infograficos Analisados

### 2.1 Barras Horizontais Comparativas (`bar_horizontal.jpeg`)
- Comparacao por ano (2023, 2024, 2025) em 3 categorias
- Cinza para anos anteriores, verde para ano de destaque
- Tema: participacao no Saresp

### 2.2 Barras Empilhadas 100% (`bar_stacked.jpeg`)
- Grid 2x3 (Lingua Portuguesa e Matematica x 2o, 5o, 9o ano)
- 4 niveis: Abaixo do Basico, Basico, Adequado, Avancado
- Gradiente cinza-escuro a verde-escuro
- Tema: niveis de proficiencia Saresp

### 2.3 Barras Verticais Serie Historica (`info_barras.jpeg`)
- Serie de 2001 a 2026 com barras verticais
- Cinza (#C0C0C0) para historico, verde para ano atual
- Tema: roubos no Estado de SP

### 2.4 Barras Verticais Serie Historica (`info_barras_2.jpeg`)
- Mesmo padrao visual que info_barras.jpeg
- Tema: roubos na Cidade de SP

### 2.5 Tabela Comparativa (`tabela.jpeg`)
- Colunas: Natureza, Jan-2025, Jan-2026, Variacao absoluta, Variacao %
- Fundo verde nas celulas do periodo atual
- Vermelho para variacoes negativas
- Tema: indicadores criminais

---

## 3. Padroes Visuais Recorrentes

Os infograficos analisados compartilham um conjunto consistente de padroes:

| Elemento | Padrao |
|----------|--------|
| **Fundo** | Branco limpo |
| **Titulo** | Negrito, com keyword destacada em verde |
| **Subtitulo** | Descritivo, cinza/preto, fonte menor |
| **Fonte de dados** | Canto inferior esquerdo, cinza, fonte pequena |
| **Espaco em branco** | Abundante, design minimalista |
| **Barras** | Cantos levemente arredondados |

### Semantica de Cores
- **Verde:** dado atual, destaque positivo, crescimento
- **Cinza:** dados historicos, contexto, baseline
- **Vermelho:** dados negativos, queda, alerta

---

## 4. Dados de Exemplo Disponiveis

**Arquivo:** `inputs/dados-exemplo/slide3-serie-historica-proficiencias.csv`

- Proficiencias medias do Saresp (2015-2025)
- Disciplinas: Lingua Portuguesa e Matematica
- Series: 2o Ano (dados a partir de 2021), 5o Ano, 9o Ano
- Valores numericos em escala de proficiencia

---

## 5. Recomendacoes para Criacao de Templates

### Estrutura Geral
1. **Header:** titulo em Futura PT Bold, com keyword em verde (#0B9247). Subtitulo em Montserrat Medium, cor cinza.
2. **Corpo:** area de dados com fundo branco, margens generosas.
3. **Footer:** fonte de dados alinhada a esquerda em Verdana Regular cinza (#808080).

### Tipos de Template Prioritarios
Com base no repertorio analisado, os seguintes templates devem ser criados:

1. **Barras Verticais - Serie Historica:** para comparacoes longas no tempo (ex: 2001-2026). Cinza para historico, verde para destaque.
2. **Barras Horizontais - Comparacao por Ano:** para comparacoes de 2-4 anos em poucas categorias.
3. **Barras Empilhadas 100%:** para distribuicao de categorias (niveis de proficiencia, faixas). Grid quando houver multiplas dimensoes.
4. **Tabela Comparativa:** para indicadores com variacao percentual e absoluta. Fundo colorido para periodo atual, texto vermelho para variacoes negativas.

### Regras de Cores
- Usar paleta oficial do manual (verde #0B9247, cinza #808080/#BFBFBF, vermelho #FF161F)
- Verde para destaque positivo e dado mais recente
- Cinza para contexto e dados anteriores
- Vermelho para indicadores negativos ou de alerta
- Evitar cores fora da paleta secundaria

### Tipografia
- Titulos: Futura PT Bold (fallback: Montserrat Bold)
- Corpo e rotulos: Montserrat Medium
- Dados e notas: Verdana Regular
- Tamanhos proporcionais ao formato de saida (slide 16:9 ou post redes sociais)

### Boas Praticas
- Manter design minimalista com espaco em branco abundante
- Cantos arredondados nas barras dos graficos
- Contraste alto entre texto e fundo
- Fonte de dados sempre visivel no rodape
- Keywords do titulo sempre destacadas em cor
