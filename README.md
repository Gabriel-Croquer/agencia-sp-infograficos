# Agência SP — Fábrica de Templates Interativos

Sistema de agentes para criação automatizada de infográficos interativos
com identidade visual da Agência SP (Governo do Estado de São Paulo).

## Estrutura do Projeto

```
agencia-sp-templates/
├── .claude/
│   └── agents/
│       ├── analista-repertorio.md    → Agente 1: Analisa infográficos existentes e extrai IV
│       ├── estrategista-formatos.md  → Agente 2: Define quais templates criar
│       ├── dev-templates.md          → Agente 3: Cria os HTMLs interativos
│       └── qa-templates.md           → Agente 4: Revisa e corrige tudo
├── inputs/
│   ├── manual-iv/                    → Coloque aqui o PDF do manual de identidade visual
│   ├── infograficos-existentes/      → Coloque aqui imagens dos infográficos já publicados
│   └── dados-exemplo/                → Coloque aqui planilhas CSV/Excel de exemplo
├── templates/                        → Os templates HTML prontos aparecerão aqui
│   └── catalogo.json                 → Catálogo de templates gerado automaticamente
├── analise-repertorio.json           → Relatório do Agente 1 (gerado automaticamente)
├── analise-repertorio-resumo.md      → Resumo legível do Agente 1
├── plano-templates.json              → Plano do Agente 2 (gerado automaticamente)
├── plano-templates-resumo.md         → Resumo legível do Agente 2
├── qa-report.json                    → Relatório de QA do Agente 4
├── COMO-USAR.md                      → Guia de uso gerado pelo Agente 4
└── README.md                         → Este arquivo
```

## Setup (faça apenas uma vez)

### 1. Crie a pasta do projeto

```bash
mkdir agencia-sp-templates
cd agencia-sp-templates
```

### 2. Copie a pasta .claude/agents/

Copie toda a pasta `.claude/` deste repositório para a raiz do seu projeto.

### 3. Crie as pastas de input

```bash
mkdir -p inputs/manual-iv
mkdir -p inputs/infograficos-existentes
mkdir -p inputs/dados-exemplo
mkdir -p templates
```

### 4. Coloque seus arquivos

- **`inputs/manual-iv/`**: O PDF do manual de identidade visual do Governo SP
- **`inputs/infograficos-existentes/`**: Screenshots ou exports dos infográficos que a Agência SP já publicou (PNG, JPG)
- **`inputs/dados-exemplo/`**: Planilhas CSV ou XLSX com dados reais (para usar como exemplo nos templates)

### 5. Abra o Claude Code no VS Code

```bash
cd agencia-sp-templates
code .
```

Abra o terminal integrado e inicie o Claude Code.

## Como Rodar

### Opção A: Execução encadeada (recomendada para a primeira vez)

Cole este prompt no Claude Code:

```
Vou criar templates de infográficos interativos para a Agência SP.

Na pasta inputs/ há:
- Manual de identidade visual em inputs/manual-iv/
- Imagens de infográficos já publicados em inputs/infograficos-existentes/
- Dados de exemplo em inputs/dados-exemplo/

Execute os agentes nesta ordem:

1. Use o agente analista-repertorio para analisar todos os arquivos em inputs/ e gerar o analise-repertorio.json e analise-repertorio-resumo.md

2. Depois, use o agente estrategista-formatos para ler o relatório do analista e gerar o plano-templates.json e plano-templates-resumo.md

3. Depois, use o agente dev-templates para criar cada template HTML na pasta templates/, seguindo o plano na ordem de prioridade

4. Por fim, use o agente qa-templates para revisar todos os templates, corrigir problemas e gerar o qa-report.json e COMO-USAR.md

Comece pelo agente 1.
```

### Opção B: Execução agente por agente (mais controle)

Rode um agente de cada vez:

```
Use o agente analista-repertorio para analisar os arquivos em inputs/ e gerar o relatório.
```

Revise o output. Depois:

```
Use o agente estrategista-formatos para criar o plano de templates.
```

Revise o plano. Depois:

```
Use o agente dev-templates para criar os templates HTML do plano.
```

E por fim:

```
Use o agente qa-templates para revisar tudo.
```

### Opção C: Criar um template específico avulso

Se você precisa de um template novo que não está no plano:

```
Use o agente dev-templates para criar um template de [TIPO] com estes dados:
[COLE SEUS DADOS AQUI]

O título é "[SEU TÍTULO]" e a fonte é "Fonte: [SUA FONTE]".
Use a identidade visual definida em analise-repertorio.json.
```

## Após a criação

Os templates prontos estarão em `templates/`. Para usar:

1. Copie o arquivo .html desejado
2. Edite o bloco CONFIG no topo (título, subtítulo, dados)
3. Abra no navegador para verificar
4. Faça upload no servidor WordPress
5. Embede com iframe ou bloco HTML

## Manutenção

Para adicionar novos tipos de template no futuro:
1. Atualize `plano-templates.json` com a nova spec
2. Rode o agente `dev-templates` pedindo para criar o novo template
3. Rode o agente `qa-templates` para revisar

Para atualizar a identidade visual (ex: mudança de governo):
1. Substitua o PDF em `inputs/manual-iv/`
2. Rode o `analista-repertorio` novamente
3. Rode o `qa-templates` para atualizar as cores em todos os templates existentes
