# Agencia SP — Fabrica de Infograficos Interativos

Sistema de criacao automatizada de infograficos interativos com identidade visual da Agencia SP (Governo do Estado de Sao Paulo). Substitui o Flourish com templates proprios, hospedados no GitHub Pages e embedados no WordPress via iframe.

## Como funciona

```
Voce envia:                          Voce recebe:
  - Titulo                             - HTML pronto em output/
  - Linha fina (subtitulo)             - Preview para revisar
  - Fonte dos dados                    - Codigo embed para WordPress
  - CSV com os dados
  - Instrucoes adicionais
         |
         v
   Claude processa tudo
   (escolhe template, formata dados, gera HTML)
         |
         v
   Voce revisa e sugere ajustes
         |
         v
   Aprovado → push no GitHub Pages
   URL publica atualiza automaticamente
```

### Workflow passo a passo

1. **Envie os dados** — Mande o CSV + titulo, linha fina, fonte e qualquer instrucao adicional (ex: "destaque o ano de 2024", "use grafico de barras horizontal")
2. **Eu gero o infografico** — Escolho o template certo, processo os dados e gero o HTML final em `output/`
3. **Voce revisa** — Abre o HTML no navegador, ve se esta bom, sugere ajustes
4. **Eu ajusto** — Quantas vezes for necessario. Os chefes sempre tem opiniao, e tudo bem
5. **Publicacao** — Faco commit + push. O infografico fica disponivel via GitHub Pages
6. **Embed** — Voce cola o iframe no WordPress (bloco HTML Personalizado)

### Atualizacoes pos-publicacao

Precisa mudar algo depois de publicado? Sem problema. Eu edito o HTML, faco push, e a mesma URL atualiza automaticamente. O iframe no WordPress nao precisa ser tocado.

## URLs

- **Repositorio:** https://github.com/Gabriel-Croquer/agencia-sp-infograficos
- **GitHub Pages:** https://gabriel-croquer.github.io/agencia-sp-infograficos/
- **Infograficos publicados:** `https://gabriel-croquer.github.io/agencia-sp-infograficos/output/[nome].html`

### Exemplo de embed no WordPress

```html
<iframe src="https://gabriel-croquer.github.io/agencia-sp-infograficos/output/nome-do-infografico.html"
        width="100%" height="600" frameborder="0"></iframe>
```

## Estrutura do Projeto

```
agencia-sp-templates/
├── .claude/agents/          → Agentes de IA (analista, estrategista, dev, QA, gerador)
├── inputs/
│   ├── manual-iv/           → Manual de identidade visual + logo
│   ├── infograficos-existentes/ → Screenshots de referencia
│   └── dados-exemplo/       → CSVs de exemplo
├── templates/               → 6 templates-base reutilizaveis
├── output/                  → Infograficos finais prontos (publicados via GitHub Pages)
├── publicar.py              → Script auxiliar para gerar embed code
├── CLAUDE.md                → Instrucoes para o agente
└── FORGABRIEL.md            → Documentacao tecnica do projeto
```

## Templates disponiveis

| Template | Uso |
|----------|-----|
| Bar Vertical | Comparacao de valores ao longo do tempo |
| Bar Horizontal | Ranking ou comparacao entre categorias |
| Bar Stacked | Composicao de um total por categorias |
| Tabela Comparativa | Dados tabulares com destaque visual |
| Linha Temporal | Evolucao de series ao longo do tempo |
| Card KPI | Numeros-chave em destaque (indicadores) |

## Identidade Visual

- Cores: verde (#0B9247) para destaque, cinza (#C0C0C0) para historico, vermelho (#FF161F) para negativo
- Fonte: Montserrat (Google Fonts)
- Titulo em negrito com keyword em verde (a cor E a legenda)
- Logo Agencia SP centralizado embaixo
- Fundo branco, design minimalista
- "Fonte: [orgao]" no rodape esquerdo

## Tecnologias

- **Templates:** HTML + CSS + JS vanilla (zero dependencias)
- **Graficos:** SVG (responsivo, acessivel, vetorial)
- **Hosting:** GitHub Pages (gratis)
- **Embed:** iframe no WordPress
- **Processamento:** Python (pandas) para CSVs
- **Agentes:** Claude Code
