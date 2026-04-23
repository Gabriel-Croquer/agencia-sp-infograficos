# -*- coding: utf-8 -*-
# Gera os dois HTMLs do infografico Itesp (barras verticais ano a ano)
from pathlib import Path

BASE = Path(__file__).parent
LOGO = (BASE / "logo_base64.txt").read_text().strip()


def render(out_path, *, page_title, main_title_html, subtitle, badge,
           anos, vals, y_max, y_tick_format, value_format, unit_singular,
           unit_plural, tooltip_suffix_2026, source_html, label_highlight_years,
           value_label_format):
    """Gera um HTML de barras verticais ano a ano."""
    import json
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
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
    {main_title_html}
  </div>
  <div class="main-subtitle">
    {subtitle}
  </div>

  <div class="legend">
    <div class="legend-item">
      <div class="legend-swatch" style="background:#C0C0C0;"></div>
      <span>2011&ndash;2022</span>
    </div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#0B9247;"></div>
      <span>2023&ndash;2025 (gest&atilde;o atual)</span>
    </div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:repeating-linear-gradient(45deg,#0B9247 0 4px,#7FCB9F 4px 8px);"></div>
      <span>2026 (1&ordm; trimestre)</span>
    </div>
  </div>

  <div class="chart-container">
    <div class="chart-header">
      <span class="chart-badge">{badge}</span>
    </div>
    <svg id="chart" viewBox="0 0 900 360" preserveAspectRatio="xMidYMid meet"></svg>
  </div>

  <div class="chart-source">
    {source_html}
  </div>

  <div class="logo-container">
    <img src="{LOGO}" alt="Ag&ecirc;ncia SP">
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
var years = {json.dumps(anos)};
var data  = {json.dumps(vals)};
var Y_MAX = {y_max};
var HIGHLIGHT_LABEL_YEARS = {json.dumps(label_highlight_years)};

var GREEN = "#0B9247";
var GRAY  = "#C0C0C0";
var HATCH_ID = "hatch-green";
var tooltipEl = document.getElementById("tooltip");

function formatBR(n, decimals) {{
  var fixed = Number(n).toFixed(decimals || 0);
  var parts = fixed.split(".");
  parts[0] = parts[0].replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".");
  return parts.join(",");
}}

function formatTooltip(n) {{
  {value_format}
}}

function formatYTick(v) {{
  {y_tick_format}
}}

function formatValueLabel(n) {{
  {value_label_format}
}}

