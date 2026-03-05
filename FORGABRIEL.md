# FORGABRIEL - Agencia SP Templates

## O que e esse projeto?

Imagine o Flourish, aquela ferramenta que transforma planilhas em graficos bonitos para a web. Agora imagine uma versao dele que ja vem com a cara do Governo de Sao Paulo — cores, fontes, logo, tudo no padrao. E que roda dentro do Claude Code, sem precisar de conta em nenhum servico. E isso aqui.

A Agencia SP (agencia de noticias do Governo do Estado de Sao Paulo) publica infograficos interativos nas suas materias. Ate agora, usavam o Flourish. Esse projeto cria uma alternativa propria: templates HTML interativos que seguem a identidade visual do governo, alimentados por dados via CSV, e publicados via GitHub Pages.

---

## Arquitetura Tecnica

### Como as pecas se encaixam

```
inputs/                     → Materia-prima (manual IV, infograficos de referencia, CSVs)
    manual-iv/              → PDF do manual + logo PNG
    infograficos-existentes/→ Screenshots dos infos ja publicados (referencia visual)
    dados-exemplo/          → CSVs com dados reais do Saresp

templates/                  → Os 6 templates-base (esqueletos reutilizaveis)
    template-bar-vertical.html
    template-bar-horizontal.html
    template-bar-stacked.html
    template-tabela-comparativa.html
    template-linha-temporal.html
    template-card-kpi.html
    catalogo.json           → Indice de templates

output/                     → Infograficos finais prontos (gerados pelo agente)

.claude/agents/             → Definicoes dos agentes de IA
    analista-repertorio.md  → Analisa inputs e extrai identidade visual
    estrategista-formatos.md→ Define quais templates criar
    dev-templates.md        → Cria os HTMLs
    qa-templates.md         → Revisa e corrige tudo
    gerador-infografico.md  → O principal: recebe dados + instrucao, gera info pronto

publicar.py                 → Gera codigo de embed para WordPress
analise-repertorio.json     → Relatorio da identidade visual extraida
plano-templates.json        → Plano dos 6 templates com specs
```

### Fluxo de uso (o dia-a-dia)

```
Gabriel envia CSV + "faz um grafico de barras de X"
        ↓
Agente gerador-infografico:
  1. Le o CSV (com Python/pandas)
  2. Escolhe o template certo
  3. Processa dados → formato CONFIG
  4. Gera HTML final em output/
        ↓
python publicar.py output/nome.html --base-url https://URL
        ↓
Copia o <iframe> e cola no WordPress (bloco HTML Personalizado)
```

### Cada template e um arquivo .html unico

Sem dependencias externas (exceto Google Fonts Montserrat). Tudo — CSS, JavaScript, SVG, dados, logo — esta dentro do mesmo arquivo. Isso e proposital: facilita o hosting, o embed, e evita quebras por CDN fora do ar.

Os graficos sao renderizados em **SVG** (nao Canvas), o que permite:
- Responsividade nativa
- Acessibilidade (aria-labels nos elementos)
- Qualidade em qualquer resolucao
- Tooltips e hovers via CSS/JS vanilla

---

## Tecnologias e Decisoes

| Decisao | Escolha | Por que |
|---------|---------|---------|
| Stack dos templates | HTML + CSS + JS vanilla | Zero dependencias = zero quebras |
| Graficos | SVG | Responsivo, acessivel, vetorial |
| Fonte | Montserrat (Google Fonts) | Mais proxima da Futura PT do manual, gratis e web-safe |
| Logo nos templates | Base64 embutido | Mantém single-file, sem dependencia de path |
| Hosting | GitHub Pages | Gratis, facil, sem precisar de acesso ao servidor WP |
| Embed | iframe | Compativel com bloco HTML Personalizado do WordPress |
| Processamento de dados | Python (pandas) | Ja instalado no ambiente, robusto para CSVs |
| Agentes | Claude Code Agent Teams | 7 agentes em paralelo para criar os 6 templates de uma vez |

### Por que nao usar o Flourish?

