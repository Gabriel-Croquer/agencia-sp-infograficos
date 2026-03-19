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

### Mapa Coropletico: D3 e o winding order invertido

Essa foi a licao mais dolorosa do projeto. Gastamos varias tentativas ate o mapa renderizar corretamente — em vez de mostrar os 645 municipios de SP, aparecia um retangulo solido de uma cor so cobrindo todo o SVG.

**O problema:** O D3.js usa uma convencao de winding order (ordem dos vertices dos poligonos) **oposta** ao padrao GeoJSON RFC 7946. No RFC 7946, aneis exteriores sao counter-clockwise. No D3, sao clockwise. Quando o D3 recebe um poligono com winding order "errado" (do ponto de vista dele), ele interpreta como "todo o planeta MENOS esse poligono". Resultado: 645 poligonos invertidos empilhados = um retangulo solido.

**A solucao:** Inverter todos os aneis de coordenadas antes de usar no D3:
```python
def reverse_rings(geometry):
    if geometry['type'] == 'Polygon':
        geometry['coordinates'] = [ring[::-1] for ring in geometry['coordinates']]
    elif geometry['type'] == 'MultiPolygon':
        geometry['coordinates'] = [[ring[::-1] for ring in poly] for poly in geometry['coordinates']]
```

O arquivo `templates/sp_municipios_2024.geojson` ja vem com o winding order corrigido. Se alguem trocar o GeoJSON, TEM que inverter de novo.

### TopoJSON do Python != TopoJSON do D3

Tentamos usar a lib Python `topojson` para converter GeoJSON → TopoJSON (arquivo menor). O TopoJSON gerado pelo Python e estruturalmente diferente do que a lib `topojson-client` do D3 espera. Os nomes dos objetos internos, a estrutura dos arcos, tudo incompativel. Solucao: abandonamos TopoJSON e usamos GeoJSON direto. O arquivo fica maior (~670KB vs ~200KB), mas funciona sem dor de cabeca.

### GeoJSON do IBGE pode vir com geometrias faltando

O GeoJSON simplificado de municipios de SP veio com 644 geometrias em vez de 645. Aguas de Sao Pedro (menor municipio de SP, ~3.6 km²) tinha geometria nula — provavelmente perdida na simplificacao. Solucao: pegamos a geometria do GeoJSON original (nao simplificado) e injetamos no simplificado. Moral: sempre conferir se o numero de features bate com o esperado.

### Workflow final do mapa coropletico

O que funciona de verdade, sem surpresas:
1. GeoJSON base ja salvo no projeto com winding order corrigido (`templates/sp_municipios_2024.geojson`)
2. Ler CSV com pandas, montar array de dados com `codigo_ibge` (string, 7 digitos)
3. Embutir o GeoJSON inteiro como JS literal no HTML (sim, ~670KB inline — funciona)
4. D3 renderiza com `geoMercator().fitSize()` — sem tiles, sem Leaflet, SVG puro
5. Escala de cores: categorical para sim/nao, threshold para faixas, sequential para valores continuos

---

### Scrollytelling: mapa narrativo com scroll

O 8o template do projeto. Combina um mapa SVG sticky do estado de SP com capitulos de texto que rolam ao lado. Conforme o leitor rola, o mapa reage: da zoom em regioes, destaca municipios, mostra pontos de interesse, e troca a coloracao coropletica. Tudo controlado por um array `CONFIG.capitulos[]` onde cada capitulo define um `mapState`.

**Stack:** scrollama.js (deteccao de scroll via IntersectionObserver, 5.9k stars no GitHub, lib padrao da industria usada por NYT, Pudding, WaPo, Vox) + D3 v7 (renderizacao SVG do mapa) + nosso GeoJSON de municipios de SP.

**A pesquisa que antecedeu:** Antes de codar, pesquisamos repos do The Pudding (svelte-starter, climate-zones, gayborhood), Mapbox storytelling template, Jim Vallandingham (scroll_demo, a referencia canonica), D3 zoom-to-bounding-box do Mike Bostock, e IHME ScrollyTeller. O template final combina o melhor de cada:
- Layout sticky-side do jsoma/simplified-scrollama-scrollytelling
- d3.zoom transform do Observable (performatico — nao redesenha paths, so aplica CSS transform no `<g>`)
- Config de chapters inspirado no Mapbox storytelling
- Pattern de activateFunctions[] do Vallandingham

**Como funciona o zoom:** Em vez de re-calcular a projecao (caro — redesenha 645 paths), usamos `d3.zoom` que aplica um transform CSS no grupo `<g>` do SVG. Isso e instantaneo. O truque e counter-scale os stroke-widths e raios dos pontos dividindo por `transform.k` (o fator de escala), senao as bordas ficam grossas demais no zoom.

