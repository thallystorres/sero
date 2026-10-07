## 2026-10-06

- Normalmente se instancia o app do FastAPI no `main.py` na raiz do app, junto com alguns arquivos de configuração geral, database e etc (#14)
- Semelhante ao que eu faço no Django, a comunidade do FastAPI recomenda uma divisão por domínio das pastas do projeto, que podem conter arquivos de gerenciamento de rotas (`router.py`), schemas do Pydantic, models e etc (#14)
- Os testes ficam numa pasta `tests/` dentro da raíz do repositório (nesse caso, dentro de `api/`) (#14)
- A palavra chave await só pode ser necessariamente usada em funções async. Ela pausa todas as próximas linhas para esperar o fim da tarefa, e só pode ser aplicada em objetos ou funções que também são `awaitables` (#14)
- Já o yield retorna o estado intermediário de algo função GERADORA, funciona basicamente como um return, mas não acaba com a função quando é chamado (#14)
- Quando bato num await numa função síncrona, ela trava aquela função até chegar mais informações, mas libera todo o event loop pra executar outras tarefas async que estão sobrando (#14)

## 2026-10-05

- Quando for usar Redis como Broker, é legal guardar em disco algumas coisas em algum volume montado no Docker (#4)
- Esse volume montado serve pra garantir persistência de dados e evitar perda de mensagens caso o container caia (#4)
- Tem o RDB que guarda snapshots periódicos e tem o AOF que guarda logs de cada comando (#4)
- Busque sempre usar uma versão do Debian pra imagem do Postgres, elas usam glibc que performa melhor na busca de textos (#4)
- Uvicorn é um servidor ASGI (Asynchronous Server Gateway Interface), ele define uma interface pra se comunicar entre a web o server async (#14)

## 2026-10-03

- Schema de API é diferente de Schema de dados (#3)
- Tem como configurar o entrypoint no `pyproject.toml` (#3)

  ```toml
  [tool.fastapi]
  entrypoint = "main:app"
  ```

- Caso o entrypoint estiver em um diretório diferente (como em sei lá `./api/main.py`), então a config deveria ser (#3)

  ```toml
  [tool.fastapi]
  entrypoint = "api.main:app"
  ```

- O FastAPI faz endpoints serem mais parecidos com funções, e não como classes como os ViewSets do Django REST Framework (#3)
- Em casos em que há mais de um caminho em uma url (por exemplo, a URL `/users/` pode ter tanto `/users/me` quanto `/users/{user_id}`), o endpoint fixo precisa vir primeiro na ordem do código (ou seja, `/users/me` vem primeiro), porque as rotas são avaliadas em ordem e `/users/{user_id}` capturaria o `me` (#3)
- Dá pra ter query parameters, path parameters e body na mesma requisição, mas para desempacotar um modelo pydantic em um dict é legal usar `**model.model_dump()` (#3)
- Tem como fazer validação adicional de string ou números em PP ou QP (#3)
- Com a forma especial typing.Annotated é possível adicionar metadados em um tipo para esses casos (#3)
- É possível até mesmo fazer um modelo do Pydantic para diversos query parameters juntos, com `Annotated[CustomParamsFeitosPorMim, Query()]` (#3)
- Caso eu queira que meu body da API receba o nome do modelo do Pydantic mesmo quando for um objeto único, usar como `model: Annotated[MeuModel, Body(embed=True)]` (#3)
- SQLAlchemy possui uma forma de se conectar de forma async com o banco, assim dá pra usar endpoints async da API com conexões de banco (#3)
- Existe também o SQLModel, feito por quem criou o FastAPI que é uma camada fina de abstração sobre o SQLAlchemy e o Pydantic, mas é bem imaturo e instável, além de simplificar muito as coisas, é melhor não usar no projeto (#3)
- O Celery não é async (eu achava que era). Ele na realidade é síncrono e existem opções async como o Taskiq e ARQ (#3)
- Para utilizar o Celery com o SQLAlchemy async, dá pra usar um engine sem pool, que abre e fecha a conexão junto com a sessão (#3)

## 2026-10-02

- Descobri que tem como configurar um template de issue pro GitHub usando aquela pastinha lá do `.github`. (#11)
- Achei bem legal o tanto de integração que o ambiente do GitHub tem entre si, esses cara conseguiram integrar tanto projetos como issues e automatizar no repositório. (#1)
- O arquivo `.gitkeep` em pastas vazias serve pra trackear essas pastas no git mesmo que elas não tenham nenhum conteúdo nelas ainda, serviu como uma luva nas pastas de aplicação que eu ainda vou desenvolver. (#1)
