from datetime import date, datetime

from scripts import agente_juridico


def test_gerar_resumo_inclui_academia_arquitetura_aula_revisoes_e_desempenho():
    texto = (
        "\ufeffDireito penal estuda o crime, a pena e as medidas de segurança. "
        "A teoria do crime organiza fato típico, ilicitude e culpabilidade."
    )

    resumo = agente_juridico.gerar_resumo(
        texto,
        nome_arquivo="direito_penal_teoria_crime",
        gerado_em=datetime(2026, 7, 1, 10, 30),
    )

    assert "# Academia Jurídica IA" in resumo
    assert "Data: 01/07/2026 10:30" in resumo
    assert "Tema: Direito Penal Teoria Crime" in resumo
    assert "Disciplina inferida: Direito Penal" in resumo
    assert "Semestre: semestre_01" in resumo
    assert "## 1. Arquitetura Modular" in resumo
    assert "`aulas/`: aulas estruturadas por disciplina e tema" in resumo
    assert "## 2. Disciplinas do Semestre" in resumo
    assert "| Direito Penal |" in resumo
    assert "## 3. Plano Semanal" in resumo
    assert "### Segunda-feira: Direito Penal" in resumo
    assert "## 4. Aula Estruturada" in resumo
    assert "### Objetivo da aula" in resumo
    assert "### Base legal" in resumo
    assert "Código Penal" in resumo
    assert "- **Fato:** Direito penal estuda o crime" in resumo
    assert "- **Fundamento:**" in resumo
    assert "- **Risco:**" in resumo
    assert "- **Próximo passo:**" in resumo
    assert "## 5. Questões Objetivas" in resumo
    assert "**Gabarito:**" in resumo
    assert "## 6. Questões Discursivas" in resumo
    assert "**Espelho mínimo**" in resumo
    assert "## 7. Revisões Espaçadas" in resumo
    assert "### D+1 - 02/07/2026" in resumo
    assert "### D+30 - 31/07/2026" in resumo
    assert "#### 5 perguntas rápidas" in resumo
    assert "#### 3 questões objetivas" in resumo
    assert "#### 1 questão discursiva" in resumo
    assert "#### 1 resumo de memória" in resumo
    assert "## 8. Flashcards" in resumo
    assert "| Frente | Verso |" in resumo
    assert "## 9. Simulado" in resumo
    assert "Simulado de fixação" in resumo
    assert "## 10. Desempenho" in resumo
    assert "A preencher após a correção dos exercícios." in resumo
    assert "## 11. Checklist de Estudo" in resumo
    assert "Conferir a legislação, súmulas e jurisprudência atualizadas" in resumo
    assert "## 12. Texto Analisado" in resumo
    assert "\ufeff" not in resumo


def test_gerar_pacote_estudo_expoe_componentes_modulares():
    pacote = agente_juridico.gerar_pacote_estudo(
        "Direito constitucional protege direitos e garantias fundamentais.",
        nome_arquivo="direito_constitucional_direitos_fundamentais",
        gerado_em=datetime(2026, 7, 1, 9, 0),
    )

    assert pacote["projeto"] == "Academia Jurídica IA"
    assert pacote["disciplina"] == "Direito Constitucional"
    assert pacote["semestre"] == "semestre_01"
    assert pacote["arquitetura"]["pastas"]["flashcards"] == "cartões de memorização por tema"
    assert "semestre_10" in pacote["arquitetura"]["semestres"]
    assert len(pacote["aula"]["exercicios"]["objetivas"]) == 3
    assert len(pacote["questoes_objetivas"]) == 3
    assert len(pacote["questoes_discursivas"]) == 2
    assert len(pacote["flashcards"]) >= 4
    assert [revisao["intervalo"] for revisao in pacote["revisoes"]] == [
        "D+1",
        "D+3",
        "D+7",
        "D+15",
        "D+30",
    ]
    assert pacote["simulado"]["questoes_discursivas"]
    assert pacote["desempenho"]["pontos_fracos"]
    assert any("pontos fracos" in item for item in pacote["checklist"])


