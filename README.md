# WeatherMap - Backend Python Application

## Descrição

WeatherMap é uma aplicação de backend desenvolvida em Python, projetada para coletar dados da API Open Weather e armazená-los como JSON. A aplicação permite que usuários obtenham informações meteorológicas de várias cidades de forma assíncrona, respeitando os limites de taxa da API, e consulta o progresso das coletas em andamento.

## Requisitos Ferramentas

### Requisitos Completos

- [x] **Linguagem de Programação Python**: Desenvolvida inteiramente em Python 3 como requisito do projeto.
- [x] **Banco de Dados Não Relacional**: Utilização do MongoDB, um banco de dados não relacional por conta da flexibilidade de schema, desempenho/escalabilidade e a facilidade de integração com Python.
- [x] **FastAPI**: Usado FastApi pela capacidade de uso com banco nosql, arquitetura customizável(clean arch), suporte a operações async e documentação automática.
- [x] **Pytest**: Framework utilizado por conta da riqueza de funcionalidades, como fixture, plugins, code coverage e ainda suporte para testes async.

# Como rodar a aplicação

#### Requisitos mínimos

- Docker/Docker-compose
- Client mongodb(compass), caso queira acessar o banco manualmente.

## Instruções para Clonar e Executar a Aplicação

1.  **Clonar o Repositório**:

```bash

git  clone https://github.com/apenasweber/weathermap-challenge.git

```

```bash

cd  weathermap

```

2.  **Renomear o Arquivo de Configuração**:

- Renomeie o arquivo `.env-example` para `.env`

3.  **Construir e Executar a Aplicação/Testes**:

- Utilize para construir/executar a aplicação o comando:

```bash

-docker-compose up --build

```

- Para rodar apenas os testes:

```bash

docker-compose up --build tests

```

4.  **Acessar a Documentação da API**:

- Agora você pode acessar [http://localhost:8000/docs](http://localhost:8000/docs) para testar os endpoints manualmente.

## Endpoints da API

### 1. Coletar Dados Meteorológicos

- **Método e Caminho**: `POST /collect`
- **Parâmetros**:
  - `user_defined_id`: ID definido pelo usuário para a coleta (único para cada requisição).
- **Descrição**: Inicia a coleta de dados meteorológicos de várias cidades.

### 2. Progresso da Coleta

- **Método e Caminho**: `GET /progress/{user_defined_id}`
- **Parâmetros**:
  - `user_defined_id`: ID definido pelo usuário.
- **Descrição**: Retorna o progresso da coleta de dados meteorológicos para o ID especificado.

# Benefícios Clean Arch

- **Separação de Responsabilidades**: Cada parte da aplicação tem um trabalho específico, tornando o código mais fácil de entender, manter e desenvolver.

- **Testabilidade**: Com seções separadas para diferentes aspectos do aplicativo, fica mais fácil testar unidades individuais de código.

- **Escalabilidade**: Com Docker e código modular, é mais fácil escalar a aplicação conforme necessário.

- **Organização**: O código é mais fácil de encontrar em um projeto bem estruturado.

- **Controle de Versão**: A separação também ajuda no gerenciamento de controle de versão, pois as mudanças podem ser isoladas em áreas específicas do projeto.

- **Reutilização**: Com uma estrutura bem definida, fica mais fácil reutilizar componentes conforme necessário.

- **Segurança**: Armazenar dados sensíveis em variáveis de ambiente (arquivo .env) protege as informações de serem expostas.

## Estrutura da Aplicação

- **app**: É onde reside a lógica principal do aplicativo. Está dividido em vários subdiretórios:

- **api**: Contém a versão da API e seus endpoints. No meu caso, a versão v1 da API.

- **endpoints**: Contém os diferentes endpoints da API.

- **core**: Este diretório mantém a funcionalidade central do meu projeto, como conexões com o banco de dados e configurações.

- **tests**: Este diretório contém todos os meus casos de teste, divididos em testes unitários, de integração e de estresse.

- **.env e .env-example**: Esses arquivos são usados para armazenar variáveis de ambiente.

- **docker-compose.yaml e Dockerfile**: Esses arquivos são usados para contêinerizar a aplicação e gerenciar serviços, fornecendo um ambiente isolado para a execução do aplicativo.

- **requirements.txt**: Este arquivo lista todas as dependências da biblioteca Python que precisam ser instaladas usando pip install.

---
