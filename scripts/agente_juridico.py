from datetime import date, datetime, timedelta
from pathlib import Path
import re
import unicodedata

PASTA_ENTRADA = Path("entrada")
PASTA_SAIDA = Path("saida")
NOME_PROJETO = "Academia Jurídica IA"
SEMESTRE_PADRAO = "semestre_01"
PASTAS_ARQUITETURA = {
    "disciplinas": Path("disciplinas"),
    "semestres": Path("semestres"),
    "aulas": Path("aulas"),
    "revisoes": Path("revisoes"),
    "flashcards": Path("flashcards"),
    "questoes": Path("questoes"),
    "simulados": Path("simulados"),
    "desempenho": Path("desempenho"),
    "planos_semanais": Path("planos_semanais"),
}
AVISO_LEGISLACAO = (
    "Conferir a legislação, súmulas e jurisprudência atualizadas antes de usar "
    "este material em prova, peça ou caso prático."
)
REVISOES_ESPACADAS_DIAS = (1, 3, 7, 15, 30)
DIAS_PLANO_SEMANAL = (
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
)

DISCIPLINAS_PADRAO_SEMESTRE = [
    {
        "nome": "Direito Penal",
        "modulos": [
            "Teoria da norma penal",
            "Teoria do crime",
            "Penas e medidas de segurança",
            "Crimes em espécie",
        ],
        "conexao": "OAB, graduação e concursos policiais",
    },
    {
        "nome": "Processo Penal",
        "modulos": [
            "Inquérito policial",
            "Ação penal",
            "Provas",
            "Prisões, medidas cautelares e recursos",
        ],
        "conexao": "OAB, prática penal e concursos policiais",
    },
    {
        "nome": "Direito Administrativo",
        "modulos": [
            "Princípios administrativos",
            "Atos administrativos",
            "Licitações e contratos",
            "Responsabilidade civil do Estado",
        ],
        "conexao": "OAB e concursos públicos",
    },
    {
        "nome": "Direito Constitucional",
        "modulos": [
            "Teoria da Constituição",
            "Direitos e garantias fundamentais",
            "Organização do Estado",
            "Controle de constitucionalidade",
        ],
        "conexao": "OAB e concursos públicos",
    },
    {
        "nome": "Direito Civil",
        "modulos": [
            "Parte geral",
            "Obrigações",
            "Contratos",
            "Responsabilidade civil",
        ],
        "conexao": "OAB e prática cível",
    },
    {
        "nome": "Processo Civil",
        "modulos": [
            "Jurisdição e competência",
            "Petição inicial e resposta do réu",
            "Provas e sentença",
            "Recursos e cumprimento de sentença",
        ],
        "conexao": "OAB e prática cível",
    },
    {
        "nome": "Direito do Trabalho",
        "modulos": [
            "Relação de emprego",
            "Contrato de trabalho",
            "Jornada e remuneração",
            "Rescisão contratual",
        ],
        "conexao": "OAB e prática trabalhista",
    },
    {
        "nome": "Direito das Sucessões",
        "modulos": [
            "Abertura da sucessão",
            "Herdeiros e ordem de vocação hereditária",
            "Sucessão legítima e testamentária",
            "Inventário e partilha",
        ],
        "conexao": "OAB e prática cível",
    },
]

BASE_LEGAL_POR_DISCIPLINA = {
    "Direito Penal": "Código Penal, Constituição Federal e legislação penal especial pertinente ao tema.",
    "Processo Penal": "Código de Processo Penal, Constituição Federal e legislação processual penal especial pertinente ao tema.",
    "Direito Administrativo": "Constituição Federal, leis administrativas gerais e legislação especial aplicável ao tema.",
    "Direito Constitucional": "Constituição Federal, legislação de controle constitucional e entendimentos atualizados aplicáveis.",
    "Direito Civil": "Código Civil, Constituição Federal e legislação civil especial pertinente ao tema.",
    "Processo Civil": "Código de Processo Civil, Constituição Federal e legislação processual especial pertinente ao tema.",
    "Direito do Trabalho": "CLT, Constituição Federal e legislação trabalhista especial pertinente ao tema.",
    "Direito das Sucessões": "Código Civil, legislação especial aplicável e entendimentos atualizados pertinentes ao tema.",
    "Formação Jurídica Geral": "Legislação pertinente ao tema, sempre conferida em fonte oficial e atualizada.",
}

