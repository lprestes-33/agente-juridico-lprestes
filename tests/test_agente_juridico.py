from datetime import datetime

from scripts import agente_juridico


def test_gerar_resumo_inclui_estrutura_juridica_questoes_flashcards_e_checklist():
    texto = (
        "\ufeffDireito sucessório trata da transmissão do patrimônio da pessoa falecida "
        "aos seus herdeiros. A sucessão pode ser legítima ou testamentária."
    )

    resumo = agente_juridico.gerar_resumo(
        texto,
        nome_arquivo="tema_sucessorio",
        gerado_em=datetime(2026, 7, 1, 10, 30),
    )

    assert "# Resumo Jurídico Gerado" in resumo
    assert "Data: 01/07/2026 10:30" in resumo
    assert "Tema: Tema Sucessorio" in resumo
    assert "## 1. Resumo Estruturado" in resumo
    assert "## 2. Análise Prática" in resumo
    assert "- **Fato:** Direito sucessório trata da transmissão" in resumo
    assert "- **Fundamento:**" in resumo
    assert "- **Risco:**" in resumo
    assert "- **Próximo passo:**" in resumo
    assert "## 3. Questões de Fixação" in resumo
    assert "1. Qual é o conceito central de Tema Sucessorio?" in resumo
    assert "## 4. Flashcards" in resumo
    assert "| Frente | Verso |" in resumo
    assert "Qual cuidado jurídico é obrigatório?" in resumo
    assert "## 5. Checklist de Revisão OAB" in resumo
    assert "- [ ] Identifique o tema e o subtema jurídico." in resumo
    assert "Conferir a legislação, súmulas e jurisprudência atualizadas" in resumo
    assert "## 6. Texto Analisado" in resumo
    assert "\ufeff" not in resumo
    assert "A sucessão pode ser legítima ou testamentária." in resumo


def test_main_le_arquivos_txt_da_entrada_e_gera_resumo_na_saida(tmp_path, capsys):
    pasta_entrada = tmp_path / "entrada"
    pasta_saida = tmp_path / "saida"
    pasta_entrada.mkdir()

    texto = (
        "Direito penal estuda o crime, a pena e as medidas de segurança. "
        "A resposta deve separar fato, fundamento, risco e próximo passo."
    )
    arquivo_entrada = pasta_entrada / "direito_penal.txt"
    arquivo_entrada.write_text(texto, encoding="utf-8")
    (pasta_entrada / "ignorado.md").write_text("nao deve gerar resumo", encoding="utf-8")

    agente_juridico.main(pasta_entrada=pasta_entrada, pasta_saida=pasta_saida)

    arquivo_saida = pasta_saida / "resumo_direito_penal.md"
    assert arquivo_saida.exists()
    resumo = arquivo_saida.read_text(encoding="utf-8")
    assert "# Resumo Jurídico Gerado" in resumo
    assert "Tema: Direito Penal" in resumo
    assert "## 3. Questões de Fixação" in resumo
    assert "## 4. Flashcards" in resumo
    assert "## 5. Checklist de Revisão OAB" in resumo
    assert texto in resumo
    assert not (pasta_saida / "resumo_ignorado.md").exists()
    assert f"Resumo gerado: {arquivo_saida}" in capsys.readouterr().out


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
