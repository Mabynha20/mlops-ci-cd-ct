# Tarefas do grupo: adaptação para o filtro de spam

Entrega: **25/11**. Repositório: https://github.com/Mabynha20/mlops-ci-cd-ct

Dataset escolhido: **Spambase (UCI)**. Contrato (já está em `src/mlops_demo/config.py`, PR #1):

- classe positiva: **spam (1)**; legítimo é 0;
- erro mais caro: **falso positivo** (e-mail bom indo para o spam);
- métrica principal: **precisão de spam >= 0,90**; piso de **recall de spam >= 0,80**.

## Antes de começar (todos)

1. Aceitem o convite do repositório em https://github.com/Mabynha20/mlops-ci-cd-ct/invitations (expira em 7 dias).
2. Clonem e preparem o ambiente:

   ```bash
   git clone https://github.com/Mabynha20/mlops-ci-cd-ct.git
   cd mlops-ci-cd-ct
   python -m venv .venv
   source .venv/Scripts/activate      # PowerShell: .venv\Scripts\Activate.ps1
   pip install -e ".[dev,ct]"
   ```

3. Configurem o Git **só nesta pasta**, com o e-mail da sua conta do GitHub (senão o commit não conta para você):

   ```bash
   git config user.name "Seu Nome"
   git config user.email "seu-email-do-github@exemplo.com"
   ```

4. Trabalhem **a partir da branch `adaptacao/contrato-spambase`** (PR #1), que já tem o `config.py` novo:

   ```bash
   git checkout adaptacao/contrato-spambase
   git checkout -b adaptacao/<sua-parte>
   ```

5. Rodem `python demo/local.py ci` antes de cada push e abram um **Pull Request** para a `main`.
   Não façam push direto na `main`. **Nenhum token ou senha no repositório.**

### Combinados técnicos (para tudo se encaixar)

- As colunas dos CSVs são exatamente `config.FEATURES`, na mesma ordem. Os símbolos ficam por extenso
  (`char_freq_exclamation`, `char_freq_dollar`...), e o alvo se chama `spam`.
- `evaluate.calcular_metricas` devolve as chaves `precisao_spam` e `recall_spam` (o `gate.py` lê essas chaves).
- Colunas de drift e do teste direcional: `config.COLUNAS_SINAL_SPAM` (mais delas, mais spam).
- `CLASSE_MALIGNA` e `COLUNAS_TAMANHO` são apelidos temporários. Usem `CLASSE_POSITIVA` e `COLUNAS_SINAL_SPAM`.

---

## Amabilly: infraestrutura e contrato

- [x] Parte B: repositório público sem fork, primeiro commit, permissões do Actions, `PROMOCAO_AUTOMATICA=false`, primeiro CI verde.
- [x] Etapa 3: `config.py` (FEATURES, ALVO, classe positiva, colunas de sinal, limiares) e `gate.py`.
- [x] Relatório, seção 2 (contrato de qualidade).
- [x] Convites de colaborador para todos.
- [ ] Etapa 11: gerar o campeão inicial com `python -m mlops_demo.train --campeao`, **depois** que dados, modelo, API e testes estiverem na `main`.
- [ ] E1: CI verde na `main` com os três jobs, depois da adaptação.

## Ruan: dados (prioridade: destrava todo mundo)

- [ ] Etapa 1: `data/raw/base_treino.csv` e `data/raw/base_holdout.csv` com o Spambase, **sem sobreposição**. Remover as **391 linhas duplicadas** antes de dividir. Deixar `data/raw/lotes/` vazia.
- [ ] Etapa 2: tirar o `load_breast_cancer` de `dividir_dataset` e `criar_base` em `data.py`. Se houver script de geração, usar semente fixa.
- [ ] Etapa 4: `validar_dataframe` com regras do domínio. Exemplos: frequências entre 0 e 100, `capital_run_length_*` >= 1, alvo só 0 ou 1, sem nulos, tipos numéricos.
- [ ] Testes: adaptar `tests/test_dados.py` e criar **1 teste novo** da camada de dados.
- [ ] Relatório, seção 1: problema, fonte, licença (CC BY 4.0, conferir na página da UCI) e tamanho do dataset.

## Roger: modelo e métricas

- [ ] Etapa 5: `features.py`, `train.py` e `params.yaml`. Com StandardScaler e LR balanceada a precisão fica no limite (~0,90); `log1p` antes do scaler leva a ~0,91 a 0,94.
- [ ] Etapa 6: `evaluate.py` com `pos_label=1` e as chaves `precisao_spam` e `recall_spam`.
- [ ] Testes: adaptar `tests/test_modelo.py`, ajustar o **teste direcional** (aumentar as colunas de sinal de spam deve aumentar a probabilidade de spam) e criar **1 teste novo**.
- [ ] E4: CT com o portão **reprovando** (recall alto e precisão baixa) e o campeão sem mudar.
- [ ] Relatório, seção 5: por que o portão sozinho não garante um bom modelo.

## Erica: drift e CT

- [ ] Etapa 7: `aplicar_drift` em `data.py` usando `COLUNAS_SINAL_SPAM` (simular uma campanha de spam nova), `monitor.py` e ajuste de `MIN_FEATURES_DRIFT` em `config.py`.
- [ ] Testes: adaptar `tests/test_codigo.py` (os testes do portão ainda usam as chaves antigas) e criar **1 teste novo**.
- [ ] E3: lote com drift em `data/raw/lotes/` enviado **por PR**. O Summary do CT deve mostrar o drift e a tabela do portão aprovando.
- [ ] Relatório, seção 5: o que monitoraríamos em produção.

## Herbe: API e CD

- [ ] Etapa 8: `api.py` e `demo/smoke_test.py`. Trocar o tamanho fixo **30** por `N_FEATURES` (57) e adaptar o schema, as mensagens e as respostas (spam / legítimo).
- [ ] Testes: adaptar `tests/test_api.py` e criar **1 teste novo**.
- [ ] E5: tag `v1.0.0`, CD verde, imagem publicada no ghcr.io e visibilidade do pacote mudada para **Public**. Testar com:

  ```bash
  docker run -p 8000:8000 ghcr.io/mabynha20/mlops-ci-cd-ct:1.0.0
  python demo/smoke_test.py http://localhost:8000
  ```

- [ ] Print ou URL da página de Packages para o D2L.

## Rafael: cenários, documentação e entrega

- [ ] Etapa 10: reescrever os cenários 1 a 5 em `demo/cenarios.py` com as colunas do Spambase.
- [ ] E2: branch com um bug controlado (usando um cenário adaptado) e PR mostrando o step vermelho.
- [ ] Etapa 12: atualizar o `README.md` para o filtro de spam.
- [ ] Relatório, seção 3 (o que mudou, arquivo por arquivo), montagem final do `ADAPTACAO.md` e envio no D2L.
- [ ] Opcional (+5): promoção automática (`PROMOCAO_AUTOMATICA=true`, `main` sem proteção), com vantagens e riscos no relatório.

## Todos

- [ ] Colar o link da própria evidência na seção 4 do `ADAPTACAO.md`.
- [ ] Escrever a própria linha na seção 6 (contribuição e, se houver, uso de IA).
- [ ] Ter commits próprios no histórico (entra na avaliação).

---

## Cronograma

| Período | O quê | Quem |
|---|---|---|
| até 12/11 | Dados e validação (destrava o resto) | Ruan |
| 12 a 17/11 | Modelo, drift, API e cenários em paralelo, cada um na sua branch | Roger, Erica, Herbe e Rafael |
| 17 a 19/11 | Testes novos, merge na `main`, campeão inicial e CI verde (E1) | Todos; Amabilly fecha o E1 |
| 19 a 23/11 | Evidências E2 a E5 | Rafael, Erica, Roger e Herbe |
| 24/11 | Revisão do relatório | Todos |
| 25/11 | Entrega no D2L | Rafael |

**Ordem das evidências:** E1 primeiro (base verde). E3 e E4 dependem do campeão inicial na `main`. E5 pode
sair logo depois do E1.
