# Sero — Requisitos, Stack e Plano

Oct 2, 2026 · @Thallys

## Visão geral

O projeto tem dois objetivos com o mesmo peso: um produto que você usa todo dia e um laboratório para aprender FastAPI, Kotlin/Android, redes e Go. Quando os dois entrarem em conflito, o produto pode esperar; o aprendizado não deve ser pulado.

**O produto** organiza seus deveres devocionais (terço, consagrações, liturgia diária, confissão) e acompanha uma streak de dias sem conteúdo adulto. Ele também bloqueia conteúdo adulto e anúncios no celular e no notebook, e torna difícil desativar esse bloqueio.

**Nome e módulos.** O app se chama **Sero**, de "Sero te amavi" ("tarde te amei"), de Santo Agostinho nas *Confissões* (X, 27): nunca é tarde para recomeçar.

| Módulo | Nome | Origem | Nome no código |
| --- | --- | --- | --- |
| Devocional | Tolle Lege | "Toma e lê", a conversão de Agostinho (*Confissões* VIII, 12) | `devotions` |
| Streak e recomeço | Surgam | "Levantar-me-ei e irei a meu pai" (Lc 15,18) | `streak` |
| Bloqueio e accountability | Vigilare | "Vigiar", de "vigiai e orai" (Mt 26,41) | `blocking`, `accountability` |

Os nomes em latim aparecem só na interface; o código usa os nomes técnicos, para o repositório ser lido sem dicionário.

**Princípios de design**

- **Fricção + prestação de contas, não tranca absoluta.** Nenhum bloqueio resiste a quem controla o aparelho; o objetivo é vencer o impulso e envolver uma pessoa de confiança.
- **Misericórdia, não punição.** Uma queda reinicia a contagem, mas o app mostra recorde e progresso do mês e aponta para a confissão, não para a culpa.
- **Privacidade por padrão.** Os sites que você acessa são filtrados no próprio aparelho e nunca vão para o servidor.
- **Uso pessoal.** Um usuário, instalação via APK, sem Play Store.

**Plataformas:** celular Android (Samsung Galaxy A56) e notebook (Windows e Linux).

**Ponto de atenção no Samsung:** a One UI encerra serviços em segundo plano de forma agressiva para economizar bateria. O app precisa ficar fora da otimização de bateria (lista de apps que nunca entram em suspensão), senão o VpnService e o heartbeat caem e geram alertas falsos ao parceiro. Teste isso cedo, já na Fase 2.

## Requisitos funcionais

São 25 requisitos em cinco módulos; a coluna Fase liga cada um ao roadmap do fim do documento. O MVP (Fase 1) é só conta, devocional e streak, sem bloqueio.

**Conta e dispositivos**

| ID | Requisito | Fase |
| --- | --- | --- |
| RF01 | Login com um usuário e vários dispositivos registrados (celular, notebook) | Fase 1 |

**Devocional (Tolle Lege)**

| ID | Requisito | Fase |
| --- | --- | --- |
| RF02 | Cadastrar práticas com recorrência: diária, dias da semana, semanal ou mensal | Fase 1 |
| RF03 | Checklist do dia: marcar cada prática como feita | Fase 1 |
| RF04 | Terço guiado com os mistérios do dia da semana e contador de dezenas | Fase 1 |
| RF05 | Lembretes por notificação, com horário por prática | Fase 1 |
| RF06 | Confissão: registrar a data da última e lembrar após um intervalo configurável | Fase 1 |
| RF07 | Consagrações com duração (ex.: 33 dias), dia atual e retomada se perder um dia | Fase 2 |
| RF08 | Liturgia diária: leituras do dia com cache no backend | Fase 2 |
| RF09 | Exame de consciência antes da confissão | Fase 2 |
| RF10 | Calendário de constância com o histórico das práticas | Fase 2 |

**Streak e recomeço (Surgam)**

| ID | Requisito | Fase |
| --- | --- | --- |
| RF11 | Contador de dias sem conteúdo adulto, com data de início configurável | Fase 1 |
| RF12 | Registrar queda: zera a streak atual, mantém o recorde e o total de dias do mês, sugere confissão | Fase 1 |
| RF13 | Check-in diário opcional para reforçar o compromisso | Fase 2 |

**Bloqueio (Vigilare)**