def test_criar_arquitetura_modular_cria_pastas_base(tmp_path):
    caminhos = agente_juridico.criar_arquitetura_modular(tmp_path)

    for nome in (
        "disciplinas",
        "semestres",
        "aulas",
        "revisoes",
        "flashcards",
        "questoes",
        "simulados",
        "desempenho",
        "planos_semanais",
    ):
        assert caminhos[nome].is_dir()

    assert (tmp_path / "questoes" / "objetivas").is_dir()
    assert (tmp_path / "questoes" / "discursivas").is_dir()


def test_salvar_pacote_modular_cria_arquivos_em_pastas_de_ensino(tmp_path):
    pacote = agente_juridico.gerar_pacote_estudo(
        "Direito administrativo exige legalidade, motivação e controle dos atos administrativos.",
        nome_arquivo="atos_administrativos",
        gerado_em=datetime(2026, 7, 1, 8, 0),
    )

    caminhos = agente_juridico.salvar_pacote_modular(pacote, base_dir=tmp_path)

    esperados = {
        "disciplina",
        "semestre",
        "aula",
        "questoes_objetivas",
        "questoes_discursivas",
        "revisoes",
        "flashcards",
        "simulado",
        "desempenho",
        "plano_semanal",
        "checklist",
    }
    assert set(caminhos) == esperados

    for caminho in caminhos.values():
        assert caminho.exists()

    assert caminhos["aula"] == (
        tmp_path / "aulas" / "direito-administrativo" / "Atos Administrativos".lower().replace(" ", "-")
    ).with_suffix(".md")
    assert "# Aula Estruturada - Atos Administrativos" in caminhos["aula"].read_text(
        encoding="utf-8"
    )
    assert "# Questões Objetivas - Atos Administrativos" in caminhos[
        "questoes_objetivas"
    ].read_text(encoding="utf-8")
    assert "# Checklist de Estudo - Atos Administrativos" in caminhos["checklist"].read_text(
        encoding="utf-8"
    )


def test_gerar_plano_semanal_aceita_disciplinas_customizadas():
    plano = agente_juridico.gerar_plano_semanal(
        disciplinas=["Direito Penal", "Processo Penal"],
        horas_por_dia=3,
    )

    assert len(plano) == 6
    assert plano[0]["dia"] == "Segunda-feira"
    assert plano[0]["disciplina"] == "Direito Penal"
    assert plano[0]["modulo"] == "Teoria da norma penal"
    assert plano[0]["carga_horaria"] == 3
    assert plano[1]["disciplina"] == "Processo Penal"
    assert plano[1]["modulo"] == "Ação penal"
    assert any("pontos fracos" in tarefa for tarefa in plano[0]["tarefas"])
    assert any("revisões espaçadas" in tarefa for tarefa in plano[3]["tarefas"])


def test_revisoes_espacadas_criam_ciclos_com_exercicios():
    revisoes = agente_juridico.gerar_revisoes_espacadas(
        "Direito administrativo exige controle da legalidade dos atos administrativos.",
        "Atos Administrativos",
        data_base=date(2026, 7, 1),
    )

    assert [revisao["intervalo"] for revisao in revisoes] == [
        "D+1",
        "D+3",
        "D+7",
        "D+15",
        "D+30",
    ]
    assert revisoes[0]["data"] == date(2026, 7, 2)
    assert revisoes[-1]["data"] == date(2026, 7, 31)
    assert len(revisoes[0]["perguntas_rapidas"]) == 5
    assert len(revisoes[0]["questoes_objetivas"]) == 3
    assert "enunciado" in revisoes[0]["questao_discursiva"]
    assert "resumo de memória" in agente_juridico.formatar_revisoes_espacadas(revisoes)


