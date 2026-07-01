from datetime import datetime
from pathlib import Path
import re

PASTA_ENTRADA = Path("entrada")
PASTA_SAIDA = Path("saida")
AVISO_LEGISLACAO = (
    "Conferir a legislação, súmulas e jurisprudência atualizadas antes de usar "
    "este material em prova, peça ou caso prático."
)


def limpar_texto(texto):
    return texto.replace("\ufeff", "").strip()


def titulo_por_nome_arquivo(nome_arquivo):
    if not nome_arquivo:
        return "Tema jurídico"

    titulo = nome_arquivo.replace("_", " ").replace("-", " ").strip()
    return titulo.title() if titulo else "Tema jurídico"


def extrair_sentencas(texto, limite=5):
    texto_limpo = " ".join(limpar_texto(texto).split())
    if not texto_limpo:
        return []

    sentencas = re.split(r"(?<=[.!?])\s+", texto_limpo)
    sentencas = [sentenca.strip() for sentenca in sentencas if sentenca.strip()]
    return sentencas[:limite]


def resumir_pontos_principais(texto, limite=4):
    sentencas = extrair_sentencas(texto, limite=limite)
    if sentencas:
        return sentencas

    return ["Nenhum conteúdo foi informado para análise."]


def gerar_questoes_fixacao(texto, tema):
    pontos = resumir_pontos_principais(texto, limite=2)
    primeiro_ponto = pontos[0]

    return [
        f"Qual é o conceito central de {tema}?",
        f"Explique, com suas palavras, a seguinte ideia: {primeiro_ponto}",
        "Quais informações do texto indicam regra geral, exceção ou classificação?",
        "Qual fundamento legal precisa ser conferido antes de usar esse conteúdo?",
        "Que pegadinha de prova poderia aparecer sobre esse tema?",
    ]


def gerar_flashcards(texto, tema):
    pontos = resumir_pontos_principais(texto, limite=3)

    return [
        {
            "frente": "Qual é o tema central?",
            "verso": tema,
        },
        {
            "frente": "Qual é a ideia principal do texto?",
            "verso": pontos[0],
        },
        {
            "frente": "Qual cuidado jurídico é obrigatório?",
            "verso": AVISO_LEGISLACAO,
        },
        {
            "frente": "Como transformar o conteúdo em resposta de OAB?",
            "verso": "Identifique o fato, indique o fundamento, formule a tese e conclua com o pedido ou providência.",
        },
    ]


def gerar_checklist_oab():
    return [
        "Identifique o tema e o subtema jurídico.",
        "Separe fato, fundamento, risco e próximo passo.",
        "Confira a legislação atualizada antes de citar artigo, súmula ou jurisprudência.",
        "Verifique se há regra geral, exceção, prazo ou competência.",
        "Formule uma tese objetiva em linguagem de prova.",
        "Treine ao menos uma questão discursiva sobre o conteúdo.",
        "Revise os flashcards até responder sem consultar o resumo.",
    ]


def gerar_analise_pratica(texto):
    pontos = resumir_pontos_principais(texto, limite=1)

    return {
        "Fato": pontos[0],
        "Fundamento": "Fundamento jurídico deve ser conferido em legislação atualizada antes do uso.",
        "Risco": "Risco de citar artigo, súmula ou jurisprudência desatualizados ou inexistentes.",
        "Próximo passo": "Conferir a base legal aplicável e resolver questões de fixação sobre o tema.",
    }


def formatar_lista_numerada(itens):
    return "\n".join(f"{indice}. {item}" for indice, item in enumerate(itens, start=1))


def formatar_checklist(itens):
    return "\n".join(f"- [ ] {item}" for item in itens)


def escapar_tabela_markdown(texto):
    return texto.replace("|", "\\|").replace("\n", " ")


def formatar_flashcards(flashcards):
    linhas = ["| Frente | Verso |", "| --- | --- |"]
    for flashcard in flashcards:
        frente = escapar_tabela_markdown(flashcard["frente"])
        verso = escapar_tabela_markdown(flashcard["verso"])
        linhas.append(f"| {frente} | {verso} |")

    return "\n".join(linhas)


def gerar_resumo(texto, nome_arquivo=None, gerado_em=None):
    texto_limpo = limpar_texto(texto)
    tema = titulo_por_nome_arquivo(nome_arquivo)
    data = gerado_em or datetime.now()
    pontos = resumir_pontos_principais(texto_limpo)
    questoes = gerar_questoes_fixacao(texto_limpo, tema)
    flashcards = gerar_flashcards(texto_limpo, tema)
    checklist = gerar_checklist_oab()
    analise = gerar_analise_pratica(texto_limpo)

    pontos_formatados = "\n".join(f"- {ponto}" for ponto in pontos)
    analise_formatada = "\n".join(
        f"- **{chave}:** {valor}" for chave, valor in analise.items()
    )

    resumo = f"""\
# Resumo Jurídico Gerado

Data: {data.strftime("%d/%m/%Y %H:%M")}

Tema: {tema}

> {AVISO_LEGISLACAO}

## 1. Resumo Estruturado

### Pontos principais
{pontos_formatados}

### Base legal
Não foi feita pesquisa externa nem validação legislativa automática. Use o texto como material de estudo e confira a legislação atualizada antes de citar artigos, súmulas ou jurisprudência.

## 2. Análise Prática
{analise_formatada}

## 3. Questões de Fixação

{formatar_lista_numerada(questoes)}

## 4. Flashcards

{formatar_flashcards(flashcards)}

## 5. Checklist de Revisão OAB

{formatar_checklist(checklist)}

## 6. Texto Analisado

{texto_limpo}
"""
    return resumo


def listar_arquivos_txt(pasta_entrada):
    if not pasta_entrada.exists():
        return []

    return sorted(pasta_entrada.glob("*.txt"))


def processar_arquivo(arquivo, pasta_saida):
    texto = arquivo.read_text(encoding="utf-8-sig")
    resultado = gerar_resumo(texto, nome_arquivo=arquivo.stem)

    pasta_saida.mkdir(parents=True, exist_ok=True)
    saida = pasta_saida / f"resumo_{arquivo.stem}.md"
    saida.write_text(resultado, encoding="utf-8")

    return saida


def main(pasta_entrada=None, pasta_saida=None):
    pasta_entrada = pasta_entrada or PASTA_ENTRADA
    pasta_saida = pasta_saida or PASTA_SAIDA
    arquivos = listar_arquivos_txt(pasta_entrada)

    if not arquivos:
        print("Nenhum arquivo .txt encontrado na pasta entrada.")
        print("Crie um arquivo chamado entrada\\tema.txt e rode novamente.")
        return

    for arquivo in arquivos:
        saida = processar_arquivo(arquivo, pasta_saida)
        print(f"Resumo gerado: {saida}")


if __name__ == "__main__":
    main()
