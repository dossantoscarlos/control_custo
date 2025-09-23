# Controle de Custo

Este é um projeto de exemplo que demonstra uma aplicação FastAPI com integração com Keycloak para autenticação, e uma stack de observabilidade com Grafana, Prometheus e OpenTelemetry. A arquitetura do projeto segue o padrão Ports and Adapters.

## Começando

Estas instruções permitirão que você tenha uma cópia do projeto em funcionamento em sua máquina local para fins de desenvolvimento e teste.

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd control_custo
   ```

2. Instale as dependências do Python com o Poetry:
   ```bash
   poetry install
   ```

3. Inicie todos os serviços com o Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Uso

Após iniciar os serviços, você pode acessar as seguintes aplicações:

- **API Gateway (NGINX)**: [http://localhost](http://localhost)
- **FastAPI (através do gateway)**: [http://localhost/api](http://localhost/api)
- **Keycloak (através do gateway)**: [http://localhost/auth](http://localhost/auth)
- **Grafana**: [http://localhost:3000](http://localhost:3000) (usuário: `admin`, senha: `admin`)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)

### Autenticação

O projeto vem com um realm pré-configurado para o Keycloak que é importado na primeira inicialização. Para se autenticar, você pode obter um token de acesso para o usuário de exemplo:

- **URL**: `http://localhost/auth/realms/fastapi-realm/protocol/openid-connect/token`
- **Method**: `POST`
- **Body** (x-www-form-urlencoded):
    - `grant_type`: `password`
    - `client_id`: `fastapi-id-client`
    - `username`: `fastapi`
    - `password`: `fastapi`
    - `client_secret`: `my-secret`

### Acessando Endpoints Protegidos

Para acessar endpoints protegidos, como o `/api/me`, inclua o token de acesso no cabeçalho `Authorization`:

```
Authorization: Bearer <seu-token-de-acesso>
```

## Tarefas

O projeto usa o `taskipy` para gerenciar tarefas de desenvolvimento. As seguintes tarefas estão disponíveis:

- `lint`: Executa o `ruff` e o `isort` para verificar o estilo e a formatação do código.
- `test`: Executa os testes com o `pytest`.
- `run`: Inicia a aplicação FastAPI em modo de desenvolvimento (usado pelo Docker Compose).

Para executar uma tarefa, use o comando `poetry run task <nome-da-tarefa>`.

## Arquitetura

O projeto segue a arquitetura Ports and Adapters (ou Hexagonal). A estrutura de diretórios é a seguinte:

- `src/control_custo/domain`: Contém os modelos de dados da aplicação.
- `src/control_custo/application`: Contém a lógica de negócio e os casos de uso.
- `src/control_custo/adapters`: Contém as implementações de tecnologias externas, como o FastAPI (`web`) e o banco de dados (`db`).

## Observabilidade

O projeto inclui uma stack de monitoramento com:

- **OpenTelemetry**: Para coletar métricas e traces da aplicação FastAPI.
- **Prometheus**: Para armazenar as métricas.
- **Grafana**: Para visualizar as métricas em dashboards.
