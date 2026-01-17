# OrçaWeb - Sistema de Orçamentos

Sistema web para gestão de orçamentos desenvolvido em Python com Flask.

## Funcionalidades

- Gerenciamento de clientes com contatos e endereços
- Cadastro de itens (produtos/serviços)
- Criação e gerenciamento de orçamentos
- Sistema de login e usuários
- Interface responsiva com Bootstrap

## Instalação Local

1. Clone o repositório
2. Crie ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Execute inicialização: `python init_db.py`
6. Execute a aplicação: `python app.py`
7. Acesse http://127.0.0.1:5000

Usuário padrão: admin@example.com / admin123

## Deploy no Render

1. Crie uma conta no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. Crie um novo Web Service
4. Configure as variáveis de ambiente:
   - `DATABASE_URL`: URL do banco PostgreSQL (fornecida pelo Render)
   - `SECRET_KEY`: Chave secreta para sessões
5. Execute o script `create_tables.sql` no banco PostgreSQL do Render
6. Deploy automático

## Estrutura do Banco

O script `create_tables.sql` contém todas as tabelas necessárias para PostgreSQL.

## Sugestões

- Nome da aplicação: OrçaWeb
- Empresa: Personalizável via variáveis no template
