# Instrucoes Gerais


## Documentacao de Projetos


Para cada projeto, escreva um arquivo `FOR[seunome].md` detalhado que explique todo o projeto em linguagem simples.


### O que incluir
- **Arquitetura Tecnica**: Explique a estrutura do codigo-fonte e como as diversas partes estao conectadas.
- **Tecnologias Utilizadas**: Liste as tecnologias e por que tomamos essas decisoes tecnicas.
- **Licoes Aprendidas**: Bugs encontrados e como corrigimos, possiveis problemas e como evita-los, novas tecnologias, melhores praticas.


### Tom e Estilo
A leitura deve ser envolvente; evite que pareca um documento tecnico tedioso. Quando apropriado, utilize analogias e anedotas para torna-lo mais compreensivel e memoravel.


## Context7 MCP


Sempre use o Context7 MCP quando precisar de documentacao de biblioteca/API, geracao de codigo, instalacao ou etapas de configuracao, sem eu ter que pedir explicitamente.


---


# Workflow de Sprint: Spec-Driven Development (SDD)


**QUANDO ATIVAR:** Sempre que o usuario disser "sprint", "nova sprint", "preciso implementar uma feature", ou qualquer variacao que indique uma rodada de mudancas significativas no codigo.


**PRINCIPIO CENTRAL:** A qualidade do input determina a qualidade do output. Cada etapa produz um artefato que alimenta a proxima. Contexto limpo entre etapas = implementacao precisa.


## Fluxo Obrigatorio (3 Etapas)


```
PESQUISA → PRD.md → /clear → SPEC → Spec.md → /clear → IMPLEMENTACAO
```


### ETAPA 1: PESQUISA (Research)


**Objetivo:** Coletar todas as informacoes necessarias antes de planejar.


**O que fazer:**
1. Perguntar ao usuario: "Qual e a feature/mudanca que voce quer implementar?"
2. Explorar o codebase para identificar:
   - Arquivos que serao afetados
   - Padroes de implementacao similares que ja existem no codigo
   - Funcoes e dependencias relevantes
3. Se necessario, buscar documentacao de tecnologias envolvidas (APIs, bibliotecas)
4. Coletar code snippets que sirvam como referencia


**Output obrigatorio:** Criar o arquivo `docs/PRD.md` com:
```markdown
# PRD: [Nome da Feature]


## Objetivo
[O que queremos alcançar]


## Contexto do Codebase
[Arquivos relevantes, funcoes existentes, padroes encontrados]


## Referencia Tecnica
[Snippets, documentacao, exemplos de implementacao similar]


## Decisoes de Design
[Escolhas tecnicas e por que]
```


**Acao final:** Pedir ao usuario para usar `/clear` antes de seguir para a ETAPA 2.


---


### ETAPA 2: SPEC (Especificacao Tatica)


**Objetivo:** Transformar a pesquisa em um plano de implementacao preciso, arquivo por arquivo.


**O que fazer:**
1. Ler o `docs/PRD.md` criado na etapa anterior
2. Criar especificacao detalhada listando CADA arquivo que sera modificado/criado
3. Para cada arquivo, descrever EXATAMENTE o que fazer
4. Incluir code snippets prontos quando possivel
5. Definir ordem de implementacao


**Output obrigatorio:** Criar o arquivo `docs/Spec.md` com:
```markdown
# Spec: [Nome da Feature]


## Arquivos a Modificar


### 1. `Codigo.js`
- **Linha ~XXX**: Adicionar funcao `nomeFuncao()`
- **O que faz**: [descricao]
- **Snippet:**
  ```javascript
  function nomeFuncao() { ... }
  ```


### 2. `HubSidebar.html`
- **Secao CSS**: Adicionar estilos para `.nova-classe`
- **Secao HTML**: Novo container `#novoContainer`
- **Secao JS**: Nova funcao `novaFuncao()`


## Ordem de Implementacao
1. Backend primeiro (Codigo.js)
2. Frontend depois (HubSidebar.html)
3. Testes


## Verificacao
- [ ] Cenario 1: ...
- [ ] Cenario 2: ...
```


**Acao final:** Pedir ao usuario para usar `/clear` antes de seguir para a ETAPA 3.


---


### ETAPA 3: IMPLEMENTACAO (Code)


**Objetivo:** Implementar exatamente o que esta no Spec.md, com contexto limpo e maximo de qualidade.


**O que fazer:**
1. Ler o `docs/Spec.md`
2. Seguir a ordem de implementacao definida
3. Implementar arquivo por arquivo, conforme especificado
4. Nao inventar nada alem do que esta no Spec — se algo novo surgir, documentar como "divida tecnica" para proxima sprint
5. Ao terminar, atualizar `FORGABRIEL.md` com os aprendizados da sprint


**Regras durante a implementacao:**
- NAO explorar o codebase novamente (isso ja foi feito na ETAPA 1)
- NAO redesenhar a solucao (isso ja foi feito na ETAPA 2)
- FOCO total em codigo — contexto limpo = mais espaco para qualidade
- Se encontrar algo inesperado, anotar e seguir — nao desviar do plano


---


## Regras Gerais do SDD


1. **Nunca pular etapas.** Sem PRD, nao faz Spec. Sem Spec, nao implementa.
2. **`/clear` entre etapas e obrigatorio.** O contexto da pesquisa polui a implementacao. Limpe sempre.
3. **Mantenha o contexto enxuto.** Alimente a IA apenas com informacoes relevantes, nunca dumps gigantes.
4. **Code snippets > descricoes em texto.** Mostre como fazer, nao apenas diga.
5. **Uma sprint = uma feature.** Nao misture features na mesma sprint. Se surgirem novas ideias, anote para a proxima.
6. **Spec e contrato.** Se durante a implementacao perceber que o Spec esta errado, PARE e atualize o Spec antes de continuar.


---


## Estrutura de Pastas


```
docs/
  PRD.md        ← Pesquisa (ETAPA 1)
  Spec.md       ← Especificacao (ETAPA 2)
FORGABRIEL.md   ← Documentacao acumulada do projeto
CLAUDE.md       ← Este arquivo (instrucoes para o agente)
```


Os arquivos PRD.md e Spec.md sao sobrescritos a cada nova sprint — eles representam o trabalho *atual*, nao historico. O historico fica no FORGABRIEL.md.