# Como Usar os Templates da Agencia SP

## O que sao estes templates?

Sao arquivos HTML prontos para uso que geram graficos e visualizacoes de dados interativas. Cada template e um arquivo unico e independente - basta abrir no navegador para ver o resultado. Nao precisam de instalacao de software adicional.

Os templates seguem a identidade visual da Agencia SP (verde #0B9247, fonte Montserrat, fundo branco).

---

## Templates disponiveis

| Template | Arquivo | Para que serve |
|----------|---------|----------------|
| Barras Verticais | `template-bar-vertical.html` | Serie historica com barras verticais e destaque em um ano |
| Barras Horizontais | `template-bar-horizontal.html` | Comparativo por categoria com barras agrupadas por ano |
| Barras Empilhadas | `template-bar-stacked.html` | Composicao percentual (100%) por niveis em grid |
| Tabela Comparativa | `template-tabela-comparativa.html` | Tabela com ordenacao, variacao absoluta e percentual |
| Grafico de Linhas | `template-linha-temporal.html` | Evolucao temporal com multiplas series |
| Cards KPI | `template-card-kpi.html` | Cards com numero grande, animacao de contagem e variacao |

---

## Como editar os dados (CONFIG)

Cada template tem um bloco `CONFIG` no inicio do codigo JavaScript. E nele que voce altera os dados, titulos e cores.

### Passo a passo

1. Clique com o botao direito no arquivo HTML e escolha **"Abrir com"** > **Bloco de Notas** (ou qualquer editor de texto)
2. Procure a palavra `CONFIG` - ela aparece logo no inicio do bloco `<script>`
3. Altere os valores conforme necessario
4. Salve o arquivo (Ctrl+S)
5. Abra o arquivo no navegador para ver o resultado

### Exemplo: alterando o titulo

Antes:
```javascript
titulo: 'Seguranca Publica em SP - <span class="destaque">Janeiro 2026</span>',
```

Depois:
```javascript
titulo: 'Seguranca Publica em SP - <span class="destaque">Fevereiro 2026</span>',
```

A parte dentro de `<span class="destaque">...</span>` aparece em verde no titulo.

### Exemplo: alterando dados no grafico de barras verticais

```javascript
dados: [
  { label: "2023", valor: 16000 },
  { label: "2024", valor: 15800 },
  { label: "2025", valor: 12100 }
]
```

- `label`: o rotulo que aparece no eixo (normalmente o ano)
- `valor`: o numero que define a altura da barra

### Exemplo: alterando dados na tabela comparativa

```javascript
dados: [
  { natureza: 'Roubo de veiculo', periodo1: 2312, periodo2: 1361, var_abs: -951, var_pct: -41.13 },
  { natureza: 'Furto', periodo1: 48026, periodo2: 44226, var_abs: -3800, var_pct: -7.91 }
]
```

### Exemplo: alterando um card KPI

```javascript
cards: [
  { label: 'Roubo de Veiculo', valor: 1361, variacao: -41.13, prefixo: '', sufixo: '' }
]
```

- `label`: nome do indicador
- `valor`: numero principal
- `variacao`: percentual de mudanca (negativo = queda, positivo = aumento)
- `prefixo`/`sufixo`: texto antes/depois do numero (ex: `prefixo: 'R$ '` ou `sufixo: '%'`)

### Campos comuns em todos os templates

| Campo | O que faz |
|-------|-----------|
| `titulo` | Titulo principal (aceita HTML para destaque em verde) |
| `subtitulo` | Texto explicativo abaixo do titulo |
| `fonte` | Credito da fonte de dados (aparece no rodape) |

---

## Como abrir no navegador

1. Localize o arquivo HTML na pasta `templates/`
2. De um duplo-clique no arquivo - ele abrira no navegador padrao
3. Ou: abra o navegador e arraste o arquivo para dentro da janela

O grafico sera renderizado automaticamente com os dados do CONFIG.

---

## Como usar em WordPress (iframe)

### Opcao 1: Upload direto + iframe

1. Faca upload do arquivo HTML para o servidor (via FTP ou Gerenciador de Arquivos do hosting)
   - Exemplo: coloque em `wp-content/uploads/graficos/template-bar-vertical.html`
2. No editor do WordPress, adicione um bloco **HTML personalizado** com:

```html
<iframe
  src="/wp-content/uploads/graficos/template-bar-vertical.html"
  width="100%"
  height="500"
  frameborder="0"
  style="border: none; max-width: 100%;"
  title="Grafico de barras verticais">
</iframe>
```

3. Ajuste o `height` conforme necessario para cada tipo de grafico:
   - Barras verticais: `height="500"`
   - Barras horizontais: `height="400"`
   - Barras empilhadas: `height="700"`
   - Tabela comparativa: `height="500"`
   - Grafico de linhas: `height="550"`
   - Cards KPI: `height="400"`

### Opcao 2: Pagina completa

Se quiser que o grafico ocupe uma pagina inteira, basta acessar diretamente a URL do arquivo HTML no servidor.

---

## Troubleshooting

### O grafico nao aparece / pagina em branco
- Verifique se o arquivo foi salvo corretamente (nao pode ter erros de sintaxe no CONFIG)
- Confira se nao removeu uma virgula, aspas ou chaves no JavaScript
- Abra o Console do navegador (F12 > aba Console) para ver mensagens de erro

### As fontes estao diferentes
- Os templates usam Google Fonts (Montserrat). E necessario conexao com internet para carregar a fonte
- Se estiver offline, o navegador usara uma fonte generica sans-serif

### A barra de destaque nao aparece em verde
- Verifique se o valor de `ano_destaque` corresponde a um dos `label` nos dados
- O label precisa ser exatamente igual (ex: `"2025"` no label e `2025` no ano_destaque)

### O iframe esta cortando o conteudo no WordPress
- Aumente o valor de `height` no iframe
- Ou adicione `scrolling="auto"` ao iframe para permitir rolagem

### Os numeros de variacao estao errados
- Confira os campos `var_abs` e `var_pct` no CONFIG da tabela
- O calculo nao e automatico - voce precisa informar os valores corretos

### O tooltip nao aparece
- Passe o mouse sobre as barras, pontos ou segmentos do grafico
- Em dispositivos touch (celular/tablet), toque e segure sobre o elemento