ALIASES_DISCIPLINAS = [
    ("Processo Penal", ("processo penal", "processual penal", "cpp")),
    ("Processo Civil", ("processo civil", "processual civil", "cpc")),
    ("Direito das Sucessões", ("sucessorio", "sucessorios", "sucessao", "sucessoes")),
    ("Direito Administrativo", ("administrativo", "administracao publica")),
    ("Direito Constitucional", ("constitucional", "constituicao", "direitos fundamentais")),
    ("Direito do Trabalho", ("trabalho", "trabalhista", "clt")),
    ("Direito Penal", ("penal", "crime", "pena", "criminologia")),
    ("Direito Civil", ("civil", "contrato", "obrigacoes", "responsabilidade civil")),
]


def limpar_texto(texto):
    return texto.replace("\ufeff", "").strip()


def normalizar_chave(texto):
    texto_sem_acentos = unicodedata.normalize("NFKD", texto or "")
    texto_ascii = "".join(
        caractere for caractere in texto_sem_acentos if not unicodedata.combining(caractere)
    )
    texto_ascii = re.sub(r"[^a-z0-9]+", " ", texto_ascii.lower())
    return " ".join(texto_ascii.split())


def slugificar(texto):
    return normalizar_chave(texto).replace(" ", "-") or "tema-juridico"


def alias_presente(origem, alias):
    alias_normalizado = normalizar_chave(alias)
    return f" {alias_normalizado} " in f" {origem} "


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


def inferir_disciplina(nome_arquivo=None, texto=""):
    origem = normalizar_chave(f"{nome_arquivo or ''} {texto or ''}")
    for disciplina, aliases in ALIASES_DISCIPLINAS:
        if any(alias_presente(origem, alias) for alias in aliases):
            return disciplina

    return "Formação Jurídica Geral"


def obter_modulos_disciplina(nome_disciplina):
    for disciplina in DISCIPLINAS_PADRAO_SEMESTRE:
        if disciplina["nome"] == nome_disciplina:
            return list(disciplina["modulos"])

    return [
        "Conceitos fundamentais",
        "Base legal e princípios",
        "Classificações, exceções e controvérsias",
        "Aplicação prática e resolução de questões",
    ]


def normalizar_disciplinas(disciplinas=None):
    disciplinas = disciplinas or DISCIPLINAS_PADRAO_SEMESTRE
    normalizadas = []

    for disciplina in disciplinas:
        if isinstance(disciplina, str):
            nome = disciplina
            modulos = obter_modulos_disciplina(nome)
            conexao = "Graduação, OAB e concursos"
        else:
            nome = disciplina.get("nome", "Disciplina jurídica")
            modulos = disciplina.get("modulos") or obter_modulos_disciplina(nome)
            conexao = disciplina.get("conexao", "Graduação, OAB e concursos")

        normalizadas.append(
            {
                "nome": nome,
                "modulos": list(modulos),
                "conexao": conexao,
            }
        )

    return normalizadas


def gerar_disciplinas_semestre(disciplinas=None):
    return normalizar_disciplinas(disciplinas)


def gerar_arquitetura_modular(disciplinas=None, total_semestres=10):
    disciplinas_semestre = gerar_disciplinas_semestre(disciplinas)

    return {
        "projeto": NOME_PROJETO,
        "pastas": {
            "disciplinas": "catálogo de disciplinas, módulos e trilhas",
            "semestres": "organização curricular por semestre",
            "aulas": "aulas estruturadas por disciplina e tema",
            "revisoes": "revisões espaçadas D+1, D+3, D+7, D+15 e D+30",
            "flashcards": "cartões de memorização por tema",
            "questoes": "questões objetivas e discursivas",
            "simulados": "simulados por disciplina ou tema",
            "desempenho": "pontos fracos, ações recomendadas e evolução",
            "planos_semanais": "rotinas semanais e checklists de estudo",
        },
        "disciplinas": [
            {
                "nome": disciplina["nome"],
                "slug": slugificar(disciplina["nome"]),
                "modulos": disciplina["modulos"],
                "conexao": disciplina["conexao"],
            }
            for disciplina in disciplinas_semestre
        ],
        "semestres": [f"semestre_{indice:02d}" for indice in range(1, total_semestres + 1)],
    }


def criar_arquitetura_modular(base_dir=None):
    base = Path(base_dir) if base_dir else Path(".")
    caminhos = {nome: base / caminho for nome, caminho in PASTAS_ARQUITETURA.items()}

    for caminho in caminhos.values():
        caminho.mkdir(parents=True, exist_ok=True)

    (caminhos["questoes"] / "objetivas").mkdir(parents=True, exist_ok=True)
    (caminhos["questoes"] / "discursivas").mkdir(parents=True, exist_ok=True)

    return caminhos


