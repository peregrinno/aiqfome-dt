# API AiQfome - Desafio Técnico

API para gerenciar clientes e seus produtos favoritos.

Explicações das tomadas de decição em [Leia-me.md](Leia-me.md)

# Documentação REST

aiqfome-peregrinno.apidog.io [Leia-me.md](Leia-me.md)

## Funcionalidades

- Autenticação de clientes
- Gerenciamento de produtos favoritos
- Integração com API externa de produtos

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis (cache)
- Docker

## Executando com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Passos para execução

1. Clone o repositório:

```bash
git clone https://github.com/peregrinno/aiqfome-dt.git
cd aiqfome-dt
```

2. Inicie os containers com Docker Compose:

```bash
docker-compose up -d
```

3. Acesse a API em [http://localhost:8000](http://localhost:8000)
4. Acesse a documentação da API em [http://localhost:8000/docs](http://localhost:8000/docs)

### Observações

- O PostgreSQL está configurado para usar a porta 55432 para evitar conflitos com instalações locais
- O Redis está configurado para usar a porta 56379 para evitar conflitos com instalações locais
- Os dados do PostgreSQL e Redis são persistidos em volumes Docker
- O sistema utiliza Redis para cache dos produtos da API externa
- Cache automático atualizado periodicamente em segundo plano

## Endpoints

### Autenticação

- `POST /v1/auth/clientes` - Registrar um novo cliente
- `POST /v1/auth/login` - Autenticar um cliente
- `GET /v1/auth/clientes/me` - Obter dados do cliente autenticado
- `PUT /v1/auth/clientes/me` - Atualizar dados do cliente autenticado
- `DELETE /v1/auth/clientes/me` - Excluir o cliente autenticado

### Produtos

- `GET /v1/produtos` - Listar todos os produtos disponíveis
- `GET /v1/produtos/{produto_id}` - Obter detalhes de um produto específico
- `GET /v1/produtos/favoritos` - Listar os produtos favoritos do cliente autenticado
- `POST /v1/produtos/favoritos` - Adicionar um produto aos favoritos
- `DELETE /v1/produtos/favoritos/{produto_id}` - Remover um produto dos favoritos
- `POST /v1/produtos/cache/update` - Atualizar o cache de produtos (requer chave de API)
- `DELETE /v1/produtos/cache` - Limpar o cache de produtos (requer chave de API)

### Health Check

- `GET /v1/health-check` - Verificar o status da API

## Estrutura do Projeto

```
.
├── Dockerfile              # Configuração para construção da imagem Docker
├── README.md              # Documentação do projeto
├── docker-compose.yml     # Configuração para orquestração dos serviços
├── pyproject.toml        # Configuração do projeto Python
├── requirements.txt      # Dependências do projeto
├── settings.py           # Configurações da aplicação
├── version               # Versão atual do projeto
├── webserver.py          # Ponto de entrada da aplicação
├── src/                  # Código fonte da aplicação
│   ├── controllers/      # Controladores da aplicação
│   ├── database.py       # Configuração do banco de dados
│   ├── dependencies.py    # Dependências da aplicação
│   ├── gateway.py        # Configuração das rotas da API
│   ├── init_db.py        # Inicialização do banco de dados
│   ├── interfaces/       # Interfaces Pydantic
│   ├── models/           # Modelos SQLAlchemy
│   ├── routes/           # Rotas da API
│   └── services/         # Serviços externos
```

## Cache de Produtos

O sistema utiliza Redis para armazenar em cache os produtos obtidos da API externa (fakestoreapi.com). Isso proporciona:

- Melhor desempenho nas consultas
- Menor dependência da API externa
- Redução de tráfego de rede

### Atualização Automática

O cache é atualizado automaticamente em segundo plano, com intervalo configurado pela variável `REDIS_TTL` (padrão: 1 hora).

### Atualização Manual

Você pode atualizar o cache manualmente de duas formas:

1. Usando a API (requer chave de API):

```bash
curl -X POST http://localhost:8000/v1/produtos/cache/update -H "X-API-Key: ?Z0JBsN4Lb1LdEe8aFxhH-g"
```

2. Executando o script de atualização:

```bash
python update_cache.py
```

Este script pode ser configurado como uma tarefa agendada (cron job) para atualizações periódicas.

## Desenvolvimento

### Versionamento

Este projeto segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

### Dependências de Desenvolvimento

Para desenvolvimento, recomenda-se instalar as dependências adicionais:

```bash
pip install isort
```

### Formatação de Código

Para formatar o código:

isort .

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).