def test_questoes_e_registro_de_pontos_fracos_sao_estruturados():
    texto = "Processo penal organiza a persecução penal e a proteção das garantias fundamentais."

    objetivas = agente_juridico.gerar_questoes_objetivas(texto, "Processo Penal")
    discursivas = agente_juridico.gerar_questoes_discursivas(texto, "Processo Penal")
    registro = agente_juridico.registrar_ponto_fraco(
        "Processo Penal",
        "Ação penal",
        "Confunde titularidade da ação penal pública e privada.",
        "Revisar classificação da ação penal e resolver questões.",
        registrado_em=datetime(2026, 7, 1, 8, 0),
    )

    assert len(objetivas) == 3
    assert objetivas[0]["alternativas"][0].startswith("Processo penal organiza")
    assert objetivas[1]["gabarito"] == "C"
    assert discursivas[0]["espelho"]["Fato"].startswith("Processo penal organiza")
    assert discursivas[0]["espelho"]["Próximo passo"]
    assert registro == {
        "data": "01/07/2026",
        "disciplina": "Processo Penal",
        "tema": "Ação penal",
        "ponto_fraco": "Confunde titularidade da ação penal pública e privada.",
        "acao_recomendada": "Revisar classificação da ação penal e resolver questões.",
        "status": "pendente",
    }
    tabela = agente_juridico.formatar_pontos_fracos([registro])
    assert "| Data | Disciplina | Tema | Ponto fraco | Ação recomendada | Status |" in tabela
    assert "Confunde titularidade" in tabela


def test_main_le_arquivos_txt_da_entrada_e_gera_material_na_saida_e_modulos(tmp_path, capsys):
    pasta_entrada = tmp_path / "entrada"
    pasta_saida = tmp_path / "saida"
    pasta_entrada.mkdir()

    texto = (
        "Direito sucessório trata da transmissão do patrimônio da pessoa falecida "
        "aos seus herdeiros. A sucessão pode ser legítima ou testamentária."
    )
    arquivo_entrada = pasta_entrada / "direito_sucessorio.txt"
    arquivo_entrada.write_text(texto, encoding="utf-8")
    (pasta_entrada / "ignorado.md").write_text("nao deve gerar material", encoding="utf-8")

    agente_juridico.main(pasta_entrada=pasta_entrada, pasta_saida=pasta_saida)

    arquivo_saida = pasta_saida / "resumo_direito_sucessorio.md"
    assert arquivo_saida.exists()
    resumo = arquivo_saida.read_text(encoding="utf-8")
    assert "# Academia Jurídica IA" in resumo
    assert "Disciplina inferida: Direito das Sucessões" in resumo
    assert "## 4. Aula Estruturada" in resumo
    assert "## 7. Revisões Espaçadas" in resumo
    assert "## 10. Desempenho" in resumo
    assert texto in resumo
    assert not (pasta_saida / "resumo_ignorado.md").exists()

    disciplina_dir = tmp_path / "aulas" / "direito-das-sucessoes"
    assert (disciplina_dir / "direito-sucessorio.md").exists()
    assert (
        tmp_path
        / "questoes"
        / "objetivas"
        / "direito-das-sucessoes"
        / "direito-sucessorio.md"
    ).exists()
    assert (
        tmp_path / "planos_semanais" / "direito-das-sucessoes" / "direito-sucessorio_checklist.md"
    ).exists()
    assert f"Material de aula gerado: {arquivo_saida}" in capsys.readouterr().out


def test_listar_arquivos_txt_retorna_apenas_txt_ordenados(tmp_path):
    pasta_entrada = tmp_path / "entrada"
    pasta_entrada.mkdir()
    arquivo_b = pasta_entrada / "b.txt"
    arquivo_a = pasta_entrada / "a.txt"
    arquivo_b.write_text("b", encoding="utf-8")
    arquivo_a.write_text("a", encoding="utf-8")
    (pasta_entrada / "c.md").write_text("c", encoding="utf-8")

    arquivos = agente_juridico.listar_arquivos_txt(pasta_entrada)

    assert arquivos == [arquivo_a, arquivo_b]


def test_main_avisa_quando_nao_ha_arquivo_txt(tmp_path, capsys):
    pasta_entrada = tmp_path / "entrada"
    pasta_saida = tmp_path / "saida"
    pasta_entrada.mkdir()

    agente_juridico.main(pasta_entrada=pasta_entrada, pasta_saida=pasta_saida)

    saida = capsys.readouterr().out
    assert "Nenhum arquivo .txt encontrado na pasta entrada." in saida
    assert not pasta_saida.exists()
