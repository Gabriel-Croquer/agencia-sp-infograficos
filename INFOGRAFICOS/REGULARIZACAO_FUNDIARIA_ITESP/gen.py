# Gera os dois HTMLs do infografico Itesp
from pathlib import Path

BASE = Path(__file__).parent
LOGO = (BASE / "logo_base64.txt").read_text().strip()

# ======================================================
# INFOGRAFICO 1 - HECTARES POR ANO
# ======================================================

HECTARES_TOTAL = {
    2011: 412.7951, 2012: 889.2266, 2013: 421.9973, 2014: 108.477,
    2015: 2355.253, 2016: 5684.947, 2017: 1708.342, 2018: 559.4231,
    2019: 1479.639, 2020: 143.0386, 2021: 428.509,  2022: 2152.702,
    2023: 58354.43, 2024: 80913.71, 2025: 95140.9,  2026: 3316.971,
}

anos = list(HECTARES_TOTAL.keys())
vals = list(HECTARES_TOTAL.values())

# Soma 2011-2022 (contexto da linha fina)
soma_ate_2022 = sum(v for a, v in HECTARES_TOTAL.items() if a <= 2022)
# = 16343

HTML1 = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Regularizacao de terras dispara em SP a partir de 2023</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ height: auto; overflow: hidden; }}
    body {{
      font-family: 'Montserrat', sans-serif;
      background: #FFFFFF;
      color: #1D1D1B;
      display: flex;
      justify-content: center;
      padding: 20px 20px 10px;
    }}
    .infographic {{ width: 100%; max-width: 960px; }}

    .main-title {{
      font-size: 24px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 6px;
      color: #1D1D1B;
    }}
    .main-title .destaque {{ color: #0B9247; }}

    .main-subtitle {{
      font-size: 15px;
      font-weight: 400;
      color: #444;
      line-height: 1.4;
      margin-bottom: 20px;
    }}

    .legend {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 16px;
      font-size: 12px;
      color: #555;
      flex-wrap: wrap;
    }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; }}
    .legend-swatch {{ width: 14px; height: 14px; border-radius: 2px; }}

    .chart-container {{ position: relative; margin-bottom: 16px; }}

    .chart-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
      flex-wrap: wrap;
    }}
    .chart-badge {{
      display: inline-block;
      font-size: 13px;
      font-weight: 700;
      color: #0B9247;
      background: #E8F5E9;
      border-radius: 4px;
      padding: 2px 10px;
    }}

    .chart-container svg {{ width: 100%; height: auto; display: block; }}

    .bar-rect {{ cursor: pointer; transition: opacity 0.2s ease; }}
    .bar-rect:hover {{ opacity: 0.8; }}

    .tooltip {{
      position: fixed;
      pointer-events: none;
      background: #1D1D1B;
      color: #fff;
      font-family: 'Montserrat', sans-serif;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 10px;
      border-radius: 4px;
      line-height: 1.4;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.15s ease;
      z-index: 100;
    }}
    .tooltip.visible {{ opacity: 1; }}

    .chart-source {{ font-size: 12px; color: #808080; margin-top: 12px; line-height: 1.4; }}

    .logo-container {{ text-align: center; margin-top: 16px; }}
    .logo-container img {{ height: 32px; }}

    @media (max-width: 600px) {{
      .main-title {{ font-size: 20px; }}
      .main-subtitle {{ font-size: 13px; }}
    }}
  </style>
</head>
<body>

<div class="infographic">
  <div class="main-title">
    Regularizacao de terras <span class="destaque">dispara em SP</span> a partir de 2023
  </div>
  <div class="main-subtitle">
    O Itesp titulou mais hectares em 2025 (95,1 mil) do que em todo o periodo de 2011 a 2022 somado (16,3 mil)
  </div>

  <div class="legend">
    <div class="legend-item">
      <div class="legend-swatch" style="background:#C0C0C0;"></div>
      <span>2011-2022</span>
    </div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#0B9247;"></div>
      <span>2023-2025 (gestao atual)</span>
    </div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:url(#hatch-green);background:repeating-linear-gradient(45deg,#0B9247 0 4px,#7FCB9F 4px 8px);"></div>
      <span>2026 (1&ordm; trimestre)</span>
    </div>
  </div>

  <div class="chart-container">
    <div class="chart-header">
      <span class="chart-badge">Hectares regularizados por ano</span>
    </div>
    <svg id="chart" viewBox="0 0 900 360" preserveAspectRatio="xMidYMid meet"></svg>
  </div>

  <div class="chart-source">
    Fonte: Fundacao Itesp / Secretaria de Agricultura e Abastecimento do Estado de Sao Paulo.<br>
    Dados de 2026 correspondem apenas ao 1&ordm; trimestre.
  </div>

  <div class="logo-container">
    <img src="{LOGO}" alt="Agencia SP">
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
var years = {anos};
var data  = {vals};

var GREEN = "#0B9247";
var GRAY  = "#C0C0C0";
var HATCH_ID = "hatch-green";
var tooltipEl = document.getElementById("tooltip");

function formatNum(n) {{
  // n em hectares com ate 2 casas
  if (n >= 1000) {{
    return (n/1000).toFixed(1).replace(".", ",") + " mil ha";
  }}
  return n.toFixed(0).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " ha";
}}

function formatShort(n) {{
  if (n >= 1000) return (n/1000).toFixed(n >= 10000 ? 0 : 1).replace(".", ",") + " mil";
  return n.toFixed(0);
}}

(function buildChart() {{
  var svg = document.getElementById("chart");
  var n = data.length;
  var maxVal = Math.max.apply(null, data);

  // Escala arredondada
  var yMax = 100000; // 100 mil hectares

  var svgW = 900, svgH = 360;
  var ml = 60, mr = 20, mt = 40, mb = 40;
  var plotW = svgW - ml - mr;
  var plotH = svgH - mt - mb;

  var barW = Math.floor(plotW / n * 0.78);
  var gap = (plotW - barW * n) / n;

  // Defs: padrao hachurado para 2026 (1T)
  var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  var pat = document.createElementNS("http://www.w3.org/2000/svg", "pattern");
  pat.setAttribute("id", HATCH_ID);
  pat.setAttribute("patternUnits", "userSpaceOnUse");
  pat.setAttribute("width", "8");
  pat.setAttribute("height", "8");
  pat.setAttribute("patternTransform", "rotate(45)");
  var patBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  patBg.setAttribute("width", "8");
  patBg.setAttribute("height", "8");
  patBg.setAttribute("fill", "#0B9247");
  pat.appendChild(patBg);
  var patLine = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  patLine.setAttribute("width", "4");
  patLine.setAttribute("height", "8");
  patLine.setAttribute("fill", "#7FCB9F");
  pat.appendChild(patLine);
  defs.appendChild(pat);
  svg.appendChild(defs);

  // Y axis
  var nTicks = 5;
  for (var t = 0; t <= nTicks; t++) {{
    var val = (yMax / nTicks) * t;
    var yPos = mt + plotH - (val / yMax) * plotH;

    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", ml);
    line.setAttribute("x2", svgW - mr);
    line.setAttribute("y1", yPos);
    line.setAttribute("y2", yPos);
    line.setAttribute("stroke", "#E5E5E5");
    line.setAttribute("stroke-width", "1");
    svg.appendChild(line);

    var label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", ml - 8);
    label.setAttribute("y", yPos + 4);
    label.setAttribute("text-anchor", "end");
    label.setAttribute("font-size", "11");
    label.setAttribute("fill", "#999");
    label.setAttribute("font-family", "Montserrat, sans-serif");
    var txt = val === 0 ? "0" : (val/1000).toFixed(0) + " mil ha";
    label.textContent = txt;
    svg.appendChild(label);
  }}

  // Bars
  var barsInfo = [];
  for (var i = 0; i < n; i++) {{
    var x = ml + gap / 2 + i * (barW + gap);
    var h = data[i] > 0 ? (data[i] / yMax) * plotH : 0;
    var y = mt + plotH - h;
    var yr = years[i];

    var fill = GRAY;
    if (yr === 2023 || yr === 2024 || yr === 2025) fill = GREEN;
    if (yr === 2026) fill = "url(#" + HATCH_ID + ")";

    var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("class", "bar-rect");
    rect.setAttribute("x", x);
    rect.setAttribute("y", mt + plotH);
    rect.setAttribute("width", barW);
    rect.setAttribute("height", 0);
    rect.setAttribute("rx", "2");
    rect.setAttribute("fill", fill);
    rect.dataset.year = yr;
    rect.dataset.value = data[i];
    svg.appendChild(rect);
    barsInfo.push({{ el: rect, targetY: y, targetH: h }});

    // X label - todos os anos
    var xLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    xLabel.setAttribute("x", x + barW/2);
    xLabel.setAttribute("y", mt + plotH + 18);
    xLabel.setAttribute("text-anchor", "middle");
    xLabel.setAttribute("font-size", "10");
    xLabel.setAttribute("fill", (yr>=2023) ? "#1D1D1B" : "#777");
    xLabel.setAttribute("font-weight", (yr>=2023) ? "700" : "400");
    xLabel.setAttribute("font-family", "Montserrat, sans-serif");
    xLabel.textContent = String(yr);
    svg.appendChild(xLabel);

    // 2026 marker "1T"
    if (yr === 2026) {{
      var tag = document.createElementNS("http://www.w3.org/2000/svg", "text");
      tag.setAttribute("x", x + barW/2);
      tag.setAttribute("y", mt + plotH + 32);
      tag.setAttribute("text-anchor", "middle");
      tag.setAttribute("font-size", "9");
      tag.setAttribute("fill", "#0B9247");
      tag.setAttribute("font-weight", "700");
      tag.setAttribute("font-family", "Montserrat, sans-serif");
      tag.textContent = "(1T)";
      svg.appendChild(tag);
    }}

    // Label acima das barras 2023-2025 (obrigatorio conforme briefing)
    if (yr === 2023 || yr === 2024 || yr === 2025) {{
      var vlabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
      vlabel.setAttribute("x", x + barW/2);
      vlabel.setAttribute("y", y - 6);
      vlabel.setAttribute("text-anchor", "middle");
      vlabel.setAttribute("font-size", "12");
      vlabel.setAttribute("fill", "#0B9247");
      vlabel.setAttribute("font-weight", "700");
      vlabel.setAttribute("font-family", "Montserrat, sans-serif");
      vlabel.textContent = formatShort(data[i]);
      vlabel.setAttribute("opacity", "0");
      vlabel.dataset.anim = "1";
      svg.appendChild(vlabel);
    }}
  }}

  // Tooltip
  svg.addEventListener("mousemove", function(e) {{
    var target = e.target;
    if (target.classList && target.classList.contains("bar-rect")) {{
      var yr = target.dataset.year;
      var val = parseFloat(target.dataset.value);
      var suffix = (yr === "2026") ? " <em style='font-weight:400'>(1&ordm; tri)</em>" : "";
      tooltipEl.innerHTML = yr + ": <strong>" + formatNum(val) + "</strong>" + suffix;
      tooltipEl.classList.add("visible");
      tooltipEl.style.left = (e.clientX + 12) + "px";
      tooltipEl.style.top  = (e.clientY - 36) + "px";
    }}
  }});
  svg.addEventListener("mouseleave", function() {{
    tooltipEl.classList.remove("visible");
  }});

  // Animate
  requestAnimationFrame(function() {{
    setTimeout(function() {{
      barsInfo.forEach(function(b, idx) {{
        setTimeout(function() {{
          b.el.style.transition = "y 0.5s ease, height 0.5s ease";
          b.el.setAttribute("y", b.targetY);
          b.el.setAttribute("height", b.targetH);
        }}, idx * 25);
      }});
      setTimeout(function() {{
        var labels = svg.querySelectorAll('text[data-anim]');
        labels.forEach(function(l) {{
          l.style.transition = "opacity 0.5s ease";
          l.setAttribute("opacity", "1");
        }});
      }}, 25*barsInfo.length + 300);
    }}, 80);
  }});
}})();
</script>

<script>
function notifyHeight() {{
  var h = document.documentElement.scrollHeight;
  window.parent.postMessage({{ sentinel: 'agencia-sp', type: 'resize', height: h }}, '*');
}}
window.addEventListener('load', notifyHeight);
window.addEventListener('resize', notifyHeight);
setTimeout(notifyHeight, 2500);
</script>

</body>
</html>
"""

(BASE / "hectares_regularizados_itesp.html").write_text(HTML1, encoding="utf-8")
print("OK - hectares_regularizados_itesp.html")


# ======================================================
# INFOGRAFICO 2 - TITULOS RURAIS POR GESTAO
# ======================================================

# Totais por gestao (linha "rurais" agrupada)
GESTOES = [
    {"nome": "Geraldo Alckmin",          "periodo": "2011-2014",    "val": 102,  "atual": False},
    {"nome": "Alckmin / Marcio Franca",  "periodo": "2015-2018",    "val": 140,  "atual": False},
    {"nome": "Joao Doria / Rodrigo Garcia","periodo":"2019-2022",  "val": 89,   "atual": False},
    {"nome": "Tarcisio de Freitas",      "periodo": "2023-1T2026",  "val": 5375, "atual": True},
]

import json
GESTOES_JSON = json.dumps(GESTOES, ensure_ascii=True)

HTML2 = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Titulos rurais saltam de 331 para 5,3 mil em uma gestao</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ height: auto; overflow: hidden; }}
    body {{
      font-family: 'Montserrat', sans-serif;
      background: #FFFFFF;
      color: #1D1D1B;
      display: flex;
      justify-content: center;
      padding: 20px 20px 10px;
    }}
    .infographic {{ width: 100%; max-width: 960px; }}

    .main-title {{
      font-size: 24px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 6px;
      color: #1D1D1B;
    }}
    .main-title .destaque {{ color: #0B9247; }}

    .main-subtitle {{
      font-size: 15px;
      font-weight: 400;
      color: #444;
      line-height: 1.4;
      margin-bottom: 20px;
    }}

    .chart-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .chart-badge {{
      display: inline-block;
      font-size: 13px;
      font-weight: 700;
      color: #0B9247;
      background: #E8F5E9;
      border-radius: 4px;
      padding: 2px 10px;
    }}

    .bars-list {{ display: flex; flex-direction: column; gap: 18px; margin-bottom: 20px; }}
    .bar-row {{ display: grid; grid-template-columns: 230px 1fr; align-items: center; gap: 16px; }}
    @media (max-width: 600px) {{
      .bar-row {{ grid-template-columns: 1fr; gap: 4px; }}
      .bar-label {{ text-align: left !important; }}
    }}

    .bar-label {{
      text-align: right;
      font-size: 13px;
      line-height: 1.3;
      color: #1D1D1B;
    }}
    .bar-label .nome {{ font-weight: 700; display: block; }}
    .bar-label .periodo {{ color: #777; font-size: 11px; }}
    .bar-row.atual .bar-label .nome {{ color: #0B9247; }}

    .bar-track {{
      position: relative;
      height: 36px;
      background: #F5F5F5;
      border-radius: 4px;
      overflow: visible;
    }}
    .bar-fill {{
      position: absolute;
      left: 0; top: 0; bottom: 0;
      background: #C0C0C0;
      width: 0;
      border-radius: 4px;
      transition: width 0.9s cubic-bezier(.22,1,.36,1);
    }}
    .bar-row.atual .bar-fill {{ background: #0B9247; }}

    .bar-value {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      font-size: 14px;
      font-weight: 700;
      color: #1D1D1B;
      padding-left: 10px;
      white-space: nowrap;
    }}
    .bar-row.atual .bar-value {{ color: #0B9247; font-size: 18px; }}
    .bar-row.atual .bar-value small {{
      font-size: 11px;
      font-weight: 600;
      color: #0B9247;
      background: #E8F5E9;
      padding: 2px 8px;
      border-radius: 3px;
      margin-left: 8px;
      vertical-align: middle;
    }}

    .callout {{
      background: #F9FBF9;
      border-left: 4px solid #0B9247;
      padding: 12px 16px;
      border-radius: 4px;
      font-size: 13px;
      line-height: 1.5;
      color: #1D1D1B;
      margin-bottom: 12px;
    }}
    .callout strong {{ color: #0B9247; }}

    .chart-source {{ font-size: 12px; color: #808080; margin-top: 12px; line-height: 1.4; }}

    .logo-container {{ text-align: center; margin-top: 16px; }}
    .logo-container img {{ height: 32px; }}

    @media (max-width: 600px) {{
      .main-title {{ font-size: 20px; }}
      .main-subtitle {{ font-size: 13px; }}
    }}
  </style>
</head>
<body>

<div class="infographic">
  <div class="main-title">
    Titulos rurais saltam de 331 para <span class="destaque">5,3 mil</span> em uma gestao
  </div>
  <div class="main-subtitle">
    Tres gestoes anteriores entregaram 331 documentos rurais entre 2011 e 2022; a atual soma 5.375 em pouco mais de tres anos
  </div>

  <div class="chart-header">
    <span class="chart-badge">Titulos rurais entregues pelo Itesp, por gestao</span>
  </div>

  <div class="bars-list" id="bars-list"></div>

  <div class="callout">
    A gestao atual entregou <strong>cerca de 38 vezes</strong> o total de titulos rurais da melhor gestao anterior (140), e <strong>16 vezes</strong> a soma das tres gestoes que a precederam (331 titulos entre 2011 e 2022).
  </div>

  <div class="chart-source">
    Fonte: Fundacao Itesp / Secretaria de Agricultura e Abastecimento do Estado de Sao Paulo.<br>
    Gestao Tarcisio inclui dados ate o 1&ordm; trimestre de 2026.
  </div>

  <div class="logo-container">
    <img src="{LOGO}" alt="Agencia SP">
  </div>
</div>

<script>
var gestoes = {GESTOES_JSON};
var maxVal = Math.max.apply(null, gestoes.map(function(g) {{ return g.val; }}));

function formatNum(n) {{
  return n.toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".");
}}

(function buildBars() {{
  var list = document.getElementById("bars-list");
  gestoes.forEach(function(g, i) {{
    var row = document.createElement("div");
    row.className = "bar-row" + (g.atual ? " atual" : "");

    var labelDiv = document.createElement("div");
    labelDiv.className = "bar-label";
    labelDiv.innerHTML = '<span class="nome">' + g.nome + '</span><span class="periodo">' + g.periodo + '</span>';
    row.appendChild(labelDiv);

    var track = document.createElement("div");
    track.className = "bar-track";

    var fill = document.createElement("div");
    fill.className = "bar-fill";
    // width real proporcional (escala linear - mostra o salto)
    var pct = (g.val / maxVal) * 100;
    fill.dataset.target = pct.toFixed(2);
    track.appendChild(fill);

    var val = document.createElement("div");
    val.className = "bar-value";
    val.style.left = pct.toFixed(2) + "%";
    var suffix = g.atual ? ' <small>+5.044 vs gestao anterior</small>' : '';
    val.innerHTML = formatNum(g.val) + suffix;
    track.appendChild(val);

    row.appendChild(track);
    list.appendChild(row);
  }});

  // anima apos insert
  requestAnimationFrame(function() {{
    setTimeout(function() {{
      document.querySelectorAll('.bar-fill').forEach(function(f, i) {{
        setTimeout(function() {{
          f.style.width = f.dataset.target + "%";
        }}, i * 120);
      }});
    }}, 100);
  }});
}})();
</script>

<script>
function notifyHeight() {{
  var h = document.documentElement.scrollHeight;
  window.parent.postMessage({{ sentinel: 'agencia-sp', type: 'resize', height: h }}, '*');
}}
window.addEventListener('load', notifyHeight);
window.addEventListener('resize', notifyHeight);
setTimeout(notifyHeight, 2500);
</script>

</body>
</html>
"""

(BASE / "titulos_rurais_por_gestao_itesp.html").write_text(HTML2, encoding="utf-8")
print("OK - titulos_rurais_por_gestao_itesp.html")
