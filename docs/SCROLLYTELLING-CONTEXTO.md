# Scrollytelling Mapa SP — Contexto Completo para Proxima Sessao

## Status Atual

O template scrollytelling-mapa **funciona perfeitamente no desktop** (testado no browser e embedado no WordPress via iframe full-width). O problema pendente e o **layout mobile** — os cards de texto sobem por cima do mapa e ficam visiveis ao mesmo tempo, sem separacao clara.

**URL de teste:** https://gabriel-croquer.github.io/agencia-sp-infograficos/INFOGRAFICOS/TESTE_SCROLLYTELLING/teste_scrolly.html

---

## O que foi feito neste chat

### 1. Pesquisa profunda (3 agentes em paralelo)

Pesquisamos repos e padroes de scrollytelling:

- **The Pudding** (github.com/the-pudding): Stack atual e Svelte 5 + Mapbox GL JS — pesado demais para nos. Repos uteis: `svelte-starter` (Scrolly.svelte usa IntersectionObserver), `climate-zones` (Mapbox + scroll), `gayborhood` (scrollama + D3 antigo).
- **russellsamora/scrollama** (5.957 stars): Lib padrao da industria para scroll detection. Usada por NYT, WaPo, Vox, Politico, ProPublica. API simples: `scrollama().setup({ step, offset }).onStepEnter(cb)`.
- **Mapbox storytelling** (642 stars): Config de chapters com `{ center, zoom, pitch, onChapterEnter }`. Requer token Mapbox — nao serve direto, mas a arquitetura de chapters sim.
- **Jim Vallandingham scroll_demo** (215 stars): Referencia canonica. Pattern de `activateFunctions[]` — array que mapeia step index → funcao.
- **D3 zoom-to-bounding-box** (Observable/Bostock): Pattern de zoom usando `path.bounds()` + `d3.zoomIdentity.translate().scale()` — aplica CSS transform no `<g>`, nao redesenha paths.
- **jsoma/simplified-scrollama-scrollytelling**: Template vanilla mais simples. 4 layouts (basic, progress, sticky-side, sticky-overlay).

### 2. Template criado (one-shot no desktop)

Arquivo: `templates/template-scrollytelling-mapa.html`

**Stack:**
- scrollama.js via unpkg (sem versao fixa = sempre latest)
- D3 v7 via jsdelivr
- GeoJSON de SP embutido no CONFIG (684KB, 645 municipios)
- CSS flexbox + position: sticky
- Single-file HTML (zero build tools)

**Funcionalidades:**
- Mapa sticky SVG (D3 geoMercator) à esquerda, texto rola à direita
- Zoom em municipios via d3.zoom transform (performatico — nao redesenha paths)
- Highlight de municipios (cor + opacity)
- Pontos de interesse (circles SVG com labels)
- Coloracao coropletica por capitulo (threshold/sequential/categorical)
- Legenda dinamica (muda por capitulo)
- Tooltip nos municipios (hover)
- Dots de progresso (lateral direita)
- Counter-scaling de strokes e pontos no zoom (`1 / transform.k`)
- `selection.interrupt()` antes de cada transicao (evita conflitos com scroll rapido)

**CONFIG.capitulos[]:** Cada capitulo tem `titulo`, `texto`, e `mapState` com:
- `zoom`: `"full"` ou `{ tipo: "municipios", codigos: ["3550308", ...] }`
- `highlight`: `null` ou `{ codigos: [...], cor: "#0B9247" }`
- `pontos`: `true/false`
- `cores`: `null` ou `{ tipo_escala, campo_valor, faixas }` para coloracao coropletica

### 3. Licao do iframe WordPress

**Problema:** Scrollytelling precisa de scroll para funcionar. Nosso padrao de embed usa `scrolling="no"` + `overflow:hidden`, o que mata o scrollama completamente.

**Solucao:**
- CSS do template: `overflow-y: auto` (nao `hidden`)
- Scrollbar invisivel: `scrollbar-width: none` + `::-webkit-scrollbar { display: none }`
- Embed: `scrolling="auto"` (NAO "no") + `height="700"` (altura de janela, nao do conteudo)
- Full-width: truque `width:100vw; left:50%; margin-left:-50vw` para escapar da coluna central do WP

**Embed correto:**
```html
<div style="width:100vw;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;">
  <iframe src="URL" width="100%" height="700" style="border:none;" scrolling="auto" loading="lazy"></iframe>
</div>
```

### 4. Problema mobile NAO resolvido

