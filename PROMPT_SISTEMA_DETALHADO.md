# 📋 Prompt Detalhado para Sistema de Orçamentos (OrçaWeb)

## Visão Geral
Sistema web completo para gerenciamento de orçamentos, desenvolvido com Flask, SQLAlchemy e Bootstrap 5. Suporta múltiplos usuários, clientes com endereços e contatos, itens de catálogo e criação de orçamentos com rastreamento.

---

## 🏗️ Stack Tecnológica

### Backend
- **Framework**: Flask 3.1.2 (Python Web Framework)
- **ORM**: SQLAlchemy (via Flask-SQLAlchemy 3.1.1) - Mapeamento de banco de dados
- **Autenticação**: Flask-Login 0.6.3 - Gerenciamento de sessões e autenticação de usuários
- **Segurança CSRF**: Flask-WTF 1.2.2 - Proteção contra ataques CSRF
- **Validação de Formulários**: WTForms (integrado com Flask-WTF) - Validação server-side de dados
- **Server Web**: Gunicorn 21.2.0 - WSGI application server para produção
- **Database Driver**: psycopg2-binary 2.9.11 - Driver PostgreSQL para Python

### Frontend
- **Framework CSS**: Bootstrap 5 (via CDN) - Design responsivo e componentes
- **Linguagem Template**: Jinja2 (integrado ao Flask) - Template rendering no backend
- **Responsividade**: Mobile-first design, totalmente responsivo

### Banco de Dados
- **Desenvolvimento**: SQLite (arquivo local `orcamentos.db`)
- **Produção (Render)**: PostgreSQL 14+ (banco fornecido pelo Render)

### Deploy
- **Plataforma**: Render (render.com) - PaaS com suporte nativo a Flask
- **Linguagem Runtime**: Python 3.10+
- **Build Command**: Automático via `requirements.txt`
- **Start Command**: `gunicorn wsgi:app`

---

## 📊 Estrutura do Banco de Dados

### Tabela: `usuarios`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(100) | NOT NULL | Nome completo do usuário |
| email | VARCHAR(120) | NOT NULL, UNIQUE | Email único para autenticação |
| senha_hash | VARCHAR(255) | NOT NULL | Hash bcrypt da senha (nunca armazenar em plaintext) |
| ativo | BOOLEAN | DEFAULT TRUE | Flag para ativar/desativar usuário |

**Relacionamentos**: `1:N` com Orcamento

---

### Tabela: `clientes`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(100) | NOT NULL | Nome da empresa/pessoa física |
| observacoes | TEXT | NULL | Notas gerais sobre o cliente |
| criado_em | DATETIME | DEFAULT NOW() | Timestamp de criação |

**Relacionamentos**: 
- `1:N` com ContatoCliente (cascade delete)
- `1:N` com EnderecoCliente (cascade delete)
- `1:N` com Orcamento (cascade delete)

---

### Tabela: `contatos_cliente`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| cliente_id | INTEGER | FK(clientes.id), NOT NULL | Referência ao cliente |
| tipo | VARCHAR(20) | NOT NULL | Tipo: 'telefone', 'whatsapp', 'email', 'outro' |
| valor | VARCHAR(100) | NOT NULL | Número/email do contato |
| principal | BOOLEAN | DEFAULT FALSE | Marca contato principal do cliente |

**Relacionamentos**: `N:1` com Cliente (parent)

---

### Tabela: `enderecos_cliente`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| cliente_id | INTEGER | FK(clientes.id), NOT NULL | Referência ao cliente |
| logradouro | VARCHAR(200) | NOT NULL | Rua, avenida, etc. |
| numero | VARCHAR(10) | NOT NULL | Número do imóvel |
| complemento | VARCHAR(100) | NULL | Apto, sala, etc. |
| bairro | VARCHAR(100) | NOT NULL | Bairro |
| cidade | VARCHAR(100) | NOT NULL | Cidade |
| estado | VARCHAR(2) | NOT NULL | UF (ex: SP, RJ, MG) |
| cep | VARCHAR(10) | NOT NULL | CEP (formato: 12345-678) |

**Relacionamentos**: 
- `N:1` com Cliente (parent)
- `1:N` com Orcamento (referência de endereço de entrega)

---

### Tabela: `itens`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(100) | NOT NULL | Nome do produto/serviço |
| tipo | VARCHAR(20) | NOT NULL | Tipo: 'produto' ou 'serviço' |
| descricao | TEXT | NULL | Descrição detalhada |
| unidade | VARCHAR(20) | DEFAULT 'unidade' | Unidade de medida (un, m², kg, hora, etc.) |
| valor_unitario | NUMERIC(10,2) | NOT NULL | Preço unitário (R$ máximo 99.999.999,99) |

