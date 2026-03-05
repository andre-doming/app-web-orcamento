# 🎯 Prompt Otimizado para Geração de Sistema (Copy & Paste)

## Para usar com Claude, ChatGPT, GitHub Copilot ou outra IA

---

## PROMPT COMPLETO:

```
Você é um engenheiro de software experiente. Crie um sistema web completo de gerenciamento de 
orçamentos do ZERO com as especificações EXATAS abaixo.

═══════════════════════════════════════════════════════════════════════════════════

## 📋 OBJETIVO
Desenvolver "OrçaWeb" - Sistema web de gerenciamento de orçamentos com múltiplos usuários,
clientes com contatos/endereços, catálogo de itens e criação de orçamentos.

═══════════════════════════════════════════════════════════════════════════════════

## 🏗️ STACK TECNOLÓGICA EXIGIDA

### Backend
- Framework: Flask 3.1.2 (Python Web Framework)
- ORM: SQLAlchemy (Flask-SQLAlchemy 3.1.1)
- Autenticação: Flask-Login 0.6.3
- Segurança CSRF: Flask-WTF 1.2.2
- Validação de Forms: WTForms integrado
- Hash de Senhas: werkzeug.security
- Server Production: Gunicorn 21.2.0
- Database Driver: psycopg2-binary 2.9.11 (PostgreSQL)

### Frontend
- CSS Framework: Bootstrap 5 (via CDN)
- Template Engine: Jinja2 (integrado ao Flask)
- Design: Mobile-first, totalmente responsivo

### Banco de Dados
- Desenvolvimento: SQLite (arquivo local)
- Produção: PostgreSQL 14+ (Render)

═══════════════════════════════════════════════════════════════════════════════════

## 📊 MODELO DE DADOS (7 Tabelas com Relacionamentos)

### 1. TABELA: usuarios
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - nome (VARCHAR 100, NOT NULL) - Nome do usuário
  - email (VARCHAR 120, NOT NULL, UNIQUE) - Email único
  - senha_hash (VARCHAR 255, NOT NULL) - Hash bcrypt da senha
  - ativo (BOOLEAN, DEFAULT TRUE) - Flag de ativação

Relacionamentos:
  - 1:N com orcamentos

─────────────────────────────────────────────────────────────────

### 2. TABELA: clientes
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - nome (VARCHAR 100, NOT NULL) - Nome da empresa/pessoa
  - observacoes (TEXT, NULL) - Notas gerais
  - criado_em (DATETIME, DEFAULT NOW()) - Timestamp

Relacionamentos:
  - 1:N com contatos_cliente (cascade delete)
  - 1:N com enderecos_cliente (cascade delete)
  - 1:N com orcamentos (cascade delete)

─────────────────────────────────────────────────────────────────

### 3. TABELA: contatos_cliente
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - cliente_id (INTEGER, FOREIGN KEY clientes.id, NOT NULL)
  - tipo (VARCHAR 20, NOT NULL) - 'telefone', 'whatsapp', 'email', 'outro'
  - valor (VARCHAR 100, NOT NULL) - Número/email do contato
  - principal (BOOLEAN, DEFAULT FALSE) - Contato principal

Relacionamentos:
  - N:1 com clientes (parent)

─────────────────────────────────────────────────────────────────

### 4. TABELA: enderecos_cliente
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - cliente_id (INTEGER, FOREIGN KEY clientes.id, NOT NULL)
  - logradouro (VARCHAR 200, NOT NULL) - Rua/Avenida
  - numero (VARCHAR 10, NOT NULL) - Número
  - complemento (VARCHAR 100, NULL) - Apto/Sala
  - bairro (VARCHAR 100, NOT NULL)
  - cidade (VARCHAR 100, NOT NULL)
  - estado (VARCHAR 2, NOT NULL) - UF
  - cep (VARCHAR 10, NOT NULL)

Relacionamentos:
  - N:1 com clientes (parent)
  - 1:N com orcamentos (referência)

─────────────────────────────────────────────────────────────────

### 5. TABELA: itens
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - nome (VARCHAR 100, NOT NULL) - Nome do produto/serviço
  - tipo (VARCHAR 20, NOT NULL) - 'produto' ou 'serviço'
  - descricao (TEXT, NULL)
  - unidade (VARCHAR 20, DEFAULT 'unidade') - Unidade de medida
  - valor_unitario (NUMERIC 10,2, NOT NULL) - Preço unitário

Relacionamentos:
  - 1:N com orcamento_itens (cascade delete)

─────────────────────────────────────────────────────────────────

### 6. TABELA: orcamentos
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - cliente_id (INTEGER, FOREIGN KEY clientes.id, NOT NULL)
  - usuario_id (INTEGER, FOREIGN KEY usuarios.id, NOT NULL)
  - endereco_cliente_id (INTEGER, FOREIGN KEY enderecos_cliente.id, NOT NULL)
  - data_orcamento (DATE, NOT NULL)
  - data_validade (DATE, NOT NULL)
  - valor_total (NUMERIC 10,2, NOT NULL) - Calculado automaticamente
  - aprovado (BOOLEAN, DEFAULT FALSE)

Relacionamentos:
  - N:1 com clientes (parent)
  - N:1 com usuarios (parent)
  - N:1 com enderecos_cliente (parent)
  - 1:N com orcamento_itens (cascade delete)

─────────────────────────────────────────────────────────────────

### 7. TABELA: orcamento_itens
Campos:
  - id (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - orcamento_id (INTEGER, FOREIGN KEY orcamentos.id, NOT NULL)
  - item_id (INTEGER, FOREIGN KEY itens.id, NOT NULL)
  - quantidade (NUMERIC 10,2, NOT NULL)
  - valor_unitario (NUMERIC 10,2, NOT NULL) - Preço no momento
  - valor_total (NUMERIC 10,2, NOT NULL) - quantidade × valor_unitario

Relacionamentos:
  - N:1 com orcamentos (parent, cascade delete)
  - N:1 com itens (parent)

═══════════════════════════════════════════════════════════════════════════════════

## 🔐 AUTENTICAÇÃO & AUTORIZAÇÃO

- Sistema de Login com email + senha
- Hash de senha usando werkzeug.security (bcrypt)
- Proteção CSRF em todos os forms
- Sessões Flask-Login com timeout
- Decorator @login_required em todas as rotas (exceto login)
- Todos os usuários logados têm acesso igual (sem roles diferenciadas ainda)

═══════════════════════════════════════════════════════════════════════════════════

## 🔌 ENDPOINTS / ROTAS (28+ rotas)

### Autenticação
GET   /login                          → Mostrar form login
POST  /login                          → Processar login
GET   /logout                         → Logout e redirect

### Usuários (CRUD)
GET   /usuarios                       → Listar todos
GET   /usuario/novo                   → Form novo
POST  /usuario/novo                   → Criar
GET   /usuario/<id>/editar            → Form editar
POST  /usuario/<id>/editar            → Atualizar
GET   /usuario/<id>/deletar           → Deletar

### Clientes (CRUD)
GET   /clientes                       → Listar
GET   /cliente/novo                   → Form novo
POST  /cliente/novo                   → Criar
GET   /cliente/<id>                   → Detalhes
GET   /cliente/<id>/editar            → Form editar
POST  /cliente/<id>/editar            → Atualizar
GET   /cliente/<id>/deletar           → Deletar

### Contatos (CRUD aninhado)
GET   /cliente/<id>/contato/novo      → Form novo contato
POST  /cliente/<id>/contato/novo      → Criar contato
GET   /contato/<id>/editar            → Form editar
POST  /contato/<id>/editar            → Atualizar
GET   /contato/<id>/deletar           → Deletar

### Endereços (CRUD aninhado)
GET   /cliente/<id>/endereco/novo     → Form novo endereço
POST  /cliente/<id>/endereco/novo     → Criar endereço
GET   /endereco/<id>/editar           → Form editar
POST  /endereco/<id>/editar           → Atualizar
GET   /endereco/<id>/deletar          → Deletar

### Itens (CRUD)
GET   /itens                          → Listar
GET   /item/novo                      → Form novo
POST  /item/novo                      → Criar
GET   /item/<id>/editar               → Form editar
POST  /item/<id>/editar               → Atualizar
GET   /item/<id>/deletar              → Deletar

### Orçamentos (CRUD + Itens aninhados)
GET   /orcamentos                     → Listar com filtros
GET   /orcamento/novo                 → Form novo
POST  /orcamento/novo                 → Criar
GET   /orcamento/<id>                 → Detalhes
GET   /orcamento/<id>/editar          → Form editar
POST  /orcamento/<id>/editar          → Atualizar
GET   /orcamento/<id>/deletar         → Deletar
GET   /orcamento/<id>/item/novo       → Form adicionar item
POST  /orcamento/<id>/item/novo       → Criar relação
GET   /orcamento_item/<id>/editar     → Form editar item
POST  /orcamento_item/<id>/editar     → Atualizar
GET   /orcamento_item/<id>/deletar    → Remover item

═══════════════════════════════════════════════════════════════════════════════════

## 🎨 TEMPLATES HTML (Bootstrap 5)

### Estrutura Base
1. base.html
   - Navbar com logo, marca, menu
   - Sidebar com navegação CRUD
   - Link logout
   - Bootstrap 5 + CSS custom
   - Responsive mobile-first

### Templates Específicos (15 templates)
1. login.html - Form login (email + senha)
2. index.html - Dashboard com cards de estatísticas
3. usuarios.html - Lista de usuários
4. usuario_form.html - Form create/edit usuário
5. clientes.html - Lista de clientes
6. cliente_form.html - Form create/edit cliente
7. cliente_detalhes.html - Detalhes do cliente + contatos + endereços
8. contato_form.html - Form create/edit contato
9. endereco_form.html - Form create/edit endereço
10. itens.html - Catálogo de itens
11. item_form.html - Form create/edit item
12. orcamentos.html - Lista com filtros
13. orcamento_form.html - Form create/edit + adicionar itens
14. orcamento_detalhes.html - Visualização completa
15. Componentes reutilizáveis: tables, forms, alerts

### Requisitos de UI/UX
- Bootstrap 5 grid (12 colunas)
- Navbar colapsável em mobile
- Tables com scroll horizontal em mobile
- Flash messages (success, error, warning)
- Confirmações de delete
- Validação de form (WTForms)
- Acessibilidade (labels, aria, contraste)

═══════════════════════════════════════════════════════════════════════════════════

## 📁 ESTRUTURA DE ARQUIVOS

app-web-orcamento/
├── app/
│   ├── __init__.py              # Factory pattern, db init, login manager
│   ├── models.py                # 7 modelos SQLAlchemy
│   ├── routes.py                # Todos os endpoints
│   └── forms.py                 # Todos os WTForms
├── templates/
│   ├── base.html                # Layout base
│   ├── login.html
│   ├── index.html
│   ├── usuarios.html, usuario_form.html
│   ├── clientes.html, cliente_form.html, cliente_detalhes.html
│   ├── contato_form.html
│   ├── endereco_form.html
│   ├── itens.html, item_form.html
│   ├── orcamentos.html, orcamento_form.html, orcamento_detalhes.html
├── static/
│   ├── logo.png
│   ├── css/custom.css
│   └── js/main.js
├── instance/
│   └── orcamentos.db            # SQLite dev
├── wsgi.py                      # Entry point Gunicorn
├── init_db.py                   # Script inicializar DB
├── create_tables.sql            # Script SQL PostgreSQL
├── requirements.txt             # Dependencies
├── .gitignore
└── README.md

═══════════════════════════════════════════════════════════════════════════════════

## ✅ FUNCIONALIDADES PRINCIPAIS

### Usuários
✓ Create novo usuário
✓ Read listar/visualizar
✓ Update editar dados
✓ Delete remover
✓ Login/Logout
✓ Email único
✓ Senha hasheada
✓ Status ativo/inativo

### Clientes
✓ CRUD completo
✓ Múltiplos contatos por cliente
✓ Múltiplos endereços por cliente
✓ Observações gerais
✓ Timestamp de criação

### Contatos
✓ CRUD aninhado (sob cliente)
✓ Tipos: telefone, whatsapp, email, outro
✓ Marcar como principal
✓ Validação de valor

### Endereços
✓ CRUD aninhado (sob cliente)
✓ Campos completos: logradouro, número, complemento, bairro, cidade, estado, CEP
✓ Validação de UF (2 chars)
✓ Validação de CEP

### Itens
✓ CRUD de catálogo
✓ Tipos: produto ou serviço
✓ Descrição detalhada
✓ Unidade de medida customizável
✓ Valor unitário
✓ Busca/filtro por tipo

### Orçamentos
✓ CRUD de orçamentos
✓ Seleção de cliente (valida)
✓ Seleção de endereço (dinâmico)
✓ Datas: emissão e validade
✓ Adicionar/remover itens dinamicamente
✓ Cálculo automático de total
✓ Marcar como aprovado
✓ Validações de datas (emissão ≤ validade)

### Dashboard
✓ Bem-vindo ao usuário logado
✓ Cards com estatísticas:
  - Total de clientes
  - Total de orçamentos
  - Orçamentos aprovados
  - Orçamentos pendentes

═══════════════════════════════════════════════════════════════════════════════════

## 🔒 VALIDAÇÕES

### Validações de Negócio
- Email único para usuários
- CEP formato válido
- data_orcamento ≤ data_validade
- Quantidade > 0 em itens
- Valores > 0 em preços
- Cliente obrigatório em orçamento
- Endereço cliente obrigatório em orçamento
- Estado deve ter 2 caracteres

### Validações WTForms
- Email formato RFC (DataRequired, Email)
- Campos obrigatórios (DataRequired)
- Comprimento de strings (Length)
- Tipos de dados corretos (Numeric, Date, Select)
- Mensagens de erro customizadas
- Validadores customizados em forms

═══════════════════════════════════════════════════════════════════════════════════

## 🚀 INSTRUÇÕES ESPECÍFICAS

### Configuração Inicial (app/__init__.py)
- Factory pattern com create_app()
- SQLAlchemy com pool_size, pool_recycle, pool_pre_ping
- Flask-Login com user_loader
- CSRF Protection
- Suporte a SQLite (dev) e PostgreSQL (prod)
- DATABASE_URL via environment variable

### Models (app/models.py)
- UserMixin em Usuario para Flask-Login
- Relacionamentos com backref e lazy
- Cascade deletes onde apropriado
- Timestamps em criado_em

### Forms (app/forms.py)
- FlaskForm em todas as classes
- Validadores customizados onde necessário
- Email único em UsuarioForm
- SelectFields com coerce para IDs
- Campos de data com DateField
- Campos de decimal com DecimalField

### Routes (app/routes.py)
- Blueprint com nome 'main'
- Todos os endpoints como listado
- Login required em rotas protegidas
- Flash messages em cada ação (create, update, delete)
- Render template com variáveis: app_nome='OrçaWeb', empresa_nome, logo_url
- Validação 404 com get_or_404()

### Templates
- Herdar de base.html
- Bootstrap 5 classes
- Flash messages macro ({% with messages = get_flashed_messages() %})
- Forms com CSRF token automático ({{ form.csrf_token }})
- Validação de campo (form.field.errors)
- Links com url_for()
- Tabelas com Editar/Deletar buttons
- Forms com POST method

═══════════════════════════════════════════════════════════════════════════════════

## 📦 REQUIREMENTS.TXT

Exato:
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
psycopg2-binary==2.9.11
email-validator==2.1.0
gunicorn==21.2.0

═══════════════════════════════════════════════════════════════════════════════════

## 🎯 PRIORIDADES DE DESENVOLVIMENTO

1. Models e Database Schema (7 tabelas com relacionamentos)
2. Forms com validações
3. Routes CRUD básico
4. Login/Autenticação
5. Templates base (base.html)
6. Templates CRUD (list, form, detail)
7. Flash messages e feedback
8. Testes manuais completos

═══════════════════════════════════════════════════════════════════════════════════

## ⚠️ IMPORTANTES

- Debug=False em produção
- SECRET_KEY deve ser variável de ambiente
- DATABASE_URL para PostgreSQL em produção
- Nunca commitir .env
- Usar psycopg2-binary NOT psycopg2
- Cascade delete em relacionamentos apropriados
- Pool de conexão em produção

═══════════════════════════════════════════════════════════════════════════════════

Gere o código COMPLETO, FUNCIONAL, pronto para rodar.
Inclua TODOS os arquivos: models, forms, routes, templates.
Use EXATAMENTE as versões de bibliotecas listadas.
Siga o structure de arquivos especificado.
Implemente TODAS as funcionalidades descritas.

```

