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

## O que há no repositório

```
sero/
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── historia.md
├── api/
│   ├── .env.example
│   └── docker-compose.yml
├── android/
├── dns/
├── docs/
│   ├── adr-001-fastapi-sqlalchemy-async.md
│   └── requisitos.md
├── CLAUDE.md
├── README.md
├── TIL.md
└── .gitignore
```

### Pastas

| Pasta | Para que serve |
| --- | --- |
| `api/` | O servidor do app; por enquanto, só o ambiente local com Postgres e Redis |
| `android/` | O aplicativo Android |
| `dns/` | O servidor de DNS |
| `docs/` | A documentação do projeto |
| `.github/` | Configurações do GitHub, como o modelo de issue |

As pastas `android/` e `dns/` ainda estão vazias. Cada uma tem um arquivo `.gitkeep`, que existe só porque o git não guarda pastas vazias.

### Arquivos

**`README.md`** — este arquivo. É a porta de entrada: explica a ideia e mostra onde cada coisa está. Ele descreve o repositório como ele é hoje e é atualizado conforme o projeto muda.

**`docs/requisitos.md`** — o documento de onde tudo parte. Reúne o que o app precisa fazer, o plano e a forma de trabalho. Para entender o projeto a fundo, é por ele que se continua a leitura.

**`docs/adr-001-fastapi-sqlalchemy-async.md`** — o registro da decisão de usar FastAPI com SQLAlchemy 2.0 async no servidor: contexto, alternativas e consequências.

**`api/docker-compose.yml`** — sobe o Postgres e o Redis usados no desenvolvimento. Dentro de `api/`, `docker compose up -d --wait` inicia os dois e espera ficarem saudáveis; `docker compose down` os derruba sem apagar os dados. As portas ficam acessíveis só na própria máquina.

**`api/.env.example`** — o modelo das variáveis que o `docker-compose.yml` exige. Copie para `api/.env`, que não é versionado, e troque a senha.

**`TIL.md`** — *Today I Learned*, "hoje eu aprendi". Um diário com uma linha por dia de trabalho, registrando o que foi aprendido.

**`CLAUDE.md`** — as regras que o assistente de IA segue neste repositório: o que ele pode fazer, o que deve deixar para o autor e como o trabalho é organizado.

**`.github/ISSUE_TEMPLATE/historia.md`** — o modelo usado ao abrir uma issue no GitHub: a história ("Como… quero… para…") e os critérios de aceite em forma de lista de verificação.

**`.gitignore`** — a lista do que o git não deve guardar, como senhas, arquivos temporários e configurações da máquina.

## Mantendo este README

Este arquivo fala só do que já existe. Quando uma pasta ganhar conteúdo ou um arquivo base for criado, a seção acima é atualizada junto.