O Flourish e otimo, mas:
1. Dependencia de servico externo (se cai, os infos caem)
2. Marca d'agua "Made with Flourish" na versao gratis
3. Customizacao limitada da identidade visual
4. Nao integra com o workflow interno da agencia

### Por que Montserrat e nao Futura PT?

O manual define Futura PT como fonte principal, mas ela e proprietaria (custa licenca). Montserrat e a Google Font mais proxima da Futura em peso e geometria, e e gratis para web. Verdana (a fonte de sistema do manual) e o fallback.

---

## Identidade Visual — O Resumo

Extraido do Manual de Identidade Visual v1.7 (Out 2025):

**Cores que usamos nos infograficos:**
- `#0B9247` — Verde (destaque, dado atual/positivo, keyword no titulo)
- `#C0C0C0` — Cinza (dados historicos, contexto)
- `#FF161F` — Vermelho (dados negativos, variacao ruim)
- `#034EA2` — Azul (serie secundaria em graficos de linha)
- `#1D1D1B` — Preto (texto)
- `#FFFFFF` — Branco (fundo)

**Padrao visual dos infograficos da Agencia SP:**
- Fundo branco, muito espaco em branco, minimalismo
- Titulo em negrito com **keyword em verde** — a cor E a legenda (sem legenda separada)
- Subtitulo descritivo em cinza
- "Fonte: [orgao]" no rodape esquerdo
- Logo Agencia SP centralizado embaixo
- Barras cinza para historico, verde para destaque

Esse padrao foi extraido analisando 7 infograficos reais ja publicados pela agencia.

---

## Licoes Aprendidas

### Agent Teams: paralelismo e o segredo
Na primeira tentativa, lancei os agentes sequencialmente (1 → 2 → 3 → 4). O usuario corretamente apontou que Agent Teams existem para rodar em paralelo. A solucao: eu (team lead) ja tinha toda a analise na cabeca, entao escrevi os arquivos de fundacao eu mesmo e lancei 6 dev agents em paralelo — cada um criando um template diferente. Resultado: 6 templates criados simultaneamente.

### Yolo mode precisa de restart
Adicionar `permissions.mode: "yolo"` no settings.json nao surte efeito imediato no VS Code. O Claude Code precisa ser reiniciado para que a mudanca pegue. Isso causou frustacao porque o usuario queria sair para almocar sem ficar aprovando permissoes.

### CONFIG manual e anti-usuario
A primeira versao dos templates exigia que o usuario editasse um bloco `const CONFIG = {...}` manualmente com os dados. O usuario comparou com o Flourish (onde voce so cola os dados) e rejeitou essa abordagem. Solucao: criamos o agente `gerador-infografico` que processa o CSV automaticamente e gera o HTML final — o usuario nunca toca no CONFIG.

### Logo: posicao importa
Os infograficos feitos pela equipe de arte da agencia sempre colocam o logo da Agencia SP **centralizado embaixo**. Na primeira geracao, um template colocou o logo no canto superior direito. Corrigimos para todos os templates terem o logo apenas embaixo, via base64 embutido.

### PDF no Windows: pdftoppm nao existe
O Read tool nao consegue ler PDFs no Windows porque depende de `pdftoppm`. Solucao: usar PyMuPDF (`fitz`) que ja estava instalado via pip. Porem, o encoding padrao do Windows (cp1252) nao suporta alguns caracteres Unicode do PDF — precisamos forcar `sys.stdout` para UTF-8.

### Fonte: Montserrat precisa ser explicita em TUDO
Mesmo definindo `font-family` no `body`, alguns elementos (tooltips, SVG text) podem herdar fontes do sistema. Verificamos que todos os 6 templates tem `'Montserrat', sans-serif` como unica font-family declarada.

---

## Proximos Passos

1. **Subir repo no GitHub e ativar GitHub Pages** — para ter URLs publicas dos infograficos
2. **Testar o workflow completo** — enviar um CSV real, gerar infografico, publicar, embedar no WordPress
3. **Iterar nos templates** — ajustar detalhes visuais conforme feedback do time de arte
4. **Novos tipos de template** — se surgirem necessidades (mapa, donut chart, treemap, etc.)