**Relacionamentos**: `1:N` com OrcamentoItem (cascade delete)

---

### Tabela: `orcamentos`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| cliente_id | INTEGER | FK(clientes.id), NOT NULL | Referência ao cliente |
| usuario_id | INTEGER | FK(usuarios.id), NOT NULL | Usuário que criou o orçamento |
| endereco_cliente_id | INTEGER | FK(enderecos_cliente.id), NOT NULL | Endereço de entrega/local da obra |
| data_orcamento | DATE | NOT NULL | Data de emissão do orçamento |
| data_validade | DATE | NOT NULL | Data até quando o orçamento é válido |
| valor_total | NUMERIC(10,2) | NOT NULL | Soma de todos os itens (calculado) |
| aprovado | BOOLEAN | DEFAULT FALSE | Flag indicando aprovação do cliente |

**Relacionamentos**: 
- `N:1` com Cliente (parent)
- `N:1` com Usuario (parent)
- `N:1` com EnderecoCliente (parent)
- `1:N` com OrcamentoItem (cascade delete)

---

### Tabela: `orcamento_itens`
| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| orcamento_id | INTEGER | FK(orcamentos.id), NOT NULL | Referência ao orçamento |
| item_id | INTEGER | FK(itens.id), NOT NULL | Referência ao item de catálogo |
| quantidade | NUMERIC(10,2) | NOT NULL | Quantidade do item (ex: 2,5 para 2,5m²) |
| valor_unitario | NUMERIC(10,2) | NOT NULL | Preço unitário no momento do orçamento |
| valor_total | NUMERIC(10,2) | NOT NULL | quantidade × valor_unitario (calculado) |

**Relacionamentos**: 
- `N:1` com Orcamento (parent, cascade delete)
- `N:1` com Item (parent)

---

## 🎨 Estrutura de Templates (Frontend)

### Layout Base: `base.html`
- Navbar com logo e menu principal
- Sidebar com navegação CRUD (Usuários, Clientes, Itens, Orçamentos)
- Link de logout
- Bootstrap 5 + CSS customizado
- Responsive design (mobile-first)
- Flash messages para feedback do usuário

### Templates CRUD

#### 1. **`login.html`**
- Form de login com email e senha
- Validação client-side e server-side
- Link "Esqueci a senha" (opcional)
- Design limpo e centralizado

#### 2. **`index.html`** (Dashboard)
- Bem-vindo ao usuário logado
- Cards com resumo: Total de Clientes, Total de Orçamentos, Orçamentos Aprovados
- Links rápidos para ações principais
- Gráficos ou estatísticas (opcional)

#### 3. **Usuários**
- `usuarios.html`: Lista todos com botões Editar/Deletar
- `usuario_form.html`: Form para criar/editar (reutilizável)
  - Campos: Nome, Email, Senha, Ativo
  - Validação de email único
  - Confirmação de senha

#### 4. **Clientes**
- `clientes.html`: Lista de clientes com busca/filtro
- `cliente_form.html`: Form para criar/editar
  - Campos: Nome, Observações
- `cliente_detalhes.html`: Detalhes completos
  - Contatos do cliente (tabela com botões Add/Edit/Delete)
  - Endereços do cliente (tabela com botões Add/Edit/Delete)
  - Orçamentos do cliente (tabela com links)

#### 5. **Contatos**
- `contato_form.html`: Embedded form
  - Campo tipo (select: Telefone, WhatsApp, Email, Outro)
  - Campo valor
  - Checkbox para "Principal"

#### 6. **Endereços**
- `endereco_form.html`: Embedded form
  - Campos: Logradouro, Número, Complemento, Bairro, Cidade, Estado, CEP
  - Validação de CEP com regex

#### 7. **Itens**
- `itens.html`: Catalogo de itens com busca/filtro por tipo
- `item_form.html`: Form para criar/editar
  - Campos: Nome, Tipo (select), Descrição, Unidade, Valor Unitário
  - Tabela com Editar/Deletar

#### 8. **Orçamentos**
- `orcamentos.html`: Lista com filtros
  - Status (Aprovado/Pendente)
  - Data range
  - Cliente
- `orcamento_form.html`: Criar/editar orçamento
  - Campos: Cliente (select), Endereço (dinâmico), Data do Orçamento, Data de Validade, Aprovado
  - Seção para adicionar itens (tabela dinâmica)
  - Botão "Adicionar Item" que abre modal/form
