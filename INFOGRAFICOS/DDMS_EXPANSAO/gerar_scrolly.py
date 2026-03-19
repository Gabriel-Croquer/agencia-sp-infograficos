#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gera o scrollytelling da expansao da rede DDMs em SP."""

import json, csv, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, '..', '..')
TEMPLATES = os.path.join(ROOT, 'templates')
OUT = os.path.join(BASE, 'ddms-expansao-scrolly.html')

# ============================================================
# 1. LER DADOS
# ============================================================

# GeoJSON de municipios de SP
with open(os.path.join(TEMPLATES, 'sp_municipios_2024.geojson'), encoding='utf-8') as f:
    geojson = json.load(f)

# DDMs presenciais
ddms = []
with open(os.path.join(BASE, 'ddm-presenciais-geo-v2.csv'), encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        try:
            ddms.append({
                'lat': float(row['latitude']),
                'lng': float(row['longitude']),
                'nome': row['unidade'],
                'municipio': row['municipio'],
                'h24': row['funciona_24h'] == 'Sim',
                'code': row['code_muni'].split('.')[0]
            })
        except (ValueError, KeyError):
            pass

# Salas DDM Online (split por periodo)
salas_pre, salas_pos = [], []
with open(os.path.join(BASE, 'salas-ddm-online-geo.csv'), encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        try:
            entry = {
                'lat': float(row['latitude']),
                'lng': float(row['longitude']),
                'nome': row['unidade'],
                'municipio': row['municipio'],
                'ano': int(row['ano']),
                'code': row['code_muni'].split('.')[0]
            }
            if entry['ano'] < 2023:
                salas_pre.append(entry)
            else:
                salas_pos.append(entry)
        except (ValueError, KeyError):
            pass

# Salas futuras
futuras = []
with open(os.path.join(BASE, 'salas-ddm-futuras.csv'), encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        try:
            futuras.append({
                'lat': float(row['latitude']),
                'lng': float(row['longitude']),
                'nome': row['unidade'],
                'municipio': row['municipio'],
                'code': row['code_muni'].split('.')[0]
            })
        except (ValueError, KeyError):
            pass

# ============================================================
# 2. COBERTURA POR MUNICIPIO
# ============================================================

cob = {}
def ensure(code):
    if code and code not in cob:
        cob[code] = {'ddm': 0, 'sp': 0, 'sn': 0, 'fut': 0}

for d in ddms:
    if d['code']: ensure(d['code']); cob[d['code']]['ddm'] += 1
for s in salas_pre:
    if s['code']: ensure(s['code']); cob[s['code']]['sp'] += 1
for s in salas_pos:
    if s['code']: ensure(s['code']); cob[s['code']]['sn'] += 1
for ff in futuras:
    if ff['code']: ensure(ff['code']); cob[ff['code']]['fut'] += 1

# ============================================================
# 3. REGIOES PARA ZOOM
# ============================================================

regioes_rmsp = set()
regioes_campinas = set()
regioes_pp = set()
regioes_reg = set()

for src in [os.path.join(BASE, 'salas-ddm-online-geo.csv'), os.path.join(BASE, 'ddm-presenciais-geo-v2.csv')]:
    with open(src, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            sec = row.get('seccional', '').strip().upper()
            dep = row.get('departamento', '').strip().upper()
            code = row['code_muni'].split('.')[0]
            if not code: continue
            if dep in ('DEMACRO', 'DECAP'):
                regioes_rmsp.add(code)
            if 'CAMPINAS' in sec:
                regioes_campinas.add(code)
            if 'PRUDENTE' in sec:
                regioes_pp.add(code)
            if 'REGISTRO' in sec:
                regioes_reg.add(code)

# Adicionar municipios vizinhos de Campinas para zoom mais amplo
# (os que tem cobertura na regiao)
for src in [os.path.join(BASE, 'salas-ddm-online-geo.csv')]:
    with open(src, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            sec = row.get('seccional', '').strip().upper()
            code = row['code_muni'].split('.')[0]
            if not code: continue
            if any(x in sec for x in ['PIRACICABA', 'JUNDIAI', 'AMERICANA', 'LIMEIRA', 'RIO CLARO', 'SOROCABA']):
                regioes_campinas.add(code)

# ============================================================
# 4. EXTRAIR LOGO BASE64
# ============================================================

logo_b64 = ''
test_scrolly = os.path.join(ROOT, 'INFOGRAFICOS', 'TESTE_SCROLLYTELLING', 'teste_scrolly.html')
if os.path.exists(test_scrolly):
    with open(test_scrolly, encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'src="(data:image/png;base64,[^"]+)"', content)
    if m:
        logo_b64 = m.group(1)

# ============================================================
# 5. CAPITULOS
# ============================================================

capitulos = [
    {
        "titulo": "A rede de proteção em 2022",
        "texto": "Em três anos, a atual gestão do Governo de São Paulo <strong>aumentou em 54%</strong> a rede de proteção às mulheres em delegacias. Em 2022, o estado contava com 205 espaços — 143 Delegacias da Mulher e 62 salas DDM Online — em 146 municípios.",
        "mapState": {
            "shapes": "pre2023",
            "layers": [],
            "zoom": "full",
            "legenda": [
                {"cor": "#7B68AE", "texto": "Municípios com DDM ou Sala DDM Online (2022)"}
            ]
        }
    },
    {
        "titulo": "A expansão da rede",
        "texto": "Hoje, são <strong>316 espaços</strong> em <strong>196 municípios</strong>, cobrindo todas as 16 regiões administrativas do estado. Os municípios em destaque ganharam cobertura pela primeira vez.",
        "mapState": {
            "shapes": "atual",
            "layers": [],
            "zoom": "full",
            "legenda": [
                {"cor": "#7B68AE", "texto": "Cobertura anterior a 2023"},
                {"cor": "#E74C3C", "texto": "Municípios que ganharam cobertura"}
            ]
        }
    },
    {
        "titulo": "Salas DDM Online puxam a expansão",
        "texto": "A criação de <strong>111 novas Salas DDM Online</strong> puxou a expansão. Estes espaços operam em delegacias comuns, onde oferecem ambiente específico para acolher vítimas de violência de gênero.",
        "mapState": {
            "shapes": "neutro",
            "layers": ["sala_pre", "sala_pos"],
            "zoom": "full",
            "legenda": [
                {"cor": "#5DADE2", "texto": "Salas DDM Online (antes de 2023)"},
                {"cor": "#E74C3C", "texto": "Salas inauguradas na gestão atual"}
            ]
        }
    },
    {
        "titulo": "Região Metropolitana de SP",
        "texto": "As novas salas tornaram mais fácil para mulheres denunciarem agressores na Região Metropolitana de São Paulo, que passou de <strong>6 para 39 salas</strong> neste período.",
        "mapState": {
            "shapes": "neutro",
            "layers": ["sala_pre", "sala_pos", "ddm"],
            "zoom": {"codigos": list(regioes_rmsp)},
            "legenda": [
                {"cor": "#9B59B6", "texto": "DDM presencial"},
                {"cor": "#5DADE2", "texto": "Sala DDM Online (pré-2023)"},
                {"cor": "#E74C3C", "texto": "Sala inaugurada 2023+"}
            ]
        }
    },
    {
        "titulo": "Região de Campinas",
        "texto": "Outra região com crescimento destaque: Campinas, onde o número de espaços de atendimento <strong>mais que dobrou</strong>, de 14 para 35 salas.",
        "mapState": {
            "shapes": "neutro",
            "layers": ["sala_pre", "sala_pos", "ddm"],
            "zoom": {"codigos": list(regioes_campinas)},
            "legenda": [
                {"cor": "#9B59B6", "texto": "DDM presencial"},
                {"cor": "#5DADE2", "texto": "Sala DDM Online (pré-2023)"},
                {"cor": "#E74C3C", "texto": "Sala inaugurada 2023+"}
            ]
        }
    },
    {
        "titulo": "Expansão no interior",
        "texto": "A expansão também chegou ao interior do estado, especialmente no <strong>extremo oeste</strong> (Presidente Prudente) e <strong>extremo sul</strong> (Registro), regiões que antes tinham pouca ou nenhuma cobertura de salas DDM Online.",
        "mapState": {
            "shapes": "neutro",
            "layers": ["sala_pre", "sala_pos", "ddm"],
            "zoom": {"codigos": list(regioes_pp | regioes_reg)},
            "legenda": [
                {"cor": "#9B59B6", "texto": "DDM presencial"},
                {"cor": "#5DADE2", "texto": "Sala DDM Online (pré-2023)"},
                {"cor": "#E74C3C", "texto": "Sala inaugurada 2023+"}
            ]
        }
    },
    {
        "titulo": "O futuro da rede",
        "texto": "Para os próximos meses, a previsão é inaugurar mais <strong>60 salas DDM Online</strong>. Com a expansão, delegacias de 48 novas cidades passarão a ter acesso à rede de proteção. Ao todo, serão <strong>244 municípios</strong> com cobertura — quase 40% do total do estado.",
        "mapState": {
            "shapes": "futuro",
            "layers": [],
            "zoom": "full",
            "legenda": [
                {"cor": "#7B68AE", "texto": "Cobertura atual"},
                {"cor": "#2ECC71", "texto": "Municípios com cobertura futura", "borda": True}
            ]
        }
    }
]

# ============================================================
# 6. SERIALIZAR DADOS
# ============================================================

geojson_str = json.dumps(geojson, ensure_ascii=False, separators=(',', ':'))
ddm_str = json.dumps(ddms, ensure_ascii=False, separators=(',', ':'))
sala_pre_str = json.dumps(salas_pre, ensure_ascii=False, separators=(',', ':'))
sala_pos_str = json.dumps(salas_pos, ensure_ascii=False, separators=(',', ':'))
futuras_str = json.dumps(futuras, ensure_ascii=False, separators=(',', ':'))
cob_str = json.dumps(cob, ensure_ascii=False, separators=(',', ':'))
cap_str = json.dumps(capitulos, ensure_ascii=False, indent=2)

# ============================================================
# 7. GERAR HTML
# ============================================================

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rede de proteção à mulher em SP</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
  <script src="https://unpkg.com/scrollama"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    html, body {{
      height: 100%;
      overflow-y: auto;
      overflow-x: hidden;
    }}
    html {{ scrollbar-width: none; -ms-overflow-style: none; }}
    html::-webkit-scrollbar {{ display: none; }}

    body {{
      font-family: 'Montserrat', sans-serif;
      background: #1a1a2e;
      color: #ffffff;
      padding: 20px 20px 10px;
    }}

    .scrolly-container {{
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
    }}

    .scrolly-header {{
      max-width: 700px;
      margin-bottom: 24px;
    }}

    .chart-title {{
      font-size: 26px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 8px;
      color: #ffffff;
    }}
    .chart-title .destaque {{ color: #E74C3C; }}

    .chart-subtitle {{
      font-size: 14px;
      font-weight: 400;
      line-height: 1.6;
      color: rgba(255,255,255,0.7);
    }}

    .scrolly {{
      display: flex;
      position: relative;
    }}

    .scrolly__map {{
      flex: 0 0 58%;
      position: sticky;
      top: 0;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 20px 16px;
    }}

    .map-area {{
      width: 100%;
      position: relative;
    }}
    .map-area svg {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .map-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 14px;
      justify-content: center;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      color: rgba(255,255,255,0.8);
      font-weight: 600;
    }}
    .legend-swatch {{
      width: 14px;
      height: 14px;
      border-radius: 3px;
      border: 1px solid rgba(255,255,255,0.2);
    }}

    .scrolly__text {{
      flex: 0 0 42%;
      padding: 0 20px;
    }}

    .step {{
      min-height: 80vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 32px 0;
      opacity: 0.2;
      transition: opacity 0.5s ease;
    }}
    .step.is-active {{ opacity: 1; }}
    .step:first-child {{ margin-top: 30vh; }}
    .step:last-child {{ margin-bottom: 40vh; }}

    .step h3 {{
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 12px;
      color: #ffffff;
      border-left: 4px solid #E74C3C;
      padding-left: 12px;
    }}
    .step p {{
      font-size: 15px;
      line-height: 1.7;
      color: rgba(255,255,255,0.85);
    }}
    .step p strong {{
      color: #E74C3C;
      font-weight: 700;
    }}

    .tooltip {{
      position: fixed;
      pointer-events: none;
      background: rgba(0,0,0,0.9);
      color: #fff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-family: 'Montserrat', sans-serif;
      display: none;
      z-index: 999;
      border: 1px solid rgba(255,255,255,0.15);
    }}

    .chart-source {{
      font-size: 11px;
      color: rgba(255,255,255,0.5);
      margin-top: 20px;
    }}
    .logo-container {{
      text-align: center;
      margin-top: 16px;
    }}
    .logo-container img {{
      height: 36px;
      opacity: 0.8;
    }}

    .step-indicator {{
      position: fixed;
      right: 20px;
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 100;
    }}
    .step-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: rgba(255,255,255,0.3);
      transition: all 0.3s ease;
    }}
    .step-dot.is-active {{
      background: #E74C3C;
      transform: scale(1.5);
    }}

    /* === INDICADOR DE SCROLL === */
    .scroll-cue {{
      position: fixed;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 50;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      pointer-events: none;
      transition: opacity 0.5s ease;
    }}
    .scroll-cue-text {{
      font-family: 'Montserrat', sans-serif;
      font-size: 11px;
      font-weight: 600;
      color: #E74C3C;
      letter-spacing: 0.5px;
    }}
    .scroll-cue-arrows {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0;
    }}
    .scroll-cue-arrows span {{
      display: block;
      width: 14px;
      height: 14px;
      border-right: 2px solid #E74C3C;
      border-bottom: 2px solid #E74C3C;
      transform: rotate(45deg);
    }}
    .scroll-cue-arrows span:nth-child(1) {{ animation: scrollFlow 1.8s infinite; }}
    .scroll-cue-arrows span:nth-child(2) {{ animation: scrollFlow 1.8s infinite 0.25s; }}
    .scroll-cue-arrows span:nth-child(3) {{ animation: scrollFlow 1.8s infinite 0.5s; }}
    @keyframes scrollFlow {{
      0% {{ opacity: 0; transform: rotate(45deg) translateY(-6px); }}
      30% {{ opacity: 1; }}
      70% {{ opacity: 1; }}
      100% {{ opacity: 0; transform: rotate(45deg) translateY(6px); }}
    }}

    .scrolly-footer {{
      padding: 20px 0;
    }}

    /* === MOBILE OVERLAY === */
    @media (max-width: 768px) {{
      body {{ padding: 0; }}
      .scrolly-container {{ padding: 0; }}
      .scrolly-header {{ padding: 12px 16px; max-width: 100%; }}
      .chart-title {{ font-size: 20px; }}
      .chart-subtitle {{ font-size: 12px; }}
      .scrolly {{ flex-direction: column; }}

      .scrolly__map {{
        flex: none;
        width: 100%;
        height: 85vh;
        position: sticky;
        top: 0;
        z-index: 1;
        background: #1a1a2e;
        padding: 16px 8px 8px;
        justify-content: center;
        align-items: center;
        box-shadow: none;
      }}
      .scrolly__map .map-area {{
        height: calc(85vh - 60px);
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .scrolly__map .map-area svg {{
        max-height: 100%;
        max-width: 100%;
        width: auto;
        margin: 0 auto;
      }}
      .scrolly__map .map-legend {{
        position: absolute;
        bottom: 8px;
        left: 0;
        right: 0;
        margin-top: 0;
        gap: 6px;
        justify-content: center;
        background: rgba(26, 26, 46, 0.9);
        padding: 4px 8px;
        border-radius: 4px;
      }}
      .scrolly__map .map-legend .legend-item {{ font-size: 10px; }}
      .scrolly__map .map-legend .legend-swatch {{ width: 10px; height: 10px; }}

      .scrolly__text {{
        flex: none;
        width: 100%;
        position: relative;
        z-index: 2;
        padding: 0 20px;
        pointer-events: none;
      }}

      .step {{
        min-height: auto;
        padding: 20px 20px;
        margin: 0 auto;
        max-width: 320px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.4);
        pointer-events: auto;
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
      }}
      .step h3 {{ font-size: 16px; color: #1D1D1B; }}
      .step p {{ font-size: 14px; color: #333; }}
      .step p strong {{ color: #E74C3C; }}
      .step:first-child {{ margin-top: 40vh; }}
      .step:last-child {{ margin-bottom: 80vh; }}

      .step-indicator {{ display: none; }}
      .scrolly-footer {{ padding: 0 16px; }}
    }}
  </style>
</head>
<body>
  <div class="scrolly-container">
    <div class="scrolly-header">
      <div class="chart-title">Como a rede de proteção à mulher em delegacias <span class="destaque">aumentou 54%</span> em três anos</div>
      <div class="chart-subtitle">Gestão atual instalou duas Delegacias da Mulher e 173 salas DDM Online em delegacias desde 2023. Estrutura cobre 196 municípios em todas as 16 regiões administrativas do estado</div>
    </div>

    <div class="scrolly" id="scrolly">
      <div class="scrolly__map" id="scrollyMap">
        <div class="map-area" id="mapArea"></div>
        <div class="map-legend" id="legend"></div>
      </div>
      <div class="scrolly__text" id="scrollyText"></div>
    </div>

    <div class="scroll-cue" id="scrollCue">
      <span class="scroll-cue-text">Role para explorar</span>
      <div class="scroll-cue-arrows">
        <span></span><span></span><span></span>
      </div>
    </div>

    <div class="scrolly-footer">
      <div class="tooltip" id="tooltip"></div>
      <p class="chart-source">Fonte: SSP-SP e IBGE</p>
      <div class="logo-container">
        <img alt="Agência SP" src="{logo_b64}" />
      </div>
    </div>
  </div>

  <div class="step-indicator" id="stepIndicator"></div>

<script>
(function() {{
  "use strict";

  // === CONFIG ===
  var CONFIG = {{
    geojson: {geojson_str},
    cobertura: {cob_str},
    pontos: {{
      ddm: {ddm_str},
      sala_pre: {sala_pre_str},
      sala_pos: {sala_pos_str},
      futuras: {futuras_str}
    }},
    capitulos: {cap_str}
  }};

  // === GERAR STEPS ===
  var textContainer = document.getElementById("scrollyText");
  CONFIG.capitulos.forEach(function(cap, i) {{
    var step = document.createElement("div");
    step.className = "step";
    step.setAttribute("data-step", i);
    step.innerHTML = "<h3>" + cap.titulo + "</h3><p>" + cap.texto + "</p>";
    textContainer.appendChild(step);
  }});

  // === GERAR DOTS DE PROGRESSO ===
  var indicator = document.getElementById("stepIndicator");
  CONFIG.capitulos.forEach(function(_, i) {{
    var dot = document.createElement("div");
    dot.className = "step-dot";
    dot.setAttribute("data-index", i);
    indicator.appendChild(dot);
  }});

  // === D3 MAP SETUP ===
  var mapEl = document.getElementById("mapArea");
  var width = mapEl.clientWidth || 700;
  var height = Math.round(width * 0.75);

  var svg = d3.select("#mapArea").append("svg")
    .attr("viewBox", "0 0 " + width + " " + height)
    .attr("preserveAspectRatio", "xMidYMid meet");

  var g = svg.append("g");
  var projection = d3.geoMercator().fitSize([width, height], CONFIG.geojson);
  var path = d3.geoPath().projection(projection);

  // Shapes de municipios
  var shapes = g.selectAll("path.muni")
    .data(CONFIG.geojson.features)
    .enter().append("path")
    .attr("class", "muni")
    .attr("d", path)
    .attr("fill", "#2a2a4a")
    .attr("stroke", "rgba(255,255,255,0.08)")
    .attr("stroke-width", 0.5)
    .on("mouseover", function(event, d) {{
      var code = d.properties.CD_MUN;
      var nome = d.properties.NM_MUN;
      var c = CONFIG.cobertura[code];
      var info = nome;
      if (c) {{
        var parts = [];
        if (c.ddm) parts.push(c.ddm + " DDM");
        if (c.sp) parts.push(c.sp + " sala pré-2023");
        if (c.sn) parts.push(c.sn + " sala 2023+");
        if (c.fut) parts.push(c.fut + " sala futura");
        if (parts.length) info += " — " + parts.join(", ");
      }}
      var tip = document.getElementById("tooltip");
      tip.innerHTML = info;
      tip.style.display = "block";
      tip.style.left = event.clientX + 12 + "px";
      tip.style.top = event.clientY - 10 + "px";
    }})
    .on("mousemove", function(event) {{
      var tip = document.getElementById("tooltip");
      tip.style.left = event.clientX + 12 + "px";
      tip.style.top = event.clientY - 10 + "px";
    }})
    .on("mouseout", function() {{
      document.getElementById("tooltip").style.display = "none";
    }});

  // === CAMADAS DE CENTROIDES ===
  var layers = {{}};
  var layerConfig = {{
    ddm: {{ data: CONFIG.pontos.ddm, cor: "#9B59B6", r: 3.5 }},
    sala_pre: {{ data: CONFIG.pontos.sala_pre, cor: "#5DADE2", r: 3.5 }},
    sala_pos: {{ data: CONFIG.pontos.sala_pos, cor: "#E74C3C", r: 4 }},
    futuras: {{ data: CONFIG.pontos.futuras, cor: "#2ECC71", r: 3.5, opacity: 0.6 }}
  }};

  Object.keys(layerConfig).forEach(function(key) {{
    var cfg = layerConfig[key];
    var lg = g.append("g").attr("class", "layer-" + key).style("display", "none");
    cfg.data.forEach(function(p) {{
      var coords = projection([p.lng, p.lat]);
      if (coords) {{
        lg.append("circle")
          .attr("cx", coords[0])
          .attr("cy", coords[1])
          .attr("r", cfg.r)
          .attr("data-r", cfg.r)
          .attr("fill", cfg.cor)
          .attr("fill-opacity", cfg.opacity || 0.85)
          .attr("stroke", "#fff")
          .attr("stroke-width", 0.5)
          .attr("stroke-opacity", 0.4);
      }}
    }});
    layers[key] = lg;
  }});

  // === ZOOM ===
  var currentScale = 1;

  function zoomToCodigos(codigos) {{
    var features = CONFIG.geojson.features.filter(function(f) {{
      return codigos.indexOf(f.properties.CD_MUN) >= 0;
    }});
    if (!features.length) return;

    var bounds = [[Infinity, Infinity], [-Infinity, -Infinity]];
    features.forEach(function(f) {{
      var b = path.bounds(f);
      bounds[0][0] = Math.min(bounds[0][0], b[0][0]);
      bounds[0][1] = Math.min(bounds[0][1], b[0][1]);
      bounds[1][0] = Math.max(bounds[1][0], b[1][0]);
      bounds[1][1] = Math.max(bounds[1][1], b[1][1]);
    }});

    var dx = bounds[1][0] - bounds[0][0];
    var dy = bounds[1][1] - bounds[0][1];
    var x = (bounds[0][0] + bounds[1][0]) / 2;
    var y = (bounds[0][1] + bounds[1][1]) / 2;
    var scale = Math.max(1, Math.min(10, 0.85 / Math.max(dx / width, dy / height)));
    var tx = width / 2 - scale * x;
    var ty = height / 2 - scale * y;

    currentScale = scale;
    g.interrupt();
    g.transition().duration(800)
      .attr("transform", "translate(" + tx + "," + ty + ") scale(" + scale + ")");

    // Counter-scale
    setTimeout(function() {{
      g.selectAll("path.muni").attr("stroke-width", 0.5 / scale);
      g.selectAll("circle")
        .attr("r", function() {{ return parseFloat(d3.select(this).attr("data-r")) / Math.sqrt(scale); }})
        .attr("stroke-width", 0.5 / scale);
    }}, 850);
  }}

  function resetZoom() {{
    currentScale = 1;
    g.interrupt();
    g.transition().duration(800)
      .attr("transform", "translate(0,0) scale(1)");
    setTimeout(function() {{
      g.selectAll("path.muni").attr("stroke-width", 0.5);
      g.selectAll("circle")
        .attr("r", function() {{ return parseFloat(d3.select(this).attr("data-r")); }})
        .attr("stroke-width", 0.5);
    }}, 850);
  }}

  // === COLORIR SHAPES ===
  function colorShapes(mode) {{
    shapes.interrupt();
    shapes.transition().duration(600)
      .attr("fill", function(d) {{
        var code = d.properties.CD_MUN;
        var c = CONFIG.cobertura[code];
        if (!c) {{
          if (mode === "neutro") return "#1e1e38";
          return "#2a2a4a";
        }}
        switch(mode) {{
          case "pre2023":
            return (c.ddm || c.sp) ? "#7B68AE" : "#2a2a4a";
          case "atual":
            if (c.sn && !c.ddm && !c.sp) return "#E74C3C";
            if (c.ddm || c.sp) return "#7B68AE";
            return "#2a2a4a";
          case "futuro":
            if (c.fut && !c.ddm && !c.sp && !c.sn) return "rgba(46,204,113,0.5)";
            if (c.ddm || c.sp || c.sn) return "#7B68AE";
            return "#2a2a4a";
          case "neutro":
          default:
            return "#1e1e38";
        }}
      }});
  }}

  // === TOGGLE CENTROID LAYERS ===
  function toggleLayers(activeList) {{
    Object.keys(layers).forEach(function(key) {{
      layers[key].transition().duration(400)
        .style("opacity", activeList.indexOf(key) >= 0 ? 1 : 0)
        .on("end", function() {{
          layers[key].style("display", activeList.indexOf(key) >= 0 ? "block" : "none");
        }});
      if (activeList.indexOf(key) >= 0) {{
        layers[key].style("display", "block");
      }}
    }});
  }}

  // === LEGENDA ===
  function updateLegend(items) {{
    var leg = document.getElementById("legend");
    leg.innerHTML = "";
    if (!items || !items.length) return;
    items.forEach(function(item) {{
      var div = document.createElement("div");
      div.className = "legend-item";
      var swatch = document.createElement("div");
      swatch.className = "legend-swatch";
      swatch.style.background = item.borda ? "transparent" : item.cor;
      if (item.borda) {{
        swatch.style.border = "2px solid " + item.cor;
      }}
      var label = document.createElement("span");
      label.textContent = item.texto;
      div.appendChild(swatch);
      div.appendChild(label);
      leg.appendChild(div);
    }});
  }}

  // === APPLY MAP STATE ===
  function applyMapState(index) {{
    var state = CONFIG.capitulos[index].mapState;

    // Shapes
    colorShapes(state.shapes || "neutro");

    // Centroids
    toggleLayers(state.layers || []);

    // Zoom
    if (state.zoom === "full") {{
      resetZoom();
    }} else if (state.zoom && state.zoom.codigos) {{
      zoomToCodigos(state.zoom.codigos);
    }}

    // Legenda
    updateLegend(state.legenda);

    // Dots de progresso
    document.querySelectorAll(".step-dot").forEach(function(dot, i) {{
      dot.classList.toggle("is-active", i === index);
    }});
  }}

  // === SCROLLAMA ===
  var scroller = scrollama();
  var isMobile = window.innerWidth <= 768;

  scroller.setup({{
    step: ".step",
    offset: isMobile ? 0.65 : 0.5,
    debug: false
  }}).onStepEnter(function(response) {{
    applyMapState(response.index);
    var allSteps = document.querySelectorAll(".step");
    allSteps.forEach(function(s) {{ s.classList.remove("is-active"); }});
    response.element.classList.add("is-active");

    // Esconde indicador de scroll no ultimo step
    var scrollCue = document.getElementById("scrollCue");
    if (scrollCue) {{
      scrollCue.style.display = (response.index >= allSteps.length - 1) ? "none" : "";
    }}
  }});

  window.addEventListener("resize", scroller.resize);

  // Mobile: spacing entre cards
  if (isMobile) {{
    function setMobileStepSpacing() {{
      var spacing = Math.round(window.innerHeight * 0.85);
      document.querySelectorAll('.step').forEach(function(step, i, arr) {{
        if (i < arr.length - 1) step.style.marginBottom = spacing + 'px';
      }});
      scroller.resize();
    }}
    setMobileStepSpacing();
    window.addEventListener('resize', setMobileStepSpacing);
  }}

  // Estado inicial
  applyMapState(0);
  var firstStep = document.querySelector(".step");
  if (firstStep) firstStep.classList.add("is-active");

}})();
</script>
</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Gerado: {OUT}")
print(f"Tamanho: {os.path.getsize(OUT) / 1024:.0f} KB")
print(f"DDMs: {len(ddms)}, Salas pre: {len(salas_pre)}, Salas pos: {len(salas_pos)}, Futuras: {len(futuras)}")
print(f"Municipios com cobertura: {len(cob)}")
print(f"Capitulos: {len(capitulos)}")