| ID | Requisito | Fase |
| --- | --- | --- |
| RF14 | Filtro DNS local (VpnService) com listas de conteúdo adulto e anúncios | Fase 2 |
| RF15 | SafeSearch forçado em Google, YouTube, Bing e DuckDuckGo | Fase 2 |
| RF16 | Sincronizar listas de bloqueio do backend, mais uma lista pessoal | Fase 2 |
| RF17 | Bloquear servidores de DNS-over-HTTPS conhecidos, que burlariam o filtro | Fase 2 |
| RF18 | AccessibilityService: detectar palavras-chave em URLs e dentro de apps e fechar a tela | Fase 4 |
| RF19 | Bloqueio no notebook: DNS do sistema, hosts e extensão de navegador própria | Fase 5 |
| RF20 | Servidor DNS filtrante próprio em Go para a rede de casa | Fase 5 |

**Accountability e antidesinstalação (Vigilare)**

| ID | Requisito | Fase |
| --- | --- | --- |
| RF21 | Cadastrar parceiro de accountability (e-mail ou push) | Fase 3 |
| RF22 | Heartbeat do dispositivo; alerta ao parceiro após algumas horas sem sinal | Fase 3 |
| RF23 | Detectar VPN ou admin desativados e alertar o parceiro | Fase 3 |
| RF24 | Pausar ou desinstalar exige código do parceiro ou espera de 24–48h | Fase 3 |
| RF25 | Device Owner para impedir a desinstalação comum | Fase 4 |

## Requisitos não funcionais

As metas abaixo são pontos de partida para você medir, não números validados; ajuste depois dos primeiros testes reais.

| ID | Categoria | Requisito | Meta inicial |
| --- | --- | --- | --- |
| RNF01 | Privacidade | Domínios acessados são filtrados no aparelho e nunca enviados ao servidor | Servidor recebe só eventos (heartbeat, adulteração, contagem agregada) |
| RNF02 | Desempenho | O filtro DNS não pode deixar a navegação perceptivelmente lenta | < 20 ms de latência extra no p95 |
| RNF03 | Bateria | O VpnService roda o dia todo sem drenar a bateria | < 5% de consumo por dia atribuído ao app |
| RNF04 | Offline | Devocional e streak funcionam sem internet e sincronizam depois | 100% das telas do MVP utilizáveis offline |
| RNF05 | Segurança | JWT com access curto e refresh; token próprio por dispositivo; código de desinstalação guardado só como hash | Access de 15 min; rate limit no endpoint do código |
| RNF06 | Resiliência | O filtro volta sozinho após reiniciar o aparelho ou o app ser morto pelo sistema | Religado em < 1 min após o boot |
| RNF07 | Testabilidade | Backend com testes automatizados; parser DNS e regras de streak com testes unitários | ≥ 80% de cobertura no backend |
| RNF08 | Manutenibilidade | Backend organizado por domínio; decisões registradas em ADRs | Um ADR por decisão de arquitetura |
| RNF09 | Custo | Infraestrutura barata para uso pessoal | Free tier ou o menor VPS disponível |
| RNF10 | Tom | Textos do app sem linguagem de culpa ou punição | Revisar toda mensagem de queda e de alerta |

## Escopo

O MVP não bloqueia nada: ele entrega o devocional e a streak funcionando no seu celular, para você aprender FastAPI e Kotlin num terreno seguro antes de mexer em rede e sistema.

**Entra no MVP (Fase 1):** RF01–RF06, RF11 e RF12. API em FastAPI publicada, app Android instalado no seu celular, dados sincronizando.

**Entra depois (Fases 2–5):** todo o bloqueio, accountability, consagrações, liturgia e desktop, na ordem do roadmap.

**Fora de escopo, de propósito:**

- iOS e publicação na Play Store.
- Vários usuários, cadastro público ou monetização.
- Frontend web: o único cliente é o app Android (e, na Fase 5, o notebook).
- Classificador de imagens NSFW no aparelho: fica como desafio opcional depois da Fase 5.
- Inspecionar tráfego HTTPS: é invasivo, frágil e desnecessário com DNS + Accessibility.

Se surgir uma ideia nova no meio do caminho, ela vai para uma lista de "depois" e não entra na fase atual. É o que mais mata projetos pessoais.

## Levantamento técnico

Das 27 tecnologias do projeto, 16 são novas para você, 5 são para aprofundar, 4 você já domina e 2 ficam a confirmar. A carga nova se concentra no Android e em redes; o backend troca só o framework e o ORM, mantendo Python, Postgres, Redis e Celery.