(function buildChart() {{
  var svg = document.getElementById("chart");
  var n = data.length;

  var svgW = 900, svgH = 360;
  var ml = 70, mr = 20, mt = 40, mb = 40;
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
  patBg.setAttribute("width", "8"); patBg.setAttribute("height", "8"); patBg.setAttribute("fill", "#0B9247");
  pat.appendChild(patBg);
  var patLine = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  patLine.setAttribute("width", "4"); patLine.setAttribute("height", "8"); patLine.setAttribute("fill", "#7FCB9F");
  pat.appendChild(patLine);
  defs.appendChild(pat);
  svg.appendChild(defs);

  // Y axis
  var nTicks = 5;
  for (var t = 0; t <= nTicks; t++) {{
    var val = (Y_MAX / nTicks) * t;
    var yPos = mt + plotH - (val / Y_MAX) * plotH;

    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", ml); line.setAttribute("x2", svgW - mr);
    line.setAttribute("y1", yPos); line.setAttribute("y2", yPos);
    line.setAttribute("stroke", "#E5E5E5"); line.setAttribute("stroke-width", "1");
    svg.appendChild(line);

    var label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", ml - 8); label.setAttribute("y", yPos + 4);
    label.setAttribute("text-anchor", "end"); label.setAttribute("font-size", "11");
    label.setAttribute("fill", "#999"); label.setAttribute("font-family", "Montserrat, sans-serif");
    label.textContent = formatYTick(val);
    svg.appendChild(label);
  }}

  // Bars
  var barsInfo = [];
  for (var i = 0; i < n; i++) {{
    var x = ml + gap / 2 + i * (barW + gap);
    var h = data[i] > 0 ? (data[i] / Y_MAX) * plotH : 0;
    var y = mt + plotH - h;
    var yr = years[i];

    var fill = GRAY;
    if (yr === 2023 || yr === 2024 || yr === 2025) fill = GREEN;
    if (yr === 2026) fill = "url(#" + HATCH_ID + ")";

    var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("class", "bar-rect");
    rect.setAttribute("x", x); rect.setAttribute("y", mt + plotH);
    rect.setAttribute("width", barW); rect.setAttribute("height", 0);
    rect.setAttribute("rx", "2"); rect.setAttribute("fill", fill);
    rect.dataset.year = yr; rect.dataset.value = data[i];
    svg.appendChild(rect);
    barsInfo.push({{ el: rect, targetY: y, targetH: h }});

    // X label - todos os anos
    var xLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    xLabel.setAttribute("x", x + barW/2); xLabel.setAttribute("y", mt + plotH + 18);
    xLabel.setAttribute("text-anchor", "middle"); xLabel.setAttribute("font-size", "10");
    xLabel.setAttribute("fill", (yr>=2023) ? "#1D1D1B" : "#777");
    xLabel.setAttribute("font-weight", (yr>=2023) ? "700" : "400");
    xLabel.setAttribute("font-family", "Montserrat, sans-serif");
    xLabel.textContent = String(yr);
    svg.appendChild(xLabel);

    // 2026 marker "(1T)"
    if (yr === 2026) {{
      var tag = document.createElementNS("http://www.w3.org/2000/svg", "text");
      tag.setAttribute("x", x + barW/2); tag.setAttribute("y", mt + plotH + 32);
      tag.setAttribute("text-anchor", "middle"); tag.setAttribute("font-size", "9");
      tag.setAttribute("fill", "#0B9247"); tag.setAttribute("font-weight", "700");
      tag.setAttribute("font-family", "Montserrat, sans-serif");
      tag.textContent = "(1T)";
      svg.appendChild(tag);
    }}

    // Label acima das barras destacadas
    if (HIGHLIGHT_LABEL_YEARS.indexOf(yr) !== -1) {{
      var vlabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
      vlabel.setAttribute("x", x + barW/2); vlabel.setAttribute("y", y - 6);
      vlabel.setAttribute("text-anchor", "middle"); vlabel.setAttribute("font-size", "12");
      vlabel.setAttribute("fill", "#0B9247"); vlabel.setAttribute("font-weight", "700");
      vlabel.setAttribute("font-family", "Montserrat, sans-serif");
      vlabel.textContent = formatValueLabel(data[i]);
      vlabel.setAttribute("opacity", "0"); vlabel.dataset.anim = "1";
      svg.appendChild(vlabel);
    }}
  }}

  // Tooltip
  svg.addEventListener("mousemove", function(e) {{
    var target = e.target;
    if (target.classList && target.classList.contains("bar-rect")) {{
      var yr = target.dataset.year;
      var val = parseFloat(target.dataset.value);
      var suffix = (yr === "2026") ? {json.dumps(tooltip_suffix_2026)} : "";
      tooltipEl.innerHTML = yr + ": <strong>" + formatTooltip(val) + "</strong>" + suffix;
      tooltipEl.classList.add("visible");
      tooltipEl.style.left = (e.clientX + 12) + "px";
      tooltipEl.style.top  = (e.clientY - 36) + "px";
    }}
  }});
  svg.addEventListener("mouseleave", function() {{ tooltipEl.classList.remove("visible"); }});

  // Animate
  requestAnimationFrame(function() {{
    setTimeout(function() {{
      barsInfo.forEach(function(b, idx) {{
        setTimeout(function() {{
          b.el.style.transition = "y 0.5s ease, height 0.5s ease";
          b.el.setAttribute("y", b.targetY); b.el.setAttribute("height", b.targetH);
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
    out_path.write_text(html, encoding="utf-8")
    print(f"OK - {out_path.name}")


# ======================================================
# INFOGRAFICO 1 - HECTARES POR ANO
# ======================================================

HECTARES_TOTAL = {
    2011: 412.7951, 2012: 889.2266, 2013: 421.9973, 2014: 108.477,
    2015: 2355.253, 2016: 5684.947, 2017: 1708.342, 2018: 559.4231,
    2019: 1479.639, 2020: 143.0386, 2021: 428.509,  2022: 2152.702,
    2023: 58354.43, 2024: 80913.71, 2025: 95140.9,  2026: 3316.971,
}

render(
    out_path = BASE / "hectares_regularizados_itesp.html",
    page_title = "Regularização de terras dispara em SP a partir de 2023",
    main_title_html = 'Regulariza&ccedil;&atilde;o de terras <span class="destaque">dispara em SP</span> a partir de 2023',
    subtitle = 'Gest&atilde;o atual titulou mais hectares em 2025 (95,1 mil) do que em todo o per&iacute;odo de 2011 a 2022 somado (16,3 mil)',
    badge = "Hectares regularizados por ano",
    anos = list(HECTARES_TOTAL.keys()),
    vals = list(HECTARES_TOTAL.values()),
    y_max = 100000,
    y_tick_format = 'return v === 0 ? "0" : (v/1000).toFixed(0) + " mil ha";',
    value_format = '''
  if (n >= 1000) return formatBR(n/1000, 1) + " mil ha";
  return formatBR(n, 0) + " ha";
''',
    value_label_format = '''
  if (n >= 1000) return formatBR(n/1000, n >= 10000 ? 0 : 1) + " mil";
  return formatBR(n, 0);
''',
    unit_singular = "hectare",
    unit_plural = "hectares",
    tooltip_suffix_2026 = " <em style='font-weight:400'>(1º tri)</em>",
    source_html = 'Fonte: Funda&ccedil;&atilde;o Itesp / Secretaria de Agricultura e Abastecimento do Estado de S&atilde;o Paulo.<br>Dados de 2026 correspondem apenas ao 1&ordm; trimestre.',
    label_highlight_years = [2023, 2024, 2025],
)


# ======================================================
# INFOGRAFICO 2 - TITULOS RURAIS POR ANO
# ======================================================

TITULOS_RURAIS = {
    2011: 27, 2012: 42, 2013: 32, 2014: 1,
    2015: 16, 2016: 15, 2017: 105, 2018: 4,
    2019: 15, 2020: 9, 2021: 32, 2022: 33,
    2023: 1973, 2024: 1534, 2025: 1612, 2026: 256,
}

render(
    out_path = BASE / "titulos_rurais_por_ano_itesp.html",
    page_title = "Títulos rurais disparam em SP a partir de 2023",
    main_title_html = 'T&iacute;tulos rurais <span class="destaque">disparam em SP</span> a partir de 2023',
    subtitle = 'S&oacute; em 2023, o Itesp entregou 1.973 t&iacute;tulos rurais&nbsp;&mdash;&nbsp;quase seis vezes o total somado de 2011 a 2022 (331 documentos)',
    badge = "Títulos rurais entregues por ano",
    anos = list(TITULOS_RURAIS.keys()),
    vals = list(TITULOS_RURAIS.values()),
    y_max = 2000,
    y_tick_format = 'return v === 0 ? "0" : formatBR(v, 0);',
    value_format = '''
  var n0 = Math.round(n);
  return formatBR(n0, 0) + (n0 === 1 ? " título" : " títulos");
''',
    value_label_format = '''
  return formatBR(Math.round(n), 0);
''',
    unit_singular = "título",
    unit_plural = "títulos",
    tooltip_suffix_2026 = " <em style='font-weight:400'>(1º tri)</em>",
    source_html = 'Fonte: Funda&ccedil;&atilde;o Itesp / Secretaria de Agricultura e Abastecimento do Estado de S&atilde;o Paulo.<br>Dados de 2026 correspondem apenas ao 1&ordm; trimestre.',
    label_highlight_years = [2023, 2024, 2025],
)