- `orcamento_detalhes.html`: Visualização completa
  - Dados do cliente, endereço, datas
  - Tabela de itens com preços
  - Valor total calculado
  - Botão de aprovação/edição/exclusão
  - Opção de imprimir/exportar PDF (opcional)

---

## 🔐 Funcionalidades de Autenticação e Autorização

### Login
- Email + Senha com hash bcrypt (werkzeug.security)
- Sessão Flask-Login com timeout configurável
- CSRF protection em todos os forms
- Redirect para login se não autenticado (@login_required)

### Permissões
- Todos os usuários logados têm acesso às mesmas funcionalidades (sem roles/permissions diferenciadas no escopo inicial)
- Futuro: Implementar roles (Admin, Vendedor, Cliente)

---

## 🔌 Endpoints da API REST / Routes

### Autenticação
```
GET  /login                        → login.html
POST /login                        → Validar credenciais, criar sessão
GET  /logout                       → Limpar sessão, redirect login
```

### Usuários
```
GET    /usuarios                   → Lista de usuários
GET    /usuario/novo               → Form novo usuário
POST   /usuario/novo               → Criar usuário
GET    /usuario/<id>/editar        → Form editar usuário
POST   /usuario/<id>/editar        → Atualizar usuário
GET    /usuario/<id>/deletar       → Deletar usuário (com confirmação)
```

### Clientes
```
GET    /clientes                   → Lista de clientes
GET    /cliente/novo               → Form novo cliente
POST   /cliente/novo               → Criar cliente
GET    /cliente/<id>               → Detalhes do cliente
GET    /cliente/<id>/editar        → Form editar cliente
POST   /cliente/<id>/editar        → Atualizar cliente
GET    /cliente/<id>/deletar       → Deletar cliente
```

### Contatos
```
GET    /cliente/<id>/contato/novo          → Form novo contato
POST   /cliente/<id>/contato/novo          → Criar contato
GET    /contato/<id>/editar                → Form editar contato
POST   /contato/<id>/editar                → Atualizar contato
GET    /contato/<id>/deletar               → Deletar contato
```

### Endereços
```
GET    /cliente/<id>/endereco/novo         → Form novo endereço
POST   /cliente/<id>/endereco/novo         → Criar endereço
GET    /endereco/<id>/editar               → Form editar endereço
POST   /endereco/<id>/editar               → Atualizar endereço
GET    /endereco/<id>/deletar              → Deletar endereço
```

### Itens
```
GET    /itens                      → Lista de itens
GET    /item/novo                  → Form novo item
POST   /item/novo                  → Criar item
GET    /item/<id>/editar           → Form editar item
POST   /item/<id>/editar           → Atualizar item
GET    /item/<id>/deletar          → Deletar item
```

### Orçamentos
```
GET    /orcamentos                 → Lista de orçamentos com filtros
GET    /orcamento/novo             → Form novo orçamento
POST   /orcamento/novo             → Criar orçamento
GET    /orcamento/<id>             → Detalhes do orçamento
GET    /orcamento/<id>/editar      → Form editar orçamento
POST   /orcamento/<id>/editar      → Atualizar orçamento
GET    /orcamento/<id>/deletar     → Deletar orçamento
GET    /orcamento/<id>/item/novo   → Adicionar item ao orçamento
POST   /orcamento/<id>/item/novo   → Criar relação item-orçamento
GET    /orcamento_item/<id>/editar → Editar quantidade/preço
POST   /orcamento_item/<id>/editar → Atualizar
GET    /orcamento_item/<id>/deletar → Remover item do orçamento
```

---

## 📁 Estrutura de Diretórios Esperada

```
app-web-orcamento/
├── app/
│   ├── __init__.py              # Inicialização Flask + Factory Pattern
│   ├── models.py                # Modelos SQLAlchemy (Usuario, Cliente, Orcamento, etc)
│   ├── routes.py                # Blueprints e rotas (endpoints)
│   ├── forms.py                 # Formulários WTForms
│   └── __pycache__/
├── templates/                    # Templates HTML Jinja2
│   ├── base.html                # Layout base com navbar/sidebar
│   ├── login.html
│   ├── index.html               # Dashboard
│   ├── usuarios.html
│   ├── usuario_form.html
│   ├── clientes.html
│   ├── cliente_form.html
│   ├── cliente_detalhes.html
│   ├── contato_form.html
│   ├── endereco_form.html
│   ├── itens.html
│   ├── item_form.html
│   ├── orcamentos.html
│   ├── orcamento_form.html
│   └── orcamento_detalhes.html
├── static/                       # Arquivos estáticos
│   ├── logo.png                 # Logo da empresa
│   ├── css/
│   │   └── custom.css           # CSS customizado
│   └── js/
│       └── main.js              # JavaScript personalizado
├── instance/                     # Pasta de instância (não versionada)
│   └── orcamentos.db            # Banco SQLite (desenvolvimento)
├── wsgi.py                      # Arquivo de inicialização para Gunicorn
├── init_db.py                   # Script para inicializar banco com dados padrão
├── create_tables.sql            # Script SQL para criar tabelas PostgreSQL
├── migrate_add_complemento.py    # Script de migração (exemplo)
├── requirements.txt             # Dependências Python
└── README.md                    # Documentação do projeto
```