| Camada | Tecnologia | Para quê | Aparece na | Status |
| --- | --- | --- | --- | --- |
| Backend | Python | Linguagem de toda a API | Fase 1 | Já domina |
| Backend | FastAPI | Framework da API, rotas e injeção de dependências | Fase 1 | Nova |
| Backend | Pydantic v2 | Schemas de entrada e saída, validação, configurações | Fase 1 | Nova |
| Backend | SQLAlchemy 2.0 (async) | ORM | Fase 1 | Nova |
| Backend | Alembic | Migrações do banco | Fase 1 | Nova |
| Backend | PostgreSQL | Banco de dados | Fase 1 | Já domina |
| Backend | Redis | Broker de tarefas e cache da liturgia | Fase 1 | Já domina |
| Backend | Celery (Taskiq como alternativa async) | Lembretes, checagem de heartbeats, alertas | Fase 1 | Já domina |
| Backend | JWT (PyJWT) + token de dispositivo | Autenticação feita à mão, sem o que o DRF dava pronto | Fase 1 | Aprofundar |
| Backend | pytest + httpx AsyncClient | Testes de API assíncrona | Fase 1 | Aprofundar |
| Mobile | Kotlin | Linguagem do app | Fase 1 | Nova |
| Mobile | Jetpack Compose | Interface do app | Fase 1 | Nova |
| Mobile | Room | Banco local para funcionar offline | Fase 1 | Nova |
| Mobile | WorkManager | Sincronização e heartbeat em segundo plano | Fase 2 | Nova |
| Mobile | Retrofit + kotlinx.serialization | Cliente HTTP da API | Fase 1 | Nova |
| Mobile | Firebase Cloud Messaging | Notificações push | Fase 1 | Nova |
| Mobile | VpnService | Interceptar e filtrar DNS no aparelho | Fase 2 | Nova |
| Redes | Protocolo DNS (RFC 1035) | Ler e responder pacotes DNS no filtro | Fase 2 | Nova |
| Redes | Listas de bloqueio (OISD, StevenBlack) | Domínios adultos e de anúncios | Fase 2 | Nova |
| Backend | WebSocket ou push para o parceiro | Alertas de adulteração em tempo real | Fase 3 | Nova |
| Infra | Docker + docker compose | Rodar API, Postgres e Redis igual em dev e produção | Fase 4 | Aprofundar |
| Infra | GitHub Actions | CI: testes e lint a cada push | Fase 4 | Nova |
| Infra | AWS ou VPS | Deploy da API | Fase 1 | Aprofundar |
| Mobile | AccessibilityService + DevicePolicyManager | Conteúdo dentro de apps e Device Owner | Fase 1 | Nova |
| Desktop | Linux: systemd-resolved, nftables | Bloqueio no Linux do notebook | Fase 5 | Aprofundar |
| Desktop | Go | Servidor DNS filtrante para a rede de casa | Fase 5 | Nova |
| Desktop | Extensão de navegador (JavaScript, Manifest V3) | Bloqueio e SafeSearch no navegador do notebook | Fase 5 | Aprofundar |

Os dois itens "a confirmar" dependem de você: se já usa Docker e GitHub Actions no estágio, mude para "Já domina" ou "Aprofundar".

## Arquitetura e modelo de dados

O bloqueio acontece inteiro no celular; o servidor só recebe sincronização e sinais de vida, e é ele quem avisa o parceiro quando algo para.

&#91;embedded content: arquitetura · celular, servidor, notebook e parceiro\]

O app sincroniza com a API; o Guardião manda heartbeats; o worker percebe quando eles param e alerta o parceiro. O tracejado indica o que só chega na Fase 5.

**Modelo de dados inicial**

| Entidade | Campos principais | Observação |
| --- | --- | --- |
| User | id, email, senha\_hash, criado\_em | Um único usuário, mas modelado direito |
| Device | id, user\_id, tipo, token\_hash, ultimo\_heartbeat | Celular e notebook autenticam como dispositivos |
| Practice | id, user\_id, tipo, nome, recorrencia, horario\_lembrete | Tipo: terço, consagração, leitura, confissão, outra |
| PracticeLog | id, practice\_id, data, feito\_em | Uma linha por prática cumprida no dia |
| Consecration | id, user\_id, nome, duracao\_dias, inicio, dia\_atual | Fase 2 |
| StreakEvent | id, user\_id, tipo, data | Tipo: início, queda, check-in; a streak é calculada a partir dos eventos, nunca guardada como número |
| AccountabilityPartner | id, user\_id, nome, email, codigo\_hash | Fase 3 |
| TamperEvent | id, device\_id, tipo, detectado\_em, alertado\_em | Tipo: VPN desligada, admin removido, sem heartbeat |
| Blocklist | id, nome, versao, url\_origem, atualizada\_em | O app baixa só quando a versão muda |

