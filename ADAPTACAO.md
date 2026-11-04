# Adaptação do projeto de CI/CD/CT: filtro de spam

## 1. Problema e dados

_(Ruan)_

## 2. Contrato de qualidade

**Problema.** Classificar e-mails como **spam (1)** ou **legítimo (0)** a partir de 57 atributos numéricos
(frequência de palavras e caracteres e sequências de letras maiúsculas). O modelo serviria a um provedor de
e-mail ou a um servidor corporativo que decide se a mensagem vai para a caixa de entrada ou para a pasta de spam.

**Classe positiva:** spam (`CLASSE_POSITIVA = 1` em `src/mlops_demo/config.py`).

**Erro mais caro: falso positivo.** Um e-mail legítimo marcado como spam (um boleto, uma proposta, a resposta de
um cliente) some da caixa de entrada e quase ninguém confere a pasta de spam. O prejuízo é real e silencioso.
O falso negativo (um spam que passa) só incomoda: o usuário vê, apaga e segue. É o contrário do projeto
original, em que perder um tumor maligno (falso negativo) era o pior erro.

**Métrica principal: precisão da classe spam.** Ela responde à pergunta "dos e-mails que o filtro mandou para
o spam, quantos eram mesmo spam?", que é exatamente o erro que queremos evitar.

| Regra do portão | Limiar | Justificativa |
|---|---|---|
| Precisão de spam do candidato | **>= 0,90** | no máximo 1 em cada 10 e-mails enviados para o spam pode ser legítimo |
| Recall de spam do candidato | **>= 0,80** | piso: sem ele, um modelo que quase nunca marca spam teria precisão alta e seria inútil |
| Precisão do candidato x campeão | **sem queda** (`TOLERANCIA_CAMPEAO = 0`) | medida no mesmo conjunto; um modelo novo não pode jogar mais e-mails legítimos no spam |
| Sanidade do campeão no holdout fixo | **>= 0,75** nas duas métricas | detecta um artefato quebrado ou que colapsou, não mede qualidade |

**Por que esses valores.** A precisão foi colocada acima do recall porque o custo do falso positivo é maior.
O recall de 0,80 é mais baixo de propósito: deixar passar 1 em cada 5 spams é tolerável, mas abaixo disso o filtro
deixa de cumprir sua função. Antes de fixar os números, conferimos que eles são alcançáveis: com regressão
logística, em 5 divisões estratificadas (75/25) da base sem duplicatas, a precisão de spam ficou entre 0,90 e 0,94
e o recall entre 0,88 e 0,92. Um limiar de precisão de 0,95 reprovaria qualquer modelo linear nessa base, e um de
0,85 aceitaria modelos que mandam 15% de e-mails bons para o spam. Com 0,90 o contrato é exigente, mas cumprível.

**Onde o contrato mora no código.** Os limiares e os nomes das métricas (`METRICA_PRINCIPAL = "precisao_spam"`,
`METRICA_SECUNDARIA = "recall_spam"`) ficam em `config.py`. O `gate.py` lê tudo de lá; mudar o contrato exige
um PR revisado nesse arquivo.

## 3. O que mudou, arquivo por arquivo

_(Rafael)_

- `src/mlops_demo/config.py`: esquema do Spambase (57 atributos, alvo `spam`), classe positiva 1, colunas de sinal
  de spam (`COLUNAS_SINAL_SPAM`, antigo `COLUNAS_TAMANHO`) e novos limiares do contrato.
- `src/mlops_demo/gate.py`: regras e tabela do portão passam a usar precisão e recall de spam; a comparação com o
  campeão passou do recall para a precisão.

## 4. Evidências

| Evidência | Link |
|---|---|
| E1. CI verde na `main` | |
| E2. CI vermelho por falha controlada | |
| E3. CT com drift e portão aprovando | |
| E4. CT com portão reprovando | |
| E5. CD verde com tag | |

## 5. Limites e riscos

_(Roger e Erica)_

## 6. Contribuição de cada integrante

- **Amabilly:** criação do repositório e configuração do GitHub Actions, contrato de qualidade (`config.py` e
  `gate.py`), campeão inicial e evidência E1.