---

## 💡 COMO USAR ESTE PROMPT

### Com Claude / ChatGPT Web
1. Copie o prompt completo acima
2. Cole na janela de chat
3. Clique enviar
4. Aguarde a IA gerar o código
5. Salve cada arquivo nos locais corretos

### Com GitHub Copilot no VS Code
1. Crie um arquivo `PROMPT.txt`
2. Cole o prompt
3. Use em conversas
4. Copilot gerará o código

### Com API OpenAI / Anthropic
```python
import anthropic

client = anthropic.Anthropic(api_key="sua-api-key")

prompt = """[Cole aqui o prompt completo]"""

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=8000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(message.content[0].text)
```

---

## 📊 O QUE VOCÊ RECEBERÁ

- ✅ Arquivo `app/__init__.py` completo
- ✅ Arquivo `app/models.py` com 7 models
- ✅ Arquivo `app/forms.py` com 8+ forms
- ✅ Arquivo `app/routes.py` com 28+ rotas
- ✅ 15 templates HTML com Bootstrap 5
- ✅ `wsgi.py` configurado
- ✅ `requirements.txt`
- ✅ `init_db.py` para inicializar
- ✅ Estrutura pronta para rodar localmente e fazer deploy

---

## 🔗 REFERÊNCIAS ÚTEIS

- Flask Docs: https://flask.palletsprojects.com
- SQLAlchemy: https://docs.sqlalchemy.org
- WTForms: https://wtforms.readthedocs.io
- Bootstrap 5: https://getbootstrap.com/docs/5.0
- Render Deploy: https://docs.render.com

---

**Próxima etapa após gerar código:**
1. Crie pasta `app-web-orcamento/`
2. Crie subpastas: `app/`, `templates/`, `static/css`, `static/js`
3. Salve cada arquivo no local correto
4. Execute `python init_db.py`
5. Execute `python wsgi.py`
6. Acesse http://localhost:5000
7. Login com admin@example.com / admin123

---

**Criado em**: Fevereiro 2026  
**Para**: Recriação de sistema OrçaWeb do zero com máxima assertividade