Guardar a streak como eventos, e não como um contador, é a decisão mais importante desse modelo: recorde, total do mês e histórico saem de uma única fonte, e dá ótimos testes unitários.

## Como usar IA sem virar muleta

A regra central: quanto mais nova a tecnologia para você, menos código a IA escreve. Em Python e Django ela pode acelerar; em Kotlin, DNS e Go ela vira professora, não programadora.

| Status da tecnologia | Papel da IA | O que você faz | Evitar |
| --- | --- | --- | --- |
| Nova | Tutora: explica conceitos, dá pistas, revisa o que você escreveu | Escreve todo o código, a partir da documentação oficial | Pedir "implemente X" e colar a resposta |
| Aprofundar | Revisora: critica seu código e aponta alternativas | Escreve a primeira versão e decide o que aceitar | Aceitar sugestões sem entender o porquê |
| Já domina | Acelerador: boilerplate, refatorações, testes repetitivos | Revisa tudo como revisaria um PR de colega | Deixar a IA decidir arquitetura |

**Regras práticas**

1. **Tente antes de perguntar.** Fique 25–30 minutos no problema com a documentação antes de abrir um chat. Travar faz parte de aprender.
2. **Peça pistas, não respostas.** Um bom pedido: "Não me dê código. Qual conceito eu não estou entendendo?" ou "Me dê só a próxima dica."
3. **Nada entra sem você saber explicar.** Se não consegue explicar cada linha em voz alta, apague e reescreva sem olhar.
4. **Você escreve os testes das partes novas.** TDD força você a entender o comportamento antes do código; a IA pode sugerir casos que você esqueceu.
5. **Autocomplete desligado nas sessões de estudo.** Copilot e similares escrevem por você sem você perceber; ligue só nas partes em Python.
6. **Decisões são suas.** Escreva o ADR primeiro; depois peça para a IA atacar a sua decisão.
7. **Registre o que aprendeu.** Um arquivo `TIL.md` no repositório com uma linha por dia vira material de revisão e de entrevista.

**Teste de muleta:** uma vez por fase, implemente uma funcionalidade pequena sem nenhuma IA. Se não conseguir, é sinal de voltar ao papel de tutora antes de seguir.

## Processo de software

O processo é um híbrido de Scrum e Kanban: do Scrum vem o ritmo (ciclos de duas semanas com meta, revisão e retrospectiva); do Kanban vem o fluxo (quadro com limite de trabalho em andamento). Você acumula os papéis de Product Owner, Scrum Master e Developer; o agente de IA ajuda nas tarefas de gestão, mas não decide nada.

**Ciclo de duas semanas**

| Evento | Quando | Duração | Saída |
| --- | --- | --- | --- |
| Planejamento | 1º dia do ciclo | 30 min | Meta do ciclo e issues escolhidas |
| Refinamento | Meio do ciclo | 20 min | Próximas issues prontas para entrar (Definition of Ready) |
| Daily assíncrona | Início de cada sessão | 5 min | Nota: o que fiz, o que farei, o que me trava |
| Revisão | Último dia | 15 min | Demo para você mesmo no celular; o que entrou e o que escorregou |
| Retrospectiva | Logo após a revisão | 15 min | Uma ou duas ações de melhoria para o próximo ciclo |

**Conceitos ágeis que você vai praticar**

- **História de usuário:** "Como \[quem\], quero \[o quê\], para \[por quê\]". Mesmo sendo você o usuário, escrever o "para quê" evita construir coisa inútil.
- **Critérios de aceite:** cenários no formato Dado / Quando / Então. Eles viram seus testes quase direto, o que casa com TDD.
- **Definition of Ready:** a issue só entra no ciclo se tiver história, critérios de aceite e tamanho P ou M.
- **Definition of Done:** testes passando no CI, código revisado no PR, documentação atualizada, linha no `TIL.md` se aprendeu algo.
- **Estimativa por tamanho:** P (até 1 sessão), M (2 sessões), G (precisa ser quebrada). Mais honesto que horas para quem ainda está aprendendo a tecnologia.
- **Limite de WIP:** no máximo duas issues em andamento.
- **Métricas:** velocidade (issues fechadas por ciclo) e lead time (tempo da issue de "Próximo" a "Feito"). Servem para planejar melhor, não para cobrar desempenho.

