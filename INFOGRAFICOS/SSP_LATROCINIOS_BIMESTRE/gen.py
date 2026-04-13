import json, csv

years = list(range(2001, 2027))
data = [75, 95, 88, 60, 62, 49, 41, 39, 59, 43, 47, 49, 67, 68, 53, 51, 73, 45, 29, 40, 28, 30, 23, 33, 28, 12]

# Save CSV
with open(r'C:\Users\gabriel.croquer\Desktop\agencia-sp-templates\INFOGRAFICOS\SSP_LATROCINIOS_BIMESTRE\latrocinios_bimestre.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Ano', 'Latrocinio'])
    for y, v in zip(years, data):
        w.writerow([y, v])

with open(r'C:\Users\gabriel.croquer\Desktop\agencia-sp-templates\INFOGRAFICOS\SSP_ROUBOS_BIMESTRE\logo_base64.txt', 'r') as f:
    logo_src = f.read().strip()

html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Latrocinios em SP - 1o bimestre 2026</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { height: auto; overflow: hidden; }
    body {
      font-family: 'Montserrat', sans-serif;
      background: #FFFFFF;
      color: #1D1D1B;
      display: flex;
      justify-content: center;
      padding: 20px 20px 10px;
    }
    .infographic { width: 100%; max-width: 960px; }

    .main-title {
      font-size: 26px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 6px;
      color: #1D1D1B;
    }
    .main-title .destaque { color: #0B9247; }

    .main-subtitle {
      font-size: 15px;
      font-weight: 400;
      color: #666;
      line-height: 1.4;
      margin-bottom: 20px;
    }

    .legend {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 16px;
      font-size: 12px;
      color: #666;
    }
    .legend-item { display: flex; align-items: center; gap: 5px; }
    .legend-swatch { width: 12px; height: 12px; border-radius: 2px; }

    .chart-area { position: relative; width: 100%; margin-bottom: 12px; }
    .chart-area svg { width: 100%; height: auto; display: block; }

    .bar-rect { cursor: pointer; transition: opacity 0.2s ease; }
    .bar-rect:hover { opacity: 0.75; }

    .tooltip {
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
    }
    .tooltip.visible { opacity: 1; }

    .chart-source { font-size: 12px; color: #808080; margin-top: 8px; }
    .logo-container { text-align: center; margin-top: 16px; }
    .logo-container img { height: 32px; }

    @media (max-width: 600px) {
      .main-title { font-size: 21px; }
      .main-subtitle { font-size: 13px; }
    }
  </style>
</head>
<body>

<div class="infographic">
  <div class="main-title">
    Latrocinios <span class="destaque">caem 57%</span> em SP no 1&ordm; bimestre de 2026
  </div>
  <div class="main-subtitle">
    Estado registrou 12 ocorrencias em janeiro e fevereiro, menor patamar da serie historica iniciada em 2001
  </div>

  <div class="legend">
    <div class="legend-item">
      <div class="legend-swatch" style="background:#C0C0C0;"></div>
      <span>2001&ndash;2025</span>
    </div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#0B9247;"></div>
      <span>2026 (minimo historico)</span>
    </div>
  </div>

  <div class="chart-area" id="chartArea"></div>

  <div class="chart-source">Fonte: SSP-SP &mdash; Secretaria da Seguranca Publica do Estado de Sao Paulo</div>

  <div class="logo-container">
    <img src="''' + logo_src + '''" alt="Agencia SP">
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
var data = ''' + json.dumps(data) + ''';
var years = ''' + json.dumps(years) + ''';
var GREEN = "#0B9247";
var GRAY = "#C0C0C0";
var tooltipEl = document.getElementById("tooltip");

function formatNum(n) {
  return n.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".");
}

(function() {
  var n = data.length;
  var maxVal = Math.max.apply(null, data);
  var mag = Math.pow(10, Math.floor(Math.log10(maxVal || 1)));
  var yMax = Math.ceil((maxVal * 1.05) / mag) * mag;

  var svgW = 960, svgH = 340;
  var ml = 40, mr = 12, mt = 12, mb = 32;
  var plotW = svgW - ml - mr;
  var plotH = svgH - mt - mb;

  var barW = Math.floor(plotW / n * 0.72);
  var gap = (plotW - barW * n) / n;

  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 " + svgW + " " + svgH);
  svg.setAttribute("preserveAspectRatio", "xMidYMid meet");

  // Y gridlines
  var nTicks = 5;
  for (var t = 0; t <= nTicks; t++) {
    var val = (yMax / nTicks) * t;
    var yPos = mt + plotH - (val / yMax) * plotH;

    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", ml); line.setAttribute("x2", svgW - mr);
    line.setAttribute("y1", yPos); line.setAttribute("y2", yPos);
    line.setAttribute("stroke", "#E5E5E5"); line.setAttribute("stroke-width", "1");
    svg.appendChild(line);

    var label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", ml - 6); label.setAttribute("y", yPos + 4);
    label.setAttribute("text-anchor", "end");
    label.setAttribute("font-size", "11"); label.setAttribute("fill", "#999");
    label.setAttribute("font-family", "Montserrat, sans-serif");
    label.textContent = val.toFixed(0);
    svg.appendChild(label);
  }

  // Bars
  var barsInfo = [];
  for (var i = 0; i < n; i++) {
    var x = ml + gap / 2 + i * (barW + gap);
    var h = data[i] > 0 ? (data[i] / yMax) * plotH : 0;
    var y = mt + plotH - h;
    var isLast = (i === n - 1);

    var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("class", "bar-rect");
    rect.setAttribute("x", x); rect.setAttribute("y", mt + plotH);
    rect.setAttribute("width", barW); rect.setAttribute("height", 0);
    rect.setAttribute("rx", "2"); rect.setAttribute("fill", isLast ? GREEN : GRAY);
    rect.dataset.year = years[i]; rect.dataset.value = data[i];
    svg.appendChild(rect);
    barsInfo.push({ el: rect, targetY: y, targetH: h });

    // X labels: first, last, every 5th, skip n-2
    if ((i === 0 || i === n - 1 || years[i] % 5 === 0) && i !== n - 2) {
      var xLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
      xLabel.setAttribute("x", x + barW / 2); xLabel.setAttribute("y", mt + plotH + 18);
      xLabel.setAttribute("text-anchor", "middle");
      xLabel.setAttribute("font-size", "11");
      xLabel.setAttribute("fill", isLast ? "#1D1D1B" : "#999");
      xLabel.setAttribute("font-weight", isLast ? "700" : "400");
      xLabel.setAttribute("font-family", "Montserrat, sans-serif");
      xLabel.textContent = String(years[i]);
      svg.appendChild(xLabel);
    }
  }

  // Tooltip
  svg.addEventListener("mousemove", function(e) {
    var t = e.target;
    if (t.classList.contains("bar-rect")) {
      tooltipEl.innerHTML = t.dataset.year + ": <strong>" + formatNum(parseInt(t.dataset.value)) + "</strong> ocorrencias";
      tooltipEl.classList.add("visible");
      tooltipEl.style.left = (e.clientX + 12) + "px";
      tooltipEl.style.top = (e.clientY - 36) + "px";
    }
  });
  svg.addEventListener("mouseleave", function() { tooltipEl.classList.remove("visible"); });

  document.getElementById("chartArea").appendChild(svg);

  // Animate
  requestAnimationFrame(function() {
    setTimeout(function() {
      barsInfo.forEach(function(b, idx) {
        setTimeout(function() {
          b.el.style.transition = "y 0.5s ease, height 0.5s ease";
          b.el.setAttribute("y", b.targetY);
          b.el.setAttribute("height", b.targetH);
        }, idx * 20);
      });
    }, 100);
  });
})();
</script>

<script>
function notifyHeight() {
  var h = document.documentElement.scrollHeight;
  window.parent.postMessage({ sentinel: 'agencia-sp', type: 'resize', height: h }, '*');
}
window.addEventListener('load', notifyHeight);
window.addEventListener('resize', notifyHeight);
setTimeout(notifyHeight, 2500);
</script>

</body>
</html>'''

outpath = r'C:\Users\gabriel.croquer\Desktop\agencia-sp-templates\INFOGRAFICOS\SSP_LATROCINIOS_BIMESTRE\latrocinios_bimestre_2026.html'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written: {len(html)} chars -> {outpath}")
