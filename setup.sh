#!/bin/bash
# ============================================
# Setup do projeto Agência SP Templates
# Execute: bash setup.sh
# ============================================

echo "🏗️  Criando estrutura do projeto Agência SP Templates..."

# Criar pastas de input
mkdir -p inputs/manual-iv
mkdir -p inputs/infograficos-existentes
mkdir -p inputs/dados-exemplo

# Criar pasta de output
mkdir -p templates

echo ""
echo "✅ Estrutura criada com sucesso!"
echo ""
echo "📁 Próximos passos:"
echo ""
echo "  1. Coloque o PDF do manual de identidade visual em:"
echo "     inputs/manual-iv/"
echo ""
echo "  2. Coloque screenshots dos infográficos já publicados em:"
echo "     inputs/infograficos-existentes/"
echo ""
echo "  3. Coloque planilhas CSV/XLSX de exemplo em:"
echo "     inputs/dados-exemplo/"
echo ""
echo "  4. Abra o Claude Code e cole o prompt do README.md"
echo ""
echo "🚀 Bom trabalho!"