**Licao crucial sobre iframe + scrollytelling:**
Scrollytelling **precisa** de scroll para funcionar — o scrollama detecta quais capitulos estao visiveis conforme o usuario rola. Nosso padrao de embed para infograficos estaticos usa `scrolling="no"` + `overflow:hidden`, o que **mata o scrollytelling completamente** (nada se move). A solucao:
1. CSS do template: `overflow-y: auto` (nao `hidden`) + scrollbar invisivel via `scrollbar-width: none` e `::-webkit-scrollbar { display: none }`
2. Embed WordPress: `scrolling="auto"` (nao `"no"`) + `height="700"` (altura de janela, nao do conteudo todo)
3. Full-width: o truque `width:100vw; left:50%; margin-left:-50vw` faz o iframe escapar da coluna central do WordPress e ocupar a tela inteira

**Embed WordPress para scrollytelling:**
```html
<div style="width:100vw;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;">
  <iframe src="URL" width="100%" height="700" style="border:none;" scrolling="auto" loading="lazy"></iframe>
</div>
```

### Scrollytelling mobile: o overlay pattern

O layout desktop (mapa sticky a esquerda 58%, texto a direita 42%) nao funciona em tela estreita. Quando empilha verticalmente com o mapa pequeno (40vh) no topo e cards abaixo, 3+ cards ficam visiveis ao mesmo tempo — confuso e ilegivel.

**A solucao: overlay pattern** (inspirado na Sky News US Election 2020). No mobile, o mapa vira background sticky de 85vh (quase fullscreen) e os cards flutuam por cima dele, um de cada vez, como cartas de baralho passando sobre a mesa.

**CSS mobile critico:**
- Mapa: `height: 85vh; justify-content: center; box-shadow: none`
- Cards: `max-width: 320px; margin: 0 auto; background: rgba(255,255,255,0.92); backdrop-filter: blur(4px); border-radius: 12px`
- Texto container: `pointer-events: none` (permite tocar no mapa entre cards)
- Cards: `pointer-events: auto` (reativa interacao nos proprios cards)
- Legenda: `position: absolute; bottom: 8px` (flutua sobre o mapa)

**Spacing entre cards — NUNCA usar vh no mobile:**
Browsers mobile mudam a altura do viewport quando a barra de URL aparece/desaparece, fazendo `vh` oscilar. Solucao: calcular o spacing em **pixels** via JavaScript usando `window.innerHeight * 0.85`. Isso garante que so um card esta visivel por vez, independente da barra de URL.

```javascript
if (isMobile) {
  function setMobileStepSpacing() {
    var spacing = Math.round(window.innerHeight * 0.85);
    document.querySelectorAll('.step').forEach(function(step, i, arr) {
      if (i < arr.length - 1) step.style.marginBottom = spacing + 'px';
    });
    scroller.resize();
  }
  setMobileStepSpacing();
  window.addEventListener('resize', setMobileStepSpacing);
}
```

### window.scrollY e a armadilha do overflow-y: auto

Essa custou 3 tentativas ate achar o bug. O scrollytelling usa `html { overflow-y: auto; height: 100% }` para funcionar dentro de iframe com scrollbar invisivel. Isso faz o scroll acontecer no elemento `<html>`, nao no `window`. Consequencia: **`window.scrollY` retorna SEMPRE 0**.

Tentamos usar `window.scrollY` para esconder o indicador "Role para explorar" no final da pagina. Nao funcionava. A solucao: usar o callback `onStepEnter` do scrollama, que funciona independente de onde o scroll acontece:

```javascript
scroller.onStepEnter(function(response) {
  var allSteps = document.querySelectorAll(".step");
  var scrollCue = document.getElementById("scrollCue");
  if (scrollCue) {
    scrollCue.style.display = (response.index >= allSteps.length - 1) ? "none" : "";
  }
});
```

**Regra:** Nos templates de scrollytelling, NUNCA usar `window.scrollY` ou `window.pageYOffset`. Usar `document.documentElement.scrollTop` ou, melhor ainda, callbacks do scrollama.

### Indicador "Role para explorar"

Todo scrollytelling tem um indicador fixo no rodape da tela com texto "Role para explorar" e 3 chevrons animados em verde (#0B9247) com animacao staggered (cada seta aparece com delay de 0.25s). O indicador some automaticamente quando o scrollama detecta o ultimo step. CSS puro, sem bibliotecas.

---

## Proximos Passos

1. ~~Subir repo no GitHub e ativar GitHub Pages~~ ✓ Feito
2. ~~Testar o workflow completo~~ ✓ Feito (infograficos de roubos no centro de SP)
3. **Iterar nos templates** — ajustar detalhes visuais conforme feedback do time de arte
4. ~~Novos tipos de template~~ ✓ Mapa coropletico (7o) e scrollytelling-mapa (8o) adicionados
5. ~~Mobile do scrollytelling~~ ✓ Overlay pattern implementado (mapa 85vh + cards flutuantes)
6. **Novos formatos** — donut chart, treemap, scatter plot se surgirem necessidades
