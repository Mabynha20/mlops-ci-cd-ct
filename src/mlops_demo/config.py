"""Configuração central do projeto: caminhos, nomes de colunas e limiares de qualidade.

Problema: filtro de spam (dataset Spambase, UCI). Cada linha é um e-mail descrito por 57
atributos numéricos (frequência de palavras e caracteres e sequências de letras maiúsculas).
"""

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]

# dados
DADOS_BRUTOS = RAIZ / "data" / "raw"
DADOS_LOTES = DADOS_BRUTOS / "lotes"
DADOS_PROCESSADOS = RAIZ / "data" / "processed"
BASE_TREINO = DADOS_BRUTOS / "base_treino.csv"
BASE_HOLDOUT = DADOS_BRUTOS / "base_holdout.csv"
TREINO_PROCESSADO = DADOS_PROCESSADOS / "treino.csv"
AVALIACAO_PROCESSADA = DADOS_PROCESSADOS / "avaliacao.csv"

# modelos e relatórios
MODELO_CAMPEAO = RAIZ / "models" / "champion" / "model.joblib"
METRICAS_CAMPEAO = RAIZ / "models" / "champion" / "metrics.json"
MODELO_CANDIDATO = RAIZ / "models" / "candidate" / "model.joblib"
METRICAS_CANDIDATO = RAIZ / "reports" / "candidate_metrics.json"
RELATORIO_GATE = RAIZ / "reports" / "gate.json"
RESUMO_GATE = RAIZ / "reports" / "gate.md"
RELATORIO_DRIFT = RAIZ / "reports" / "drift.md"
PARAMS = RAIZ / "params.yaml"

# ---------------------------------------------------------------------------------------------
# esquema dos dados (contrato com data/raw/*.csv: mesmas colunas, nesta ordem)
# ---------------------------------------------------------------------------------------------

# 48 atributos: % de palavras do e-mail iguais à palavra (0 a 100)
PALAVRAS = [
    "make", "address", "all", "3d", "our", "over", "remove", "internet",
    "order", "mail", "receive", "will", "people", "report", "addresses", "free",
    "business", "email", "you", "credit", "your", "font", "000", "money",
    "hp", "hpl", "george", "650", "lab", "labs", "telnet", "857",
    "data", "415", "85", "technology", "1999", "parts", "pm", "direct",
    "cs", "meeting", "original", "project", "re", "edu", "table", "conference",
]  # fmt: skip
COLUNAS_PALAVRAS = [f"word_freq_{p}" for p in PALAVRAS]

# 6 atributos: % de caracteres do e-mail iguais ao caractere (0 a 100).
# No arquivo original os nomes têm o próprio símbolo (char_freq_!); aqui usamos o nome por extenso.
CARACTERES = ["semicolon", "parenthesis", "bracket", "exclamation", "dollar", "hash"]
COLUNAS_CARACTERES = [f"char_freq_{c}" for c in CARACTERES]

# 3 atributos: sequências ininterruptas de letras maiúsculas (média, maior e total; todos >= 1)
COLUNAS_MAIUSCULAS = [
    "capital_run_length_average",
    "capital_run_length_longest",
    "capital_run_length_total",
]

FEATURES = [*COLUNAS_PALAVRAS, *COLUNAS_CARACTERES, *COLUNAS_MAIUSCULAS]  # 57 atributos
N_FEATURES = len(FEATURES)
ALVO = "spam"

# classe positiva: SPAM (1). Legítimo ("ham") é 0.
CLASSE_POSITIVA = 1
CLASSE_NEGATIVA = 0
NOME_CLASSE = {CLASSE_POSITIVA: "spam", CLASSE_NEGATIVA: "legitimo"}

# Sinais típicos de spam (coeficiente positivo na regressão logística: mais deles, mais spam).
# Usados para simular drift (campanha de spam nova) e no teste direcional do modelo.
COLUNAS_SINAL_SPAM = [
    "word_freq_remove",
    "word_freq_free",
    "word_freq_000",
    "word_freq_money",
    "char_freq_exclamation",
    "char_freq_dollar",
    "capital_run_length_longest",
    "capital_run_length_total",
]

# Nomes antigos (projeto de câncer de mama), mantidos só até os outros módulos serem adaptados.
# TODO: apagar quando data.py, evaluate.py, api.py e os testes usarem os nomes novos.
CLASSE_MALIGNA = CLASSE_POSITIVA
COLUNAS_TAMANHO = COLUNAS_SINAL_SPAM

# ---------------------------------------------------------------------------------------------
# contrato de qualidade do modelo. Mudar aqui exige revisão em PR (justificativa no ADAPTACAO.md).
# ---------------------------------------------------------------------------------------------
# O erro mais caro é o FALSO POSITIVO: um e-mail legítimo (boleto, proposta, resposta de cliente)
# vai para a pasta de spam e ninguém lê. O falso negativo (spam na caixa de entrada) só incomoda.
# Por isso a métrica principal é a PRECISÃO da classe spam, e o recall é só um piso.

# nomes das métricas no dicionário devolvido por evaluate.calcular_metricas
METRICA_PRINCIPAL = "precisao_spam"
METRICA_SECUNDARIA = "recall_spam"

PRECISAO_MINIMA = 0.90  # no máximo 1 em cada 10 e-mails marcados como spam é legítimo
RECALL_MINIMO = 0.80  # o filtro tem que pegar pelo menos 4 de cada 5 spams (senão é inútil)
TOLERANCIA_CAMPEAO = 0.0  # o candidato não pode ter PRECISÃO menor que a do campeão
PISO_SANIDADE = 0.75  # o campeão não pode colapsar na base de referência (holdout fixo)

# monitoramento de drift
LIMITE_DRIFT_P = 0.01  # p-valor do teste KS
MIN_FEATURES_DRIFT = 3  # gatilho do CT: quantos atributos com drift disparam o retreino


def carregar_params() -> dict:
    """Lê o params.yaml (hiperparâmetros e semente)."""
    with open(PARAMS, encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)