def gerar_plano_semanal(disciplinas=None, horas_por_dia=2):
    disciplinas_semestre = gerar_disciplinas_semestre(disciplinas)
    plano = []

    for indice, dia in enumerate(DIAS_PLANO_SEMANAL):
        disciplina = disciplinas_semestre[indice % len(disciplinas_semestre)]
        modulo = disciplina["modulos"][indice % len(disciplina["modulos"])]
        tarefas = [
            f"Estudar {modulo} com leitura ativa e anotações.",
            "Separar teoria, exemplo prático, base legal a conferir e dúvida principal.",
            "Resolver 3 questões objetivas e 1 questão discursiva.",
            "Registrar erros, inseguranças e pontos fracos após a correção.",
        ]

        if dia in ("Quinta-feira", "Sábado"):
            tarefas.append("Executar revisões espaçadas pendentes antes de avançar conteúdo.")

        plano.append(
            {
                "dia": dia,
                "disciplina": disciplina["nome"],
                "modulo": modulo,
                "carga_horaria": horas_por_dia,
                "tarefas": tarefas,
            }
        )

    return plano


def gerar_perguntas_rapidas(texto, tema, quantidade=5):
    pontos = resumir_pontos_principais(texto, limite=2)
    perguntas = [
        f"Qual é o conceito central de {tema}?",
        "Qual é a regra geral apresentada no material?",
        "Existe exceção, prazo, competência ou classificação relevante?",
        f"Como o tema {tema} pode aparecer em questão de OAB ou concurso policial?",
        "Qual base legal precisa ser conferida antes de citar o conteúdo?",
        f"Qual ponto do tema {tema} você ainda não explicaria sem consultar o material?",
        f"Como resumir a ideia principal em uma frase? Ponto de partida: {pontos[0]}",
    ]
    return perguntas[:quantidade]


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


def gerar_questoes_objetivas(texto, tema, quantidade=3):
    pontos = resumir_pontos_principais(texto, limite=3)
    questoes_base = [
        {
            "pergunta": f"Sobre {tema}, qual alternativa melhor representa a ideia central do material?",
            "alternativas": [
                pontos[0],
                "A memorização de artigos dispensa a compreensão do caso concreto.",
                "Jurisprudência não conferida pode ser tratada como fundamento definitivo.",
                "A resposta jurídica deve ignorar riscos e próximos passos.",
            ],
            "gabarito": "A",
            "comentario": "A alternativa correta retoma o ponto principal extraído do material analisado.",
        },
        {
            "pergunta": "Antes de citar artigo, súmula ou jurisprudência em prova ou peça, qual conduta é adequada?",
            "alternativas": [
                "Usar qualquer referência lembrada de memória.",
                "Evitar base legal e responder apenas por intuição.",
                "Conferir a fonte oficial e atualizada aplicável ao tema.",
                "Citar apenas doutrina genérica sem relacionar ao fato.",
            ],
            "gabarito": "C",
            "comentario": AVISO_LEGISLACAO,
        },
        {
            "pergunta": "Em uma resposta discursiva, qual estrutura atende melhor ao método do agente?",
            "alternativas": [
                "Opinião pessoal, conclusão e repetição do enunciado.",
                "Fato, fundamento, risco e próximo passo.",
                "Resumo livre, sem base legal e sem conclusão.",
                "Cópia integral do texto estudado.",
            ],
            "gabarito": "B",
            "comentario": "A análise prática deve separar fato, fundamento, risco e próximo passo.",
        },
        {
            "pergunta": f"Qual atitude melhora a preparação para provas sobre {tema}?",
            "alternativas": [
                "Estudar apenas na véspera, sem revisão.",
                "Registrar pontos fracos e revisar em ciclos espaçados.",
                "Excluir questões discursivas da rotina.",
                "Ignorar pegadinhas de regra geral e exceção.",
            ],
            "gabarito": "B",
            "comentario": "O registro de erros orienta a revisão e evita repetir a mesma falha.",
        },
    ]
    return questoes_base[:quantidade]


def gerar_questoes_discursivas(texto, tema, quantidade=2):
    pontos = resumir_pontos_principais(texto, limite=2)
    questoes_base = [
        {
            "enunciado": (
                f"Explique {tema} com base no material estudado, indicando conceito, "
                "aplicação prática e cuidado de prova."
            ),
            "espelho": {
                "Fato": pontos[0],
                "Fundamento": "Indicar a base legal pertinente somente após conferência em legislação atualizada.",
                "Risco": "Confundir regra geral com exceção ou citar fundamento desatualizado.",
                "Próximo passo": "Resolver questões e registrar pontos fracos da resposta.",
            },
        },
        {
            "enunciado": (
                f"Relacione {tema} com OAB ou concursos policiais, destacando uma "
                "pegadinha provável e uma forma de evitá-la."
            ),
            "espelho": {
                "Fato": pontos[-1],
                "Fundamento": "Vincular o raciocínio ao texto estudado e à legislação aplicável conferida.",
                "Risco": "Responder de modo abstrato sem enfrentar o problema apresentado.",
                "Próximo passo": "Reescrever a resposta com conclusão objetiva e linguagem de prova.",
            },
        },
    ]
    return questoes_base[:quantidade]


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