---

## ⚙️ Configuração para Deploy no Render

### Variáveis de Ambiente (Environment Variables)

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/dbname` | URL da conexão PostgreSQL (fornecida pelo Render) |
| `SECRET_KEY` | String aleatória longa (min 32 chars) | Chave secreta para sessões e CSRF |
| `FLASK_ENV` | `production` | Modo de execução |
| `ADMIN_EMAIL` | `admin@example.com` | Email do usuário admin padrão |
| `ADMIN_PASSWORD` | Senha forte | Senha do admin (gerar nova em produção) |

### Configuração Render Web Service

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn wsgi:app
```

**Port:** 3000 (padrão Render, listening em `0.0.0.0:3000`)

**Environment Variables**: Configurar pelo painel Render
- DATABASE_URL (PostgreSQL fornecido)
- SECRET_KEY (gerar via `python -c "import secrets; print(secrets.token_hex(32))"`)
- FLASK_ENV = production
- ADMIN_EMAIL
- ADMIN_PASSWORD

### Passos de Deploy

1. **Preparar repositório GitHub**
   - Fazer push de todo o código
   - Incluir `.gitignore` com `instance/`, `__pycache__/`, `.env`, `venv/`

2. **Criar PostgreSQL no Render**
   - Services → PostgreSQL
   - Nome: `orcaweb-db`
   - Region: São Paulo ou próxima
   - Render fornecerá DATABASE_URL

3. **Criar Web Service no Render**
   - Services → Web Services → Connect from GitHub
   - Selecionar repositório
   - Region: Mesmo da DB
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Adicionar variáveis de ambiente
   - Deploy

4. **Inicializar Banco**
   - Ejecutar SQL manualmente no PostgreSQL:
     ```bash
     psql -U postgres -h host -d orcaweb < create_tables.sql
     ```
   - Ou executar via Python:
     ```python
     flask db upgrade
     ```

---

## 🚀 Funcionalidades Principais

### 1. Gerenciamento de Usuários
- ✅ Create: Novo usuário com email único
- ✅ Read: Listar todos os usuários
- ✅ Update: Editar nome, email, senha, status
- ✅ Delete: Remover usuário (sem cascade em orcamentos, apenas marca como inativo)
- 🔒 Autenticação: Login com email/senha

### 2. Gerenciamento de Clientes
- ✅ Create: Novo cliente
- ✅ Read: Listar, visualizar detalhes
- ✅ Update: Editar dados
- ✅ Delete: Remover cliente
- 📍 Contatos múltiplos (telefone, WhatsApp, email)
- 📦 Endereços múltiplos com campos completos (CEP, UF, etc)
- 📝 Observações gerais

### 3. Catálogo de Itens
- ✅ Create: Novo produto/serviço
- ✅ Read: Listar itens
- ✅ Update: Editar preço, descrição, unidade
- ✅ Delete: Remover item (sem cascade em orçamentos, apenas marca como inativo)
- 🏷️ Tipos: Produto ou Serviço
- 📏 Unidades de medida personalizáveis

### 4. Criação de Orçamentos
- ✅ Create: Novo orçamento com cliente, endereço, datas
- ✅ Read: Listar, visualizar com detalhes completos
- ✅ Update: Editar dados, quantidade de itens, preços
- ✅ Delete: Remover orçamento
- ➕ Adicionar/remover itens dinamicamente
- 💰 Cálculo automático de total
- ✔️ Marcar como aprovado
- 📅 Validade do orçamento

### 5. Dashboard/Home
- Bem-vindo ao usuário
- Cards com estatísticas:
  - Total de clientes
  - Total de orçamentos
  - Orçamentos aprovados
  - Orçamentos pendentes

---

## 💾 Dados e Validações

### Validações de Negócio
- Email único para usuários
- CEP válido (formato)
- Datas: `data_orcamento` ≤ `data_validade`
- Quantidade > 0 em itens de orçamento
- Valores > 0 em preços
- Cliente obrigatório em orçamento
- Endereço do cliente obrigatório em orçamento

