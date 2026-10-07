<div align="center">

# Sero

*Sero te amavi* — "Tarde te amei"

<sub>Santo Agostinho, *Confissões* X, 27</sub>

**Nunca é tarde para recomeçar.**

</div>

---

## A ideia

Sero é um aplicativo pessoal para organizar a vida devocional, acompanhar uma caminhada de pureza e proteger o celular e o notebook de conteúdo adulto e anúncios.

O nome vem de Santo Agostinho, e a ideia central vem junto com ele: uma queda não apaga o caminho já percorrido. O app existe para ajudar a recomeçar, não para punir.

Ele é dividido em três partes, cada uma com um nome em latim:

| Nome | Significado | Do que cuida |
| --- | --- | --- |
| **Tolle Lege** | "Toma e lê" — a conversão de Agostinho (*Confissões* VIII, 12) | As práticas devocionais |
| **Surgam** | "Levantar-me-ei e irei a meu pai" (Lc 15,18) | A contagem de dias e o recomeço |
| **Vigilare** | "Vigiai e orai" (Mt 26,41) | O bloqueio e a prestação de contas |

O projeto tem dois objetivos de mesmo peso: ser um produto usado todos os dias e ser um laboratório de aprendizado. É de uso pessoal, feito por uma pessoa só.

## Funcionalidades previstas

O trabalho está dividido em cinco fases. A primeira entrega só conta, devocional e contagem de dias, sem bloqueio nenhum; o resto entra na ordem abaixo.

**Tolle Lege — devocional**

- Práticas com recorrência diária, por dia da semana, semanal ou mensal, e o checklist do dia (Fase 1)
- Terço guiado, com os mistérios do dia e contador de dezenas (Fase 1)
- Lembretes por notificação, com horário por prática (Fase 1)
- Confissão: data da última e lembrete depois de um intervalo configurável (Fase 1)
- Consagrações com duração, liturgia diária, exame de consciência e calendário de constância (Fase 2)

**Surgam — contagem de dias e recomeço**

- Contador de dias, com data de início configurável (Fase 1)
- Registro de queda: zera a contagem atual, preserva o recorde e o total do mês e aponta para a confissão (Fase 1)
- Check-in diário opcional (Fase 2)

**Vigilare — bloqueio e prestação de contas**

- Filtro DNS no próprio aparelho, com listas de conteúdo adulto e anúncios, SafeSearch forçado e bloqueio de DNS-over-HTTPS (Fase 2)
- Parceiro de prestação de contas, avisado quando o aparelho para de dar sinal ou o filtro é desligado; pausar ou desinstalar exige o código dele ou uma espera de 24–48h (Fase 3)
- Detecção de palavras-chave dentro de apps e proteção contra desinstalação (Fase 4)
- Bloqueio no notebook e servidor DNS próprio para a rede de casa (Fase 5)

Os sites acessados são filtrados no aparelho e nunca vão para o servidor. Ficam de fora, de propósito: iOS, Play Store, vários usuários e frontend web.

A lista completa de requisitos, o modelo de dados e o roadmap estão em [`docs/requisitos.md`](docs/requisitos.md).

## O que já foi feito

O projeto está no primeiro ciclo da Fase 1, cuja meta é a API de práticas rodando localmente, com autenticação e CI verde.

- [x] Repositório, convenções do GitHub e modelo de issue (#1)
- [x] ADR-001: FastAPI com SQLAlchemy 2.0 async (#3)
- [x] Postgres e Redis locais com docker compose (#4)
- [x] Esqueleto FastAPI por domínio, health check e pytest (#5)
- [ ] Modelos `User`, `Practice` e `PracticeLog` com a primeira migração (#6)
- [ ] Autenticação JWT: registro, login e refresh (#7)
- [ ] CRUD de práticas com recorrência (#8)
- [ ] GitHub Actions com lint e pytest a cada PR (#9)

A API ainda só responde ao health check, e não há aplicativo.

## Infraestrutura

| Parte | Pasta | Tecnologia |
| --- | --- | --- |
| Servidor | `api/` | Python, FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Redis, Celery |
| Aplicativo | `android/` | Kotlin, Jetpack Compose, Room |
| DNS da rede de casa | `dns/` | Go |

O servidor só recebe sincronização e sinais de vida dos aparelhos; o bloqueio acontece inteiro no celular. As decisões de arquitetura são registradas como ADRs em `docs/`.

Para subir o ambiente local, a partir de `api/`:

```sh
cp .env.example .env          # e troque a senha
docker compose up -d --wait   # sobe Postgres e Redis e espera ficarem saudáveis
docker compose down           # derruba mantendo os dados; com -v, apaga os volumes
```

As portas são publicadas só em `127.0.0.1`.

Para subir a API e rodar os testes, também a partir de `api/`:

```sh
uv sync              # instala as dependências
uv run fastapi dev   # sobe a API em http://127.0.0.1:8000
uv run pytest        # roda os testes
```

## Como o projeto é tocado

- Ciclos de duas semanas, cada um como um milestone no GitHub, com no máximo duas issues em andamento.
- Toda issue tem história, critérios de aceite e tamanho; o estado do projeto vive nas issues, não em conversas.
- Uma branch por issue, PR para a `main` e squash merge depois de reler o diff no dia seguinte.
- Commits no padrão Conventional Commits, referenciando a issue.
- [`TIL.md`](TIL.md) guarda uma linha por dia com o que foi aprendido.
- O assistente de IA segue as regras de [`CLAUDE.md`](CLAUDE.md): nas tecnologias novas para o autor, ele explica e revisa, mas não escreve a implementação.