def gerar_checklist_estudo():
    return [
        "Classifique o conteúdo por disciplina, semestre, módulo e tema.",
        "Identifique o tema e o subtema jurídico.",
        "Separe fato, fundamento, risco e próximo passo.",
        "Confira a legislação atualizada antes de citar artigo, súmula ou jurisprudência.",
        "Verifique se há regra geral, exceção, prazo ou competência.",
        "Formule uma tese objetiva em linguagem de prova.",
        "Treine ao menos uma questão discursiva sobre o conteúdo.",
        "Revise os flashcards até responder sem consultar o resumo.",
        "Registre erros, inseguranças e pontos fracos para acompanhar desempenho.",
    ]


def gerar_checklist_oab():
    return gerar_checklist_estudo()


def gerar_analise_pratica(texto):
    pontos = resumir_pontos_principais(texto, limite=1)

    return {
        "Fato": pontos[0],
        "Fundamento": "Fundamento jurídico deve ser conferido em legislação atualizada antes do uso.",
        "Risco": "Risco de citar artigo, súmula ou jurisprudência desatualizados ou inexistentes.",
        "Próximo passo": "Conferir a base legal aplicável e resolver questões de fixação sobre o tema.",
    }


def gerar_aula_estruturada(texto, tema, disciplina=None):
    disciplina = disciplina or inferir_disciplina(texto=texto)
    pontos = resumir_pontos_principais(texto, limite=4)
    analise = gerar_analise_pratica(texto)
    questoes_objetivas = gerar_questoes_objetivas(texto, tema, quantidade=3)
    questoes_discursivas = gerar_questoes_discursivas(texto, tema, quantidade=1)

    return {
        "objetivo": (
            f"Compreender {tema} em {disciplina}, dominar a teoria essencial e treinar "
            "aplicação em provas, OAB e concursos policiais."
        ),
        "contexto": pontos[0],
        "explicacao_didatica": pontos,
        "base_legal": BASE_LEGAL_POR_DISCIPLINA.get(
            disciplina, BASE_LEGAL_POR_DISCIPLINA["Formação Jurídica Geral"]
        ),
        "exemplo_pratico": analise,
        "jurisprudencia": (
            "Não pesquisada automaticamente. Use jurisprudência apenas quando fornecida "
            "ou após conferência em fonte atualizada e confiável."
        ),
        "pegadinhas": [
            "Confundir conceito central com exceção.",
            "Citar artigo, súmula ou jurisprudência sem conferência atualizada.",
            "Responder questão discursiva sem separar fato, fundamento, risco e próximo passo.",
        ],
        "exercicios": {
            "objetivas": questoes_objetivas,
            "discursivas": questoes_discursivas,
        },
        "revisao_final": [
            f"Explique {tema} em voz alta sem consultar o material.",
            "Releia a base legal conferida e destaque regra geral, exceções e prazos.",
            "Refaça as questões erradas e registre o motivo do erro.",
        ],
        "tarefa_revisao_espacada": (
            "Agendar revisões em D+1, D+3, D+7, D+15 e D+30, cada uma com perguntas "
            "rápidas, questões objetivas, questão discursiva e resumo de memória."
        ),
    }


def data_base_para_date(data_base):
    if data_base is None:
        return datetime.now().date()
    if isinstance(data_base, datetime):
        return data_base.date()
    if isinstance(data_base, date):
        return data_base
    raise TypeError("data_base deve ser date, datetime ou None.")


def gerar_revisoes_espacadas(texto, tema, data_base=None):
    data_inicial = data_base_para_date(data_base)
    revisoes = []

    for dias in REVISOES_ESPACADAS_DIAS:
        revisoes.append(
            {
                "intervalo": f"D+{dias}",
                "data": data_inicial + timedelta(days=dias),
                "perguntas_rapidas": gerar_perguntas_rapidas(texto, tema, quantidade=5),
                "questoes_objetivas": gerar_questoes_objetivas(texto, tema, quantidade=3),
                "questao_discursiva": gerar_questoes_discursivas(texto, tema, quantidade=1)[0],
                "resumo_memoria": (
                    f"Sem consultar o material, escreva de 5 a 8 linhas sobre {tema}, "
                    "incluindo conceito, base legal conferida, exemplo e pegadinha."
                ),
            }
        )

    return revisoes