Para estudar a base, leia o [Scrum Guide](https://scrumguides.org/scrum-guide.html) (curto e gratuito) e compare com o que você estiver praticando aqui.

**Fluxo de código:** uma branch por issue, PR para a `main` com CI rodando, merge só depois de reler o diff no dia seguinte. Commits no padrão Conventional Commits, referenciando a issue (`feat(streak): registra queda #12`).

## Planejamento

A Fase 1 cabe em quatro ciclos de duas semanas (cerca de 8 semanas). O prazo é fixo e o escopo é flexível: se um ciclo escorregar, corte requisitos em vez de esticar a fase.

**Ciclos da Fase 1**

1. **Ciclo 1 — Fundação da API.** Repositório, FastAPI organizado por domínio, banco, autenticação e CRUD de práticas, tudo com testes e CI.
2. **Ciclo 2 — Regras do domínio.** Checklist do dia (RF03), streak por eventos (RF11, RF12), terço com mistérios (RF04) e confissão (RF06). Primeiro deploy da API.
3. **Ciclo 3 — App Android básico.** Projeto Kotlin + Compose, login, checklist do dia e streak consumindo a API.
4. **Ciclo 4 — Offline e lembretes.** Room, sincronização com WorkManager e notificações (RF05). Revisão da Fase 1 e início das duas semanas de uso real.

**Backlog do Ciclo 1** — meta: *API de práticas rodando localmente, com autenticação e CI verde.*

| # | Issue | Tamanho | Requisito |
| --- | --- | --- | --- |
| 1 | Criar repositório com `api/`, `android/`, `dns/`, `docs/`, README, `TIL.md` e quadro no GitHub Projects | P | — |
| 2 | Escrever ADR-001: FastAPI com SQLAlchemy async | P | RNF08 |
| 3 | Subir Postgres e Redis com docker compose | P | — |
| 4 | Esqueleto FastAPI por domínio, health check e pytest configurado | M | RNF07 |
| 5 | Modelos User, Practice e PracticeLog com a primeira migração Alembic | M | RF02 |
| 6 | Autenticação JWT: registro, login e refresh | M | RF01, RNF05 |
| 7 | CRUD de práticas com recorrência | M | RF02 |
| 8 | GitHub Actions rodando lint e pytest a cada PR | M | RNF07 |

São oito issues, três P e cinco M. Se no fim do ciclo você fechar cinco, essa é a sua velocidade real, e o Ciclo 2 já é planejado com ela.

**Modelo de issue**

O template fica em `.github/ISSUE_TEMPLATE/historia.md`. O tamanho vai na label (`P` ou `M`) e a nota de parada vai como comentário na issue, ao fim de cada sessão.

```markdown
## História
Como devoto, quero registrar uma queda na streak, para recomeçar sem perder meu histórico.

## Critérios de aceite

- [ ] Dado uma streak de 10 dias, quando registro uma queda, então a streak atual volta a 0 e o recorde continua 10.
- [ ] Dado uma queda registrada hoje, quando consulto o mês, então o total de dias limpos do mês não é apagado.
```

## Agente de IA como gerente do projeto

O agente funciona como um assistente de Product Owner e Scrum Master: organiza, resume e questiona. Você prioriza, decide e escreve o código das partes novas. Usado assim, ele ensina ágil, porque cada evento acontece de verdade e ele cobra o que você pularia.

| Atividade | O agente faz | Você faz |
| --- | --- | --- |
| Backlog | Transforma requisitos em issues no modelo, com critérios de aceite; aponta duplicatas | Prioriza e aprova |
| Refinamento | Questiona critérios vagos e sugere como quebrar issues G | Decide a quebra |
| Planejamento | Compara a velocidade dos últimos ciclos com as issues escolhidas e avisa se passou do limite | Define a meta e escolhe as issues |
| Daily | Lê commits e notas de parada e resume onde você está | Escreve a nota de parada |
| Revisão | Gera o relatório do ciclo: issues fechadas, escorregadas, lead time | Faz a demo no celular |
| Retrospectiva | Faz as perguntas e registra as ações como issues de processo | Escolhe as ações |
| Pull requests | Revisa contra a Definition of Done e aponta testes faltando | Decide o merge |

**Regras do agente**

1. **Propõe, não executa.** Não fecha issue, não muda prioridade e não faz merge sem sua aprovação.
2. **Mesmo limite da seção de muleta.** Em tecnologia marcada como Nova, ele gerencia o trabalho e revisa, mas não escreve a implementação.
3. **O GitHub é a fonte da verdade.** Issues, milestones e labels guardam o estado do projeto; a conversa com o agente não guarda.
4. **As regras ficam num arquivo do repositório**, que você mantém e o agente lê sempre.

**Como montar, em níveis**

1. **Convenções no GitHub.** Milestone = ciclo. Labels de tipo (`feat`, `bug`, `estudo`, `chore`), de módulo e de tamanho. O modelo de issue acima é o template em `.github/ISSUE_TEMPLATE/historia.md`. Sem isso, nenhum agente consegue ajudar.
2. **Agente no terminal, dentro do repositório.** O [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) lê o código e pode usar a `gh` CLI para criar e editar issues, milestones e PRs. As regras do processo vão num `CLAUDE.md` na raiz, e cada evento vira um comando reutilizável (planejar ciclo, refinar, daily, revisão, retro).
3. **Automação no GitHub Actions (depois da Fase 1).** Ao abrir uma issue, um workflow chama a API do Claude e comenta se ela cumpre a Definition of Ready. No último dia do ciclo, um workflow agendado gera o relatório da revisão. Bom para aprender Actions, que está marcado como Nova.
4. **Seu próprio agente (opcional, vai para "Depois").** Um "Scrum Master" em LangGraph com ferramentas para ler issues pela API do GitHub, calcular métricas e propor o plano do ciclo. É a sua stack e dá um ótimo projeto de portfólio de IA, mas não pode competir com o app.

**Exemplo de trecho do `CLAUDE.md`**

```markdown
# Processo do projeto
- Ciclos de 2 semanas; cada ciclo é um milestone no GitHub.
- Issue pronta = história + critérios Dado/Quando/Então + tamanho P ou M.
- Você PROPÕE; eu aprovo. Nunca feche issues, mude prioridades ou faça merge.
- Em Kotlin, Android, DNS e Go: não escreva a implementação.
  Explique, dê pistas e revise o que eu escrevi.
- No fim de cada sessão, me lembre de atualizar a nota de parada da issue.
```

## Por onde começar

Comece pelo backend do MVP em FastAPI e só abra o Android Studio quando a API de devocional e streak estiver testada. Em paralelo, estude o básico de Kotlin, sem escrever o app ainda.

**Fases e critério de pronto**

1. **Fase 1 — MVP devocional + streak.** Pronta quando o app estiver no seu celular e você usá-lo todo dia por duas semanas.
2. **Fase 2 — Filtro DNS, SafeSearch, consagrações e liturgia.** Pronta quando sites de teste forem bloqueados no navegador e em três apps, com a bateria dentro da meta.
3. **Fase 3 — Accountability.** Pronta quando desligar a VPN gerar um alerta ao parceiro em poucos minutos.
4. **Fase 4 — Endurecimento.** AccessibilityService e Device Owner, testados primeiro num aparelho velho ou emulador. Pronta quando desinstalar sem o código do parceiro não for possível pelo caminho comum.
5. **Fase 5 — Notebook e DNS em Go.** Pronta quando o notebook, no Windows e no Linux, tiver o mesmo nível de bloqueio do celular.

**Primeiras tarefas (semanas 1 e 2)**

- [ ] Ativar hoje um filtro DNS pronto (NextDNS ou AdGuard DNS) no celular e no notebook, enquanto o seu não fica pronto
- [ ] Escolher o parceiro de accountability e conversar com ele sobre o projeto
- [ ] Criar o repositório com as pastas `api/`, `android/`, `dns/` e `docs/`, mais `README.md` e `TIL.md`
- [ ] Ler o User Guide oficial do FastAPI até as seções de Dependencies e Security
- [ ] Escrever o ADR-001: por que FastAPI com SQLAlchemy async
- [ ] Subir Postgres e Redis com docker compose
- [ ] Modelar práticas, registros e streak; primeira migração com Alembic
- [ ] Endpoints de práticas e checklist do dia, com testes escritos antes
- [ ] Regras da streak (queda, recorde, total do mês) com testes unitários
- [ ] Em paralelo: Kotlin Koans e o curso Android Basics with Compose, do Google