**O que acontece:** No celular, o layout empilha verticalmente (mapa sticky no topo 40vh, text cards abaixo). Mas os cards nao tem altura minima suficiente para criar separacao — 3 ou 4 cards ficam visiveis ao mesmo tempo, sobrepostos ao mapa. O scrollama dispara o step errado porque varios cards estao no viewport simultaneamente.

**Tentativas feitas:**
1. `height: 50vh` no mapa → mapa fica com muito espaco vazio (SVG e paisagem 800x600, tela e retrato)
2. `height: 40vh` + `justify-content: flex-start` → mapa melhor, mas cards sobem por cima
3. `min-height: 60vh` nos steps → muito espaco branco entre cards
4. `min-height: auto` nos steps → cards ficam compactos demais, visiveis ao mesmo tempo
5. `margin-top: 50vh` no primeiro step → ajuda no primeiro, mas o resto continua grudado

**O problema fundamental no mobile:** O pattern "sticky-side" (mapa ao lado do texto) nao funciona em tela estreita. Quando empilha verticalmente, o mapa fica sticky no topo e os cards passam por baixo. Para funcionar, cada card precisa de altura suficiente para que so um card esteja no viewport do scrollama por vez. Mas se os cards tem pouco texto, a altura minima cria espaco branco feio.

**Possiveis solucoes para o proximo agente tentar:**

A) **Cada step com `min-height: 100vh` no mobile** — garante que so um card esta visivel por vez, mas cria MUITO espaco branco se o texto e curto. Talvez centralizar o texto verticalmente no card com flexbox para amenizar.

B) **Mudar para overlay no mobile** — em vez de sticky-side empilhado, o mapa fica fullscreen como background e os cards flutuam como overlay translucido. Isso e o que o Mapbox storytelling template faz. Requer mudanca maior no CSS mobile.

C) **Mapa nao-sticky no mobile** — o mapa aparece como imagem inline entre os textos, um snapshot do estado para cada capitulo. Perde a animacao mas garante legibilidade. Abordagem mais radical.

D) **Combinar A + refinamento** — `min-height: calc(100vh - 40vh)` = 60vh por step no mobile (garante que cada card ocupa o espaco abaixo do mapa). Mais `scroll-snap-type: y mandatory` para que os cards "grudem" em posicao.

E) **Scroll-snap** — adicionar `scroll-snap-type: y proximity` no container e `scroll-snap-align: start` nos steps. Isso faz o browser "ajustar" o scroll para alinhar cada card, evitando posicoes intermediarias onde 2+ cards sao visiveis.

**Recomendacao:** Tentar opcao D (min-height + scroll-snap) primeiro por ser a menor mudanca. Se nao ficar bom, partir para opcao B (overlay mobile) que e o padrao da industria.

---

## Arquivos relevantes

| Arquivo | O que e |
|---|---|
| `templates/template-scrollytelling-mapa.html` | Template base (sem dados) |
| `templates/sp_municipios_2024.geojson` | GeoJSON de SP (684KB, 645 features, winding order corrigido) |
| `templates/catalogo.json` | Indice de templates (8 entradas) |
| `INFOGRAFICOS/TESTE_SCROLLYTELLING/teste_scrolly.html` | Versao de teste com dados ficticios |
| `.claude/agents/gerador-infografico.md` | Workflow do agente gerador (secao scrollytelling adicionada) |
| `CLAUDE.md` | Instrucoes do projeto (secao embed scrollytelling adicionada) |
| `FORGABRIEL.md` | Documentacao completa do projeto |

## Como regenerar o teste

```python
import json, random
random.seed(42)
with open('templates/sp_municipios_2024.geojson', encoding='utf-8') as f:
    geo = json.load(f)
dados = []
for feat in geo['features']:
    cod = feat['properties'].get('CD_MUN', '')
    nome = feat['properties'].get('NM_MUN', '')
    valor = random.randint(0, 1500)
    dados.append({'codigo_ibge': str(cod), 'nome': nome, 'valor': valor})
with open('templates/template-scrollytelling-mapa.html', encoding='utf-8') as f:
    html = f.read()
geo_str = json.dumps(geo, ensure_ascii=False, separators=(',', ':'))
html = html.replace('geojson: null,', 'geojson: ' + geo_str + ',', 1)
# ... injetar dados, pontos, capitulos conforme necessario
```

## Commits feitos neste chat

1. `d94d544` — Adiciona template scrollytelling + teste
2. `4d46607` — Fix: permite scroll interno (overflow-y: auto)
3. `e88b502` — Esconde scrollbar (CSS scrollbar-width: none)
4. `c74e024` — Documenta embed full-width em CLAUDE.md, FORGABRIEL.md, gerador-infografico.md
5. `4f0898f` — Tentativa de fix mobile (40vh mapa, min-height auto) — NAO resolveu