def registrar_ponto_fraco(
    disciplina,
    tema,
    descricao,
    acao_recomendada=None,
    registrado_em=None,
    status="pendente",
):
    registrado_em = registrado_em or datetime.now()
    if isinstance(registrado_em, datetime):
        data_registro = registrado_em.strftime("%d/%m/%Y")
    elif isinstance(registrado_em, date):
        data_registro = registrado_em.strftime("%d/%m/%Y")
    else:
        data_registro = str(registrado_em)

    return {
        "data": data_registro,
        "disciplina": disciplina,
        "tema": tema,
        "ponto_fraco": descricao,
        "acao_recomendada": acao_recomendada
        or "Revisar teoria, refazer exercício e explicar o ponto em voz alta.",
        "status": status,
    }


def gerar_registro_pontos_fracos(disciplina, tema, pontos=None, registrado_em=None):
    if not pontos:
        return [
            registrar_ponto_fraco(
                disciplina,
                tema,
                "A preencher após a correção dos exercícios.",
                "Registrar erro, causa provável, revisão necessária e nova tentativa.",
                registrado_em=registrado_em,
            )
        ]

    registros = []
    for ponto in pontos:
        if isinstance(ponto, str):
            registros.append(
                registrar_ponto_fraco(
                    disciplina,
                    tema,
                    ponto,
                    registrado_em=registrado_em,
                )
            )
        else:
            registros.append(
                registrar_ponto_fraco(
                    ponto.get("disciplina", disciplina),
                    ponto.get("tema", tema),
                    ponto.get("ponto_fraco") or ponto.get("descricao", "Ponto fraco não descrito."),
                    ponto.get("acao_recomendada"),
                    registrado_em=ponto.get("data", registrado_em),
                    status=ponto.get("status", "pendente"),
                )
            )

    return registros


def formatar_lista_numerada(itens):
    return "\n".join(f"{indice}. {item}" for indice, item in enumerate(itens, start=1))


def formatar_checklist(itens):
    return "\n".join(f"- [ ] {item}" for item in itens)


def escapar_tabela_markdown(texto):
    return str(texto).replace("|", "\\|").replace("\n", " ")


def formatar_flashcards(flashcards):
    linhas = ["| Frente | Verso |", "| --- | --- |"]
    for flashcard in flashcards:
        frente = escapar_tabela_markdown(flashcard["frente"])
        verso = escapar_tabela_markdown(flashcard["verso"])
        linhas.append(f"| {frente} | {verso} |")

    return "\n".join(linhas)


def formatar_disciplinas_semestre(disciplinas):
    linhas = ["| Disciplina | Módulos | Conexão |", "| --- | --- | --- |"]
    for disciplina in disciplinas:
        linhas.append(
            "| {nome} | {modulos} | {conexao} |".format(
                nome=escapar_tabela_markdown(disciplina["nome"]),
                modulos=escapar_tabela_markdown("; ".join(disciplina["modulos"])),
                conexao=escapar_tabela_markdown(disciplina["conexao"]),
            )
        )
    return "\n".join(linhas)


def formatar_plano_semanal(plano):
    blocos = []
    for item in plano:
        tarefas = "\n".join(f"- [ ] {tarefa}" for tarefa in item["tarefas"])
        blocos.append(
            f"""\
### {item["dia"]}: {item["disciplina"]}
- Módulo: {item["modulo"]}
- Carga sugerida: {item["carga_horaria"]}h
{tarefas}"""
        )
    return "\n\n".join(blocos)


def formatar_analise_pratica(analise):
    return "\n".join(f"- **{chave}:** {valor}" for chave, valor in analise.items())


def formatar_questoes_objetivas(questoes):
    blocos = []
    letras = ("A", "B", "C", "D", "E")

    for indice, questao in enumerate(questoes, start=1):
        alternativas = "\n".join(
            f"- {letras[posicao]}) {alternativa}"
            for posicao, alternativa in enumerate(questao["alternativas"])
        )
        blocos.append(
            f"""\
### Questão objetiva {indice}
{questao["pergunta"]}

{alternativas}

**Gabarito:** {questao["gabarito"]}

**Comentário:** {questao["comentario"]}"""
        )

    return "\n\n".join(blocos)


def formatar_questoes_discursivas(questoes):
    blocos = []
    for indice, questao in enumerate(questoes, start=1):
        blocos.append(
            f"""\
### Questão discursiva {indice}
{questao["enunciado"]}

**Espelho mínimo**
{formatar_analise_pratica(questao["espelho"])}"""
        )
    return "\n\n".join(blocos)


