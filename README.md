# Academia Jurídica IA

Plataforma pessoal de ensino jurídico com foco em graduação de Direito, OAB,
concursos policiais, revisões e organização de conhecimento.

O projeto lê materiais `.txt` em `entrada/`, gera um material consolidado em
`saida/` e também distribui os conteúdos em uma arquitetura modular de estudo.

> A plataforma não valida legislação automaticamente. Antes de usar o material em
> prova, peça, simulado ou caso prático, confira legislação, súmulas e
> jurisprudência atualizadas em fonte oficial.

## Recursos

- Aula estruturada com objetivo, contexto, explicação didática, base legal,
  exemplo prático, jurisprudência, pegadinhas, exercícios e revisão final.
- Questões objetivas com alternativas, gabarito e comentário.
- Questões discursivas com espelho mínimo baseado em fato, fundamento, risco e
  próximo passo.
- Flashcards por tema.
- Revisões espaçadas em D+1, D+3, D+7, D+15 e D+30.
- Simulados de fixação por tema.
- Registro de pontos fracos e desempenho.
- Plano semanal e checklist de estudo.

## Arquitetura Modular

- `entrada/`: textos, PDFs convertidos e materiais para análise.
- `saida/`: material consolidado gerado a partir de cada entrada.
- `disciplinas/`: catálogo e trilhas por disciplina.
- `semestres/`: organização curricular por semestre.
- `aulas/`: aulas estruturadas por disciplina e tema.
- `revisoes/`: revisões espaçadas.
- `flashcards/`: cartões de memorização.
- `questoes/objetivas/`: questões objetivas por disciplina.
- `questoes/discursivas/`: questões discursivas por disciplina.
- `simulados/`: simulados por disciplina e tema.
- `desempenho/`: pontos fracos, ações recomendadas e acompanhamento.
- `planos_semanais/`: rotinas semanais e checklists.
- `regras/`: regras de atuação do agente.
- `modelos/`: modelos de peças.
- `pecas/`: peças processuais.
- `jurisprudencia/`: julgados e entendimentos fornecidos pelo usuário.
- `scripts/`: automações em Python.
- `tests/`: testes automatizados com pytest.

## Como Usar

1. Crie um arquivo `.txt` em `entrada/`.
2. Rode o script:

```bash
python scripts/agente_juridico.py
```

3. Consulte o resumo em `saida/resumo_nome_do_arquivo.md`.
4. Consulte os materiais separados nas pastas modulares.

## Funções Principais

- `gerar_pacote_estudo()`: cria o pacote completo de aprendizagem.
- `gerar_arquitetura_modular()`: descreve a estrutura da plataforma.
- `criar_arquitetura_modular()`: cria as pastas da plataforma.
- `gerar_aula_estruturada()`: monta a aula pelo método pedagógico.
- `gerar_questoes_objetivas()`: cria questões objetivas.
- `gerar_questoes_discursivas()`: cria questões discursivas.
- `gerar_flashcards()`: cria flashcards.
- `gerar_revisoes_espacadas()`: cria ciclos D+1, D+3, D+7, D+15 e D+30.
- `gerar_simulado()`: monta simulado de fixação.
- `gerar_plano_semanal()`: cria rotina semanal de estudo.
- `gerar_checklist_estudo()`: cria checklist de revisão e execução.

## Testes

Execute:

```bash
python -m pytest
```