### Validações de Form (WTForms)
- Email válido (formato RFC)
- Campos obrigatórios
- Comprimentos máximos/mínimos de strings
- Tipos de dados (Numeric, Date, Select)
- Mensagens de erro customizadas

---

## 🎯 Requisitos de UI/UX

### Responsividade
- Mobile-first design
- Bootstrap 5 grid system (12 colunas)
- Navbar colapsável em mobile
- Tables com scroll horizontal em mobile
- Botões com padding adequado

### Acessibilidade
- Labels associadas aos inputs
- ARIA labels onde necessário
- Contraste adequado de cores
- Focus states visíveis

### Feedback do Usuário
- Flash messages (success, error, warning, info)
- Loading spinners em ações longas
- Confirmações de delete
- Validação de form em tempo real (opcional)

### Componentes
- Navbar com logo + marca + menu
- Sidebar com navegação
- Cards para resumos
- Tabelas com actions (Edit/Delete)
- Forms validados
- Modals para ações críticas
- Breadcrumbs para navegação

---

## 📋 Endpoints de Dados Dinâmicos (JSON)

**Opcional**: Implementar endpoints que retornam JSON para AJAX:

```javascript
GET /api/cliente/<id>/enderecos  → JSON array de endereços
GET /api/cliente/<id>/contatos   → JSON array de contatos
GET /api/itens                    → JSON array de itens
POST /api/orcamento/<id>/item    → Adicionar item via AJAX
```

---

## 🔧 Melhorias Futuras (Out of Scope)

- [ ] Geração de PDF de orçamento
- [ ] Email de confirmação de orçamento
- [ ] Sistema de roles/permissões (Admin, Vendedor, Cliente)
- [ ] Histórico de alterações (audit log)
- [ ] Importação/exportação de dados (CSV, Excel)
- [ ] Relatórios de vendas
- [ ] Assinatura digital de orçamentos
- [ ] API REST pública

---

## ✅ Checklist de Desenvolvimento

- [ ] Setup inicial: Criar app Flask com factory pattern
- [ ] Configurar banco SQLite/PostgreSQL
- [ ] Implementar models (7 tabelas com relacionamentos)
- [ ] Criar forms com validações
- [ ] Implementar rotas CRUD (7 entidades × 4 operações = ~28 rotas)
- [ ] Criar templates HTML base com Bootstrap 5
- [ ] Implementar login/autenticação
- [ ] Testar CRUD completo
- [ ] Configurar deploy Render (DB + Web Service)
- [ ] Testar em produção

---

## 📝 Observações Importantes

### PostgreSQL vs SQLite
- **Desenvolvimento**: SQLite é mais rápido e sem setup
- **Produção (Render)**: PostgreSQL é recomendado pelo Render e oferece melhor performance/segurança
- **Compatibilidade**: SQLAlchemy abstrai as diferenças, apenas ajuste `DATABASE_URL`

### Segurança
- ✅ Hash de senhas com werkzeug.security
- ✅ CSRF protection com Flask-WTF
- ✅ SQL Injection protection com SQLAlchemy ORM
- ✅ XSS protection com Jinja2 auto-escaping
- ⚠️ HTTPS no Render (ativar automaticamente)
- ⚠️ Não commitir `.env` ou secrets

### Performance
- Usar lazy loading com SQLAlchemy (`lazy=True`)
- Indexes em foreign keys e campos de busca
- Pagination em tabelas grandes (futuro)
- Cache de itens frequentes (futuro)

### Migrations
- Usar Alembic para versionamento de schema (futuro)
- Script `create_tables.sql` para setup inicial
- `migrate_add_complemento.py` como exemplo

---

## 🚀 Commands de Desenvolvimento

```bash
# Setup inicial
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco
python init_db.py

# Rodar aplicação (dev)
python wsgi.py

# Rodar com Gunicorn (produção local)
gunicorn wsgi:app

# Acessar
http://localhost:5000 (dev)
http://localhost:8000 (gunicorn)
```

---

## 📞 Suporte

Para recriação do sistema:
1. Clonar esta estrutura exatamente
2. Seguir stack tecnológica especificada
3. Implementar todos os endpoints listados
4. Usar templates com Bootstrap 5
5. Testar CRUD completo antes de deploy
6. Deploy no Render com variáveis de ambiente configuradas

---

**Versão**: 1.0  
**Data**: Fevereiro 2026  
**Stack**: Flask 3.1 + SQLAlchemy + Bootstrap 5 + PostgreSQL/SQLite
