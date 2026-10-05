---
Número do ADR: 001
Título: Utilizando FastAPI e SQLAlchemy 2.0 async
Data: 2026-10-03
Responsável: Thallys
Status: Aceito
---

### Contexto

No início do projeto é necessário fazer algumas escolhas de stack para o desenvolvimento do sistema, que engloba produção de APIs, conexão com banco de dados em um servidor e **principalmente** o aprendizado facilitado sobre desenvolvimento em novas tecnologias.

### Decisão

Foi decidido utilizar o Python com FastAPI para formular a API de backend do sistema, além do SQLAlchemy 2.0 como toolkit de SQL e ORM para gerenciar de forma facilitada o uso do banco de dados usado na aplicação, usando async para conexão com o banco de dados.

### Justificativa

A decisão dessa stack foi tomada por três motivos principais:

- Eu, como desenvolvedor Django, já tenho experiência em desenvolver aplicações nessa linguagem de forma profissional
- Entretanto, gostaria de aprender tecnologias novas e diferentes do que já uso profissionalmente para expandir meus horizontes de conhecimento
- E gostaria de uma stack moderna que pudesse me pôr no centro das decisões mais atuais de stacks e desenvolvimento de código limpo

### Alternativas

Foram consideradas as seguintes alternativas:

- Django com Django ORM: não queria utilizar ferramentas que eu já tinha conhecimento
- Node.js e TS com Express e Prisma ORM: Nunca tive contato com TS e seria uma barreira muito grande de entrada
- SQLAlchemy síncrono: O uso de FastAPI brilha no async, mesmo que eu não vá precisar muito. Gerenciar websockets de aviso em tempo real se encaixa bem em um servidor async, mas é apenas uma funcionalidade entre muitas. Mesmo assim, quero aprender mais sobre programação concorrente e paralela.
- SQLModel no lugar do SQLAlchemy puro: bem mais fácil de manipular, mas desatualizado e provavelmente teria que usar ambos

### Consequências

A escolha dessa stack traz as seguintes consequências:

- Curva de aprendizado para desenvolver os primeiros endpoints
- Aprender o ecossistema que gira em torno dessas tecnologias como Alembic, uv, uvicorn e Pydantic
- Desenvolver com programação assíncrona que não tenho muita familiaridade
- O gerenciamento de tasks pelo Celery de início vai ser difícil para fazer consultas, mas não foi definido 100% o uso do Celery, vira decisão futura

### Objeções e respostas

1. O app tem um usuário. Que problema de concorrência o async resolve aqui, e o que você perderia usando SQLAlchemy síncrono com endpoints def?
   Aceito como custo: No fim eu só quero aprender coisas novas mesmo. Usar async só vai trazer mais complexidade que não é justificada pelo baixo número de usuários.
2. O Celery é síncrono. Como o worker de heartbeat da Fase 3 vai acessar o banco se toda a camada de dados for async?
   Refutado: Dá pra usar uma sessão sem pool no SQLAlchemy para contornar isso, fazendo a conexão ser fechada quando a sessão for fechada, além de usar async_to_sync, assim toda task vai rodar o próprio event loop e sem precisar manipulá-lo manualmente. Ademais, já que não haverá demanda de altíssimo desempenho, posso manter essa incompatibilidade entre Celery e async. Caso o projeto evolua, é possível trocar a infraestrutura de gerenciador de tasks para um Taskiq (feito pra ser um "Celery async") ou ARQ (ótimo em compatibilidade pro Redis). No final: ainda dá pra voltar atrás, é apenas na fase 3, posso adotar o Taskiq depois.
3. Kotlin, Compose, Go e DNS já são novos, e o prazo da fase é fixo. Um backend também novo não é novidade demais de uma vez, quando Django entregaria conta e CRUD em dias?
   Aceito o custo: Eu realmente não tô nem aí pra entregar um CRUD em dias ou em semanas. A prioridade é aprender, e depois entregar. Caso não consiga entregar, paciência: bota pro próximo ciclo. Nenhuma lentidão me fará voltar atrás, mas também quero fazer todas as funcionalidades previstas.
4. O próprio tutorial do FastAPI usa SQLModel. Por que SQLAlchemy puro?
   Refutado: O SQLModel ainda está muito imaturo e muitas vezes para definição de índices, tipos específicos de tabelas, relacionamentos elaborados e esconder tabelas precisam descer o nível pro SQLAlchemy... Mantém no SQLAlchemy puro, ele já tem uma boa camada de abstração e eu já estou acostumado em ter que ter um parser e um model da tabela (no DRF temos os serializers e os models do Django, não é tão diferente)
