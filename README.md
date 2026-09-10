# Smart Stock Backend

Uma API RESTful desenvolvida em Python para o gerenciamento de estoque de produtos de uma distribuidora. Este projeto permite o cadastro, consulta, atualização e remoção de produtos no estoque, garantindo a integridade dos dados através de um banco de dados relacional.

A documentação interativa da API foi construída utilizando o padrão OpenAPI (Swagger), facilitando o teste e a integração das rotas.

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask
* **Documentação da API:** Flask-OpenAPI3 (Swagger UI)
* **ORM e Banco de Dados:** SQLAlchemy (SQLite)
* **Validação de Dados:** Pydantic
* **Containerização:** Docker

## Como executar com Docker (Recomendado)

A maneira mais fácil e isolada de rodar o projeto é utilizando o Docker. Certifique-se de ter o [Docker](https://www.docker.com/) instalado e rodando em sua máquina.

1. Faça o clone do repositório e acesse a pasta do projeto:
```bash
git clone [https://github.com/victorvazdev/distribuidora-smart-backend](https://github.com/victorvazdev/distribuidora-smart-backend)
cd distribuidora-smart-backend
```

2. Construa a imagem da aplicação:
```bash
docker build -t victorvazdev/distribuidora-smart-backend:1.0.0 .
```

3. Execute o container mapeando a porta 8000:
```bash
docker run -d --name ds-back -p 8000:8000 victorvazdev/distribuidora-smart-backend:1.0.0
```

A aplicação já estará rodando e pronta para acesso na porta 8000.

## Como executar o projeto localmente (Sem Docker)

Caso prefira rodar sem containers, siga as instruções abaixo para configurar o ambiente usando o Python instalado na sua máquina.

### Pré-requisitos

Certifique-se de ter o **Python 3.14.7** instalado no seu sistema. Você pode verificar sua versão rodando o seguinte comando no terminal:

```bash
python --version
```

### Passo a passo da Instalação
1. Clone o repositório:

```bash
git clone [https://github.com/victorvazdev/distribuidora-smart-backend](https://github.com/victorvazdev/distribuidora-smart-backend)
cd distribuidora-smart-backend
```

2. Crie um Ambiente Virtual:
O ambiente virtual isola as dependências deste projeto das demais instaladas no seu computador.

```bash
# No Windows:
python -m venv venv

# No macOS/Linux:
python3 -m venv venv
```

3. Ative o Ambiente Virtual:

```bash
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
```

4. Instale as dependências:
Com o ambiente ativado, instale as bibliotecas necessárias listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

### Inicializando a Aplicação
Após configurar o ambiente e instalar as dependências, inicie o servidor de desenvolvimento do Flask com o comando:

```bash
flask run --host 0.0.0.0 --port 8000
```

## Acessando a Documentação (Swagger)
Para testar as rotas e ver a documentação interativa (independente de usar Docker ou execução local), abra o seu navegador e acesse:

http://localhost:8000/openapi/swagger

## Estrutura do Projeto
```text
.
├── app.py
├── Dockerfile
├── models
│   ├── __init__.py
│   ├── base.py
│   └── product.py
├── README.md
├── requirements.txt
├── routes
│   ├── __init__.py
│   └── product_routes.py
└── schemas
    ├── __init__.py
    ├── error_schema.py
    └── product_schema.py
````