def formatar_aula_estruturada(aula):
    explicacao = "\n".join(f"- {ponto}" for ponto in aula["explicacao_didatica"])
    pegadinhas = "\n".join(f"- {pegadinha}" for pegadinha in aula["pegadinhas"])
    revisao_final = "\n".join(f"- [ ] {item}" for item in aula["revisao_final"])

    return f"""\
### Objetivo da aula
{aula["objetivo"]}

### Contexto do tema
{aula["contexto"]}

### Explicação didática
{explicacao}

### Base legal
{aula["base_legal"]}

> {AVISO_LEGISLACAO}

### Exemplo prático
{formatar_analise_pratica(aula["exemplo_pratico"])}

### Jurisprudência
{aula["jurisprudencia"]}

### Pegadinhas de prova
{pegadinhas}

### Exercícios
#### Objetivas
{formatar_questoes_objetivas(aula["exercicios"]["objetivas"])}

#### Discursivas
{formatar_questoes_discursivas(aula["exercicios"]["discursivas"])}

### Revisão final
{revisao_final}

### Tarefa para revisão espaçada
{aula["tarefa_revisao_espacada"]}"""


def formatar_revisoes_espacadas(revisoes):
    blocos = []
    for revisao in revisoes:
        perguntas = formatar_lista_numerada(revisao["perguntas_rapidas"])
        questoes_objetivas = formatar_questoes_objetivas(revisao["questoes_objetivas"])
        questao_discursiva = formatar_questoes_discursivas([revisao["questao_discursiva"]])
        blocos.append(
            f"""\
### {revisao["intervalo"]} - {revisao["data"].strftime("%d/%m/%Y")}
#### 5 perguntas rápidas
{perguntas}

#### 3 questões objetivas
{questoes_objetivas}

#### 1 questão discursiva
{questao_discursiva}

#### 1 resumo de memória
{revisao["resumo_memoria"]}"""
        )

    return "\n\n".join(blocos)


