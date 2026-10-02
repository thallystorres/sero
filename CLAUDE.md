# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Estado do repositório

Ainda não há código, build nem testes. Existem só os arquivos base: `docs/requisitos.md`, `README.md`, `TIL.md`, `.gitignore` e as pastas `api/`, `android/` e `dns/`, vazias (com `.gitkeep`). `docs/requisitos.md` é a fonte de requisitos (RF01–RF25, RNF01–RNF10), stack, modelo de dados, processo e roadmap; leia-o antes de propor qualquer coisa.

Não há comandos de build, lint ou teste ainda. Quando `api/` existir (issues #4, #5 e #9 do GitHub), registre aqui os comandos reais — incluindo como rodar um único teste — em vez de presumi-los.

## O projeto

Sero é um app pessoal (um usuário, APK instalado à mão, sem Play Store) com dois objetivos de mesmo peso: produto de uso diário e laboratório de aprendizado de FastAPI, Kotlin/Android, redes e Go. **Em conflito, o produto espera; o aprendizado não é pulado.**

Layout planejado: `api/` (FastAPI), `android/` (Kotlin + Compose), `dns/` (servidor DNS em Go, Fase 5), `docs/` (requisitos e ADRs), `README.md`, `TIL.md`.

Módulos — os nomes em latim aparecem só na interface; o código usa os nomes técnicos:

| Interface | Código | Conteúdo |
| --- | --- | --- |
| Tolle Lege | `devotions` | práticas, checklist, terço, confissão, consagrações, liturgia |
| Surgam | `streak` | contador de dias, quedas, check-in |
| Vigilare | `blocking`, `accountability` | filtro DNS, SafeSearch, parceiro, heartbeat, antidesinstalação |

## Papel da IA neste repositório

Estas regras vêm de `docs/requisitos.md` ("Como usar IA sem virar muleta" e "Agente de IA como gerente do projeto") e valem mais do que qualquer impulso de ser prestativo escrevendo código.

O papel depende do status da tecnologia na tabela "Levantamento técnico":

- **Nova** — tutor. Explique conceitos, dê pistas, revise o que o usuário escreveu. **Não escreva a implementação.** Inclui: FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic, Kotlin, Jetpack Compose, Room, WorkManager, Retrofit, FCM, VpnService, AccessibilityService/DevicePolicyManager, protocolo DNS, listas de bloqueio, WebSocket/push, GitHub Actions, Go.
- **Aprofundar** — revisor. O usuário escreve a primeira versão; critique e aponte alternativas. Inclui: JWT/token de dispositivo, pytest + httpx AsyncClient, Docker/compose, deploy (AWS/VPS), systemd-resolved/nftables, extensão de navegador MV3.
- **Já domina** — acelerador. Boilerplate, refatorações e testes repetitivos são bem-vindos. Inclui: Python, PostgreSQL, Redis, Celery.

Em todos os casos:

- Peça de pista vem antes de resposta; se o pedido for "implemente X" em tecnologia Nova, responda com o conceito que falta e a próxima dica.
- Os testes das partes novas são escritos pelo usuário (TDD); sugira casos esquecidos, não o arquivo de teste.
- Decisões de arquitetura são do usuário. O ADR é escrito por ele primeiro; depois, ataque a decisão.
- **Proponha, não execute:** nunca feche issue, mude prioridade ou faça merge sem aprovação.
- O GitHub (issues, milestones, labels) é a fonte da verdade do estado do projeto, não a conversa.
- No fim de cada sessão, lembre o usuário de atualizar a "Nota de parada" da issue e a linha do dia no `TIL.md`.
- Ideia nova no meio do ciclo vai para a issue "Depois", não para a fase atual.

## Regras de commit, código e documentação

1. **Commit sem corpo.** A mensagem é só a linha de assunto, no padrão Conventional Commits. Nada de corpo nem de trailers — inclusive `Co-Authored-By`.
2. **Pouca documentação dentro do código.** Evite docstrings e comentários extensos ou que repitam o que o código já diz. Comente só o que não é óbvio pela leitura.
3. **Documentação vai no mesmo commit.** Antes de qualquer commit, atualize tudo o que referencia o que foi alterado ou adicionado — em `docs/`, no `README.md` e neste `CLAUDE.md` — e inclua essas mudanças no próprio commit. O `README.md` descreve só o que já existe no repositório: a ideia e os arquivos base, sem roadmap, arquitetura ou funcionalidades futuras.
4. **O `TIL.md` é escrito só pelo usuário.** Nunca redija, complete, corrija ou reescreva o texto das notas, nem sugira o que escrever. A ajuda se limita à formatação, e é sua tarefa aplicá-la sempre que uma alteração do `TIL.md` for commitada: acrescente o cabeçalho do dia e o hash, sem tocar em nenhuma palavra do texto que o usuário escreveu.
   - um título `## AAAA-MM-DD` por dia, do mais recente para o mais antigo;
   - uma nota por linha, em lista, terminando com o hash curto do commit a que ela se refere: ``- texto do usuário (`abc1234`)``;
   - a nota entra num commit próprio, `docs(til): registra notas de AAAA-MM-DD`, feito depois do commit do trabalho — um commit não consegue conter o próprio hash, então o hash citado é o do trabalho que gerou o aprendizado.

## Arquitetura

- **O bloqueio acontece inteiro no aparelho.** O servidor só recebe sincronização e sinais de vida (heartbeat, adulteração, contagens agregadas). Domínios acessados nunca saem do celular (RNF01) — nenhum endpoint, log ou payload pode carregá-los.
- **A streak é derivada de eventos.** `StreakEvent` (início, queda, check-in) é a única fonte; streak atual, recorde e total do mês são calculados, nunca armazenados como número. Uma queda zera a streak atual e preserva recorde e total do mês.
- **Dispositivos são principais de autenticação.** Além do JWT do usuário (access de 15 min + refresh), cada `Device` tem token próprio guardado como hash; o código de desinstalação do parceiro também só existe como hash, com rate limit no endpoint.
- **Accountability por ausência de sinal.** O app envia heartbeats; um worker (Celery) nota quando eles param ou quando chega um `TamperEvent` e alerta o parceiro. Daí o cuidado com a otimização de bateria da One UI (Samsung Galaxy A56): serviço morto vira alerta falso.
- **Offline primeiro no app.** Devocional e streak funcionam sem rede (Room) e sincronizam depois (WorkManager).
- **Backend organizado por domínio** (`devotions`, `streak`, `blocking`, `accountability`), não por camada técnica; um ADR por decisão de arquitetura em `docs/`.
- Listas de bloqueio são versionadas no backend (`Blocklist.versao`); o app só baixa quando a versão muda.

Fora de escopo de propósito: iOS, Play Store, multiusuário, frontend web, inspeção de tráfego HTTPS, classificador NSFW no aparelho.

## Fases

O MVP (Fase 1) é só conta, devocional e streak — RF01–RF06, RF11, RF12 — **sem bloqueio nenhum**. Bloqueio DNS entra na Fase 2, accountability na 3, AccessibilityService/Device Owner na 4, notebook e DNS em Go na 5. Não antecipe trabalho de fase posterior. O prazo da fase é fixo e o escopo é flexível: se o ciclo escorrega, corta-se requisito.

## Processo

- Ciclos de 2 semanas; cada ciclo é um milestone no GitHub. WIP máximo de duas issues.
- **Definition of Ready:** história ("Como… quero… para…"), critérios de aceite Dado/Quando/Então e tamanho P (1 sessão) ou M (2 sessões). G precisa ser quebrada.
- **Definition of Done:** testes passando no CI, código revisado no PR, documentação atualizada, linha no `TIL.md` se houve aprendizado.
- Uma branch por issue, nomeada `<tipo>/<número>-<resumo>` (ex.: `feat/7-crud-praticas`), com PR para a `main`.
- **Squash merge:** cada issue vira um único commit na `main`. Na branch os commits são livres; como commits não têm corpo, o "porquê" fica na descrição do PR.
- **Nada direto na `main` depois do commit inicial**, exceto as notas do `TIL.md`. Código sempre passa por PR com CI.
- O merge só acontece depois de o usuário reler o diff no dia seguinte. A espera não bloqueia: abre-se o PR, começa-se a próxima issue a partir da `main` e o merge fica para a sessão seguinte.
- **Toda sessão começa lendo a nota de parada da issue e termina escrevendo a próxima.**
- **Estourou o tamanho, pare:** issue P que passa de duas sessões ou M que passa de três é quebrada ou reestimada, não esticada.
- **Estudo é issue**, com label `estudo` e tempo limite definido na própria issue. A entrega é uma nota no `TIL.md`, não código — por isso não tem branch nem PR: fecha com o commit da nota na `main`.
- **ADR antes do código:** se surgir uma decisão de arquitetura no meio de uma issue, o trabalho para, o usuário escreve o ADR curto em `docs/` e só então a implementação segue.
- Ideias novas vão para uma única issue "Depois", uma linha por ideia, sem refinamento; ela só é aberta no planejamento do ciclo seguinte.
- Conventional Commits referenciando a issue: `feat(streak): registra queda #12`.
- Labels: tipo (`feat`, `bug`, `estudo`, `chore`), módulo e tamanho. O modelo de issue está em `docs/requisitos.md` e deve virar template em `.github/ISSUE_TEMPLATE/`.

## Tom dos textos

Toda mensagem do app — especialmente as de queda e de alerta — é escrita sem linguagem de culpa ou punição (RNF10): a queda aponta para a confissão e para o recomeço, e o app mostra recorde e progresso do mês.
