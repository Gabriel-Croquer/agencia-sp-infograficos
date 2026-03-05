"""
Publicar Infograficos - Agencia SP

Script para gerar codigos de embed e preparar infograficos para publicacao.

Uso:
    python publicar.py output/meu-infografico.html
    python publicar.py output/meu-infografico.html --base-url https://agenciasp.github.io/infograficos

Gera:
    - Codigo iframe para WordPress
    - Codigo embed responsivo
    - Preview das dimensoes
"""

import sys
import os
import re

def get_title_from_html(filepath):
    """Extrai o titulo do infografico do HTML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tenta extrair do CONFIG
    match = re.search(r"titulo:\s*['\"](.+?)['\"]", content)
    if match:
        # Remove HTML tags
        title = re.sub(r'<[^>]+>', '', match.group(1))
        return title.strip()

    # Tenta extrair do <title>
    match = re.search(r'<title>(.+?)</title>', content)
    if match:
        return match.group(1).strip()

    return os.path.basename(filepath).replace('.html', '')


def generate_embed(filepath, base_url=None):
    """Gera codigos de embed para um infografico."""
    filename = os.path.basename(filepath)
    title = get_title_from_html(filepath)
    filesize = os.path.getsize(filepath) / 1024  # KB

    if base_url:
        url = f"{base_url.rstrip('/')}/{filename}"
    else:
        url = f"URL_DO_SEU_SERVIDOR/{filename}"

    print(f"\n{'='*60}")
    print(f"  PUBLICAR: {title}")
    print(f"{'='*60}")
    print(f"\n  Arquivo: {filepath}")
    print(f"  Tamanho: {filesize:.1f} KB")

    print(f"\n{'─'*60}")
    print(f"  EMBED PARA WORDPRESS (HTML Personalizado)")
    print(f"{'─'*60}")
    print(f"""
<iframe
  src="{url}"
  width="100%"
  height="600"
  frameborder="0"
  style="border: none; max-width: 900px; margin: 0 auto; display: block;"
  title="{title}"
  loading="lazy">
</iframe>
""")

    print(f"{'─'*60}")
    print(f"  EMBED RESPONSIVO (com aspect ratio)")
    print(f"{'─'*60}")
    print(f"""
<div style="position: relative; padding-bottom: 75%; height: 0; overflow: hidden; max-width: 900px; margin: 0 auto;">
  <iframe
    src="{url}"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
    title="{title}"
    loading="lazy">
  </iframe>
</div>
""")

    print(f"{'─'*60}")
    print(f"  PROXIMO PASSO")
    print(f"{'─'*60}")

    if base_url:
        print(f"\n  1. Faca git add + commit + push do arquivo")
        print(f"  2. Acesse: {url}")
        print(f"  3. Cole o embed no WordPress (bloco HTML Personalizado)")
    else:
        print(f"\n  1. Faca upload de '{filename}' para seu servidor web")
        print(f"  2. Substitua 'URL_DO_SEU_SERVIDOR' pela URL real")
        print(f"  3. Cole o embed no WordPress (bloco HTML Personalizado)")

    print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python publicar.py <arquivo.html> [--base-url URL]")
        print("Exemplo: python publicar.py output/roubos-sp-2026.html --base-url https://agenciasp.github.io/infograficos")
        sys.exit(1)

    filepath = sys.argv[1]
    base_url = None

    if '--base-url' in sys.argv:
        idx = sys.argv.index('--base-url')
        if idx + 1 < len(sys.argv):
            base_url = sys.argv[idx + 1]

    if not os.path.exists(filepath):
        print(f"Erro: Arquivo '{filepath}' nao encontrado.")
        sys.exit(1)

    generate_embed(filepath, base_url)