def formatar_pontos_fracos(registros):
    linhas = [
        "| Data | Disciplina | Tema | Ponto fraco | Ação recomendada | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for registro in registros:
        linhas.append(
            "| {data} | {disciplina} | {tema} | {ponto} | {acao} | {status} |".format(
                data=escapar_tabela_markdown(registro["data"]),
                disciplina=escapar_tabela_markdown(registro["disciplina"]),
                tema=escapar_tabela_markdown(registro["tema"]),
                ponto=escapar_tabela_markdown(registro["ponto_fraco"]),
                acao=escapar_tabela_markdown(registro["acao_recomendada"]),
                status=escapar_tabela_markdown(registro["status"]),
            )
        )
    return "\n".join(linhas)


def gerar_simulado(texto, tema, quantidade_objetivas=4, quantidade_discursivas=2):
    return {
        "titulo": f"Simulado de fixação - {tema}",
        "orientacao": (
            "Resolva sem consultar o material. Depois corrija pelo gabarito, registre "
            "pontos fracos e reprograme as revisões espaçadas."
        ),
        "questoes_objetivas": gerar_questoes_objetivas(
            texto, tema, quantidade=quantidade_objetivas
        ),
        "questoes_discursivas": gerar_questoes_discursivas(
            texto, tema, quantidade=quantidade_discursivas
        ),
    }


def gerar_registro_desempenho(disciplina, tema, pontos_fracos=None, gerado_em=None):
    pontos_fracos = pontos_fracos or gerar_registro_pontos_fracos(
        disciplina, tema, registrado_em=gerado_em
    )

    return {
        "disciplina": disciplina,
        "tema": tema,
        "data": data_base_para_date(gerado_em),
        "indicadores": [
            "Percentual de acertos em questões objetivas.",
            "Qualidade da resposta discursiva conforme fato, fundamento, risco e próximo passo.",
            "Reincidência de erros em revisões espaçadas.",
            "Módulos que precisam de reforço antes de avançar.",
        ],
        "pontos_fracos": pontos_fracos,
    }


def gerar_pacote_estudo(texto, nome_arquivo=None, gerado_em=None, semestre=SEMESTRE_PADRAO):
    texto_limpo = limpar_texto(texto)
    tema = titulo_por_nome_arquivo(nome_arquivo)
    data = gerado_em or datetime.now()
    disciplina = inferir_disciplina(nome_arquivo=nome_arquivo, texto=texto_limpo)
    disciplinas = gerar_disciplinas_semestre()
    plano = gerar_plano_semanal(disciplinas)
    aula = gerar_aula_estruturada(texto_limpo, tema, disciplina=disciplina)
    revisoes = gerar_revisoes_espacadas(texto_limpo, tema, data_base=data)
    questoes_objetivas = gerar_questoes_objetivas(texto_limpo, tema, quantidade=3)
    questoes_discursivas = gerar_questoes_discursivas(texto_limpo, tema, quantidade=2)
    flashcards = gerar_flashcards(texto_limpo, tema)
    checklist = gerar_checklist_estudo()
    pontos_fracos = gerar_registro_pontos_fracos(disciplina, tema, registrado_em=data)

    return {
        "projeto": NOME_PROJETO,
        "texto": texto_limpo,
        "tema": tema,
        "disciplina": disciplina,
        "semestre": semestre,
        "data": data,
        "arquitetura": gerar_arquitetura_modular(disciplinas),
        "disciplinas": disciplinas,
        "plano": plano,
        "aula": aula,
        "revisoes": revisoes,
        "questoes_objetivas": questoes_objetivas,
        "questoes_discursivas": questoes_discursivas,
        "flashcards": flashcards,
        "checklist": checklist,
        "pontos_fracos": pontos_fracos,
        "simulado": gerar_simulado(texto_limpo, tema),
        "desempenho": gerar_registro_desempenho(
            disciplina, tema, pontos_fracos=pontos_fracos, gerado_em=data
        ),
    }


def formatar_arquitetura_modular(arquitetura):
    pastas = "\n".join(
        f"- `{pasta}/`: {descricao}"
        for pasta, descricao in arquitetura["pastas"].items()
    )
    semestres = ", ".join(arquitetura["semestres"])
    return f"""\
Projeto: {arquitetura["projeto"]}

## Pastas
{pastas}

## Semestres
{semestres}"""


def formatar_simulado(simulado):
    return f"""\
## Orientação
{simulado["orientacao"]}

## Questões Objetivas
{formatar_questoes_objetivas(simulado["questoes_objetivas"])}

## Questões Discursivas
{formatar_questoes_discursivas(simulado["questoes_discursivas"])}"""


def formatar_desempenho(desempenho):
    indicadores = formatar_checklist(desempenho["indicadores"])
    return f"""\
Disciplina: {desempenho["disciplina"]}

Tema: {desempenho["tema"]}

Data de acompanhamento: {desempenho["data"].strftime("%d/%m/%Y")}

## Indicadores
{indicadores}

## Pontos Fracos
{formatar_pontos_fracos(desempenho["pontos_fracos"])}"""


def formatar_documentos_modulares(pacote):
    disciplina = pacote["disciplina"]
    tema = pacote["tema"]
    modulos = obter_modulos_disciplina(disciplina)

    return {
        "disciplina": f"""\
# {disciplina}

Projeto: {pacote["projeto"]}

## Módulos
{formatar_lista_numerada(modulos)}

## Conexão
Graduação em Direito, OAB e concursos policiais.

> {AVISO_LEGISLACAO}
""",
        "semestre": f"""\
# {pacote["semestre"].replace("_", " ").title()}

Projeto: {pacote["projeto"]}

## Arquitetura Modular
{formatar_arquitetura_modular(pacote["arquitetura"])}

## Disciplinas do Semestre
{formatar_disciplinas_semestre(pacote["disciplinas"])}
""",
        "aula": f"""\
# Aula Estruturada - {tema}

Disciplina: {disciplina}

Semestre: {pacote["semestre"]}

{formatar_aula_estruturada(pacote["aula"])}
""",
        "questoes_objetivas": f"""\
# Questões Objetivas - {tema}

Disciplina: {disciplina}

{formatar_questoes_objetivas(pacote["questoes_objetivas"])}
""",
        "questoes_discursivas": f"""\
# Questões Discursivas - {tema}

Disciplina: {disciplina}

{formatar_questoes_discursivas(pacote["questoes_discursivas"])}
""",
        "revisoes": f"""\
# Revisões Espaçadas - {tema}

Disciplina: {disciplina}

{formatar_revisoes_espacadas(pacote["revisoes"])}
""",
        "flashcards": f"""\
# Flashcards - {tema}

Disciplina: {disciplina}

{formatar_flashcards(pacote["flashcards"])}
""",
        "simulado": f"""\
# {pacote["simulado"]["titulo"]}

Disciplina: {disciplina}

{formatar_simulado(pacote["simulado"])}
""",
        "desempenho": f"""\
# Desempenho - {tema}

{formatar_desempenho(pacote["desempenho"])}
""",
        "plano_semanal": f"""\
# Plano Semanal - {disciplina}

{formatar_plano_semanal(pacote["plano"])}
""",
        "checklist": f"""\
# Checklist de Estudo - {tema}

Disciplina: {disciplina}

{formatar_checklist(pacote["checklist"])}
""",
    }


def caminhos_pacote_modular(pacote, base_dir=None):
    base = Path(base_dir) if base_dir else Path(".")
    pastas = criar_arquitetura_modular(base)
    disciplina_slug = slugificar(pacote["disciplina"])
    tema_slug = slugificar(pacote["tema"])
    semestre = pacote["semestre"]

    diretorios = {
        "disciplina": pastas["disciplinas"] / disciplina_slug,
        "semestre": pastas["semestres"] / semestre,
        "aula": pastas["aulas"] / disciplina_slug,
        "questoes_objetivas": pastas["questoes"] / "objetivas" / disciplina_slug,
        "questoes_discursivas": pastas["questoes"] / "discursivas" / disciplina_slug,
        "revisoes": pastas["revisoes"] / disciplina_slug,
        "flashcards": pastas["flashcards"] / disciplina_slug,
        "simulado": pastas["simulados"] / disciplina_slug,
        "desempenho": pastas["desempenho"] / disciplina_slug,
        "plano_semanal": pastas["planos_semanais"] / disciplina_slug,
        "checklist": pastas["planos_semanais"] / disciplina_slug,
    }

    for diretorio in diretorios.values():
        diretorio.mkdir(parents=True, exist_ok=True)

    return {
        "disciplina": diretorios["disciplina"] / "README.md",
        "semestre": diretorios["semestre"] / "README.md",
        "aula": diretorios["aula"] / f"{tema_slug}.md",
        "questoes_objetivas": diretorios["questoes_objetivas"] / f"{tema_slug}.md",
        "questoes_discursivas": diretorios["questoes_discursivas"] / f"{tema_slug}.md",
        "revisoes": diretorios["revisoes"] / f"{tema_slug}.md",
        "flashcards": diretorios["flashcards"] / f"{tema_slug}.md",
        "simulado": diretorios["simulado"] / f"{tema_slug}.md",
        "desempenho": diretorios["desempenho"] / f"{tema_slug}.md",
        "plano_semanal": diretorios["plano_semanal"] / "plano_semanal.md",
        "checklist": diretorios["checklist"] / f"{tema_slug}_checklist.md",
    }


def salvar_pacote_modular(pacote, base_dir=None):
    documentos = formatar_documentos_modulares(pacote)
    caminhos = caminhos_pacote_modular(pacote, base_dir=base_dir)

    for chave, conteudo in documentos.items():
        caminhos[chave].write_text(conteudo, encoding="utf-8")

    return caminhos


def formatar_resumo_consolidado(pacote):
    data = pacote["data"]
    resumo = f"""\
# {pacote["projeto"]}

Data: {data.strftime("%d/%m/%Y %H:%M")}

Tema: {pacote["tema"]}

Disciplina inferida: {pacote["disciplina"]}

Semestre: {pacote["semestre"]}

> {AVISO_LEGISLACAO}

## 1. Arquitetura Modular

{formatar_arquitetura_modular(pacote["arquitetura"])}

## 2. Disciplinas do Semestre

{formatar_disciplinas_semestre(pacote["disciplinas"])}

## 3. Plano Semanal

{formatar_plano_semanal(pacote["plano"])}

## 4. Aula Estruturada

{formatar_aula_estruturada(pacote["aula"])}

## 5. Questões Objetivas

{formatar_questoes_objetivas(pacote["questoes_objetivas"])}

## 6. Questões Discursivas

{formatar_questoes_discursivas(pacote["questoes_discursivas"])}

## 7. Revisões Espaçadas

{formatar_revisoes_espacadas(pacote["revisoes"])}

## 8. Flashcards

{formatar_flashcards(pacote["flashcards"])}

## 9. Simulado

{pacote["simulado"]["titulo"]}

{formatar_simulado(pacote["simulado"])}

## 10. Desempenho

{formatar_desempenho(pacote["desempenho"])}

## 11. Checklist de Estudo

{formatar_checklist(pacote["checklist"])}

## 12. Texto Analisado

{pacote["texto"]}
"""
    return resumo


def gerar_resumo(texto, nome_arquivo=None, gerado_em=None):
    pacote = gerar_pacote_estudo(texto, nome_arquivo=nome_arquivo, gerado_em=gerado_em)
    return formatar_resumo_consolidado(pacote)


def listar_arquivos_txt(pasta_entrada):
    if not pasta_entrada.exists():
        return []

    return sorted(pasta_entrada.glob("*.txt"))


def processar_arquivo(arquivo, pasta_saida):
    texto = arquivo.read_text(encoding="utf-8-sig")
    pacote = gerar_pacote_estudo(texto, nome_arquivo=arquivo.stem)
    resultado = formatar_resumo_consolidado(pacote)

    pasta_saida.mkdir(parents=True, exist_ok=True)
    saida = pasta_saida / f"resumo_{arquivo.stem}.md"
    saida.write_text(resultado, encoding="utf-8")
    salvar_pacote_modular(pacote, base_dir=pasta_saida.parent)

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
        print(f"Material de aula gerado: {saida}")


if __name__ == "__main__":
    main()
