# 📊 QUICK REFERENCE - Resumo Técnico em Tabelas

## 🏗️ STACK TECNOLÓGICA

| Componente | Tecnologia | Versão | Propósito |
|-----------|-----------|--------|----------|
| **Backend** | Flask | 3.1.2 | Microframework Python |
| **ORM** | SQLAlchemy | 3.1.1 (via Flask) | Mapeamento objeto-relacional |
| **Autenticação** | Flask-Login | 0.6.3 | Gerenciar sessões e login |
| **Segurança CSRF** | Flask-WTF | 1.2.2 | Proteção contra CSRF |
| **Formulários** | WTForms | (integrado) | Validação server-side |
| **Hash Senhas** | werkzeug | (integrado) | Bcrypt de senhas |
| **Frontend CSS** | Bootstrap | 5 (CDN) | Design responsivo |
| **Template Engine** | Jinja2 | (integrado) | Renderização HTML |
| **Banco Dev** | SQLite | (arquivo) | Desenvolvimento local |
| **Banco Prod** | PostgreSQL | 14+ | Produção (Render) |
| **App Server** | Gunicorn | 21.2.0 | WSGI server production |
| **DB Driver** | psycopg2 | 2.9.11 | Conexão PostgreSQL |
| **Email Valid.** | email-validator | 2.1.0 | Validação de emails |

---

## 📊 BANCO DE DADOS

### 7 Tabelas Relacionadas

| Tabela | Campos | FK | Cascade | Propósito |
|--------|--------|----|---------|---------
| **usuarios** | id, nome, email, senha_hash, ativo | - | - | Autenticação |
| **clientes** | id, nome, observacoes, criado_em | - | - | Dados clientes |
| **contatos_cliente** | id, cliente_id, tipo, valor, principal | cliente_id | ✅ | Contatos múltiplos |
| **enderecos_cliente** | id, cliente_id, logradouro, número, etc | cliente_id | ✅ | Endereços múltiplos |
| **itens** | id, nome, tipo, descricao, unidade, valor | - | - | Catálogo |
| **orcamentos** | id, cliente_id, usuario_id, endereco_id, datas, total | 3 FK | ✅ | Orçamentos |
| **orcamento_itens** | id, orcamento_id, item_id, qtd, valor | 2 FK | ✅ | Itens em orçamento |

### Relacionamentos

```
usuarios (1) ──→ (N) orcamentos
clientes (1) ──→ (N) orcamentos
clientes (1) ──→ (N) contatos_cliente
clientes (1) ──→ (N) enderecos_cliente
enderecos_cliente (1) ──→ (N) orcamentos
itens (1) ──→ (N) orcamento_itens
orcamentos (1) ──→ (N) orcamento_itens
```

---

## 🔌 ENDPOINTS (28+ Rotas)

### Autenticação (3)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/login` | Exibir form |
| POST | `/login` | Processar |
| GET | `/logout` | Desconectar |

### Usuários (6)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/usuarios` | Listar todos |
| GET | `/usuario/novo` | Form create |
| POST | `/usuario/novo` | Criar |
| GET | `/usuario/<id>/editar` | Form edit |
| POST | `/usuario/<id>/editar` | Atualizar |
| GET | `/usuario/<id>/deletar` | Deletar |

### Clientes (6)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/clientes` | Listar |
| GET | `/cliente/novo` | Form create |
| POST | `/cliente/novo` | Criar |
| GET | `/cliente/<id>` | Detalhes |
| GET | `/cliente/<id>/editar` | Form edit |
| POST | `/cliente/<id>/editar` | Atualizar |

*+ DELETE via GET `/cliente/<id>/deletar`*

### Contatos (3)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/cliente/<id>/contato/novo` | Form |
| POST | `/cliente/<id>/contato/novo` | Criar |
| GET | `/contato/<id>/editar` | Edit/Delete |

### Endereços (3)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/cliente/<id>/endereco/novo` | Form |
| POST | `/cliente/<id>/endereco/novo` | Criar |
| GET | `/endereco/<id>/editar` | Edit/Delete |

### Itens (6)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/itens` | Listar |
| GET | `/item/novo` | Form create |
| POST | `/item/novo` | Criar |
| GET | `/item/<id>/editar` | Form edit |
| POST | `/item/<id>/editar` | Atualizar |
| GET | `/item/<id>/deletar` | Deletar |

### Orçamentos (10+)
| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/orcamentos` | Listar com filtros |
| GET | `/orcamento/novo` | Form create |
| POST | `/orcamento/novo` | Criar |
| GET | `/orcamento/<id>` | Detalhes |
| GET | `/orcamento/<id>/editar` | Form edit |
| POST | `/orcamento/<id>/editar` | Atualizar |
| GET | `/orcamento/<id>/deletar` | Deletar |
| GET | `/orcamento/<id>/item/novo` | Form item |
| POST | `/orcamento/<id>/item/novo` | Adicionar item |
| GET | `/orcamento_item/<id>/editar` | Edit/Delete item |

---

## 📄 TEMPLATES (15 Arquivos)

| Template | Propósito | Herda de |
|----------|-----------|----------|
| **base.html** | Layout base com navbar/sidebar | - |
| **login.html** | Form de autenticação | base.html |
| **index.html** | Dashboard com cards | base.html |
| **usuarios.html** | Listagem de usuários | base.html |
| **usuario_form.html** | Create/Edit usuário | base.html |
| **clientes.html** | Listagem de clientes | base.html |
| **cliente_form.html** | Create/Edit cliente | base.html |
| **cliente_detalhes.html** | Detalhes + contatos + endereços | base.html |
| **contato_form.html** | Create/Edit contato | base.html |
| **endereco_form.html** | Create/Edit endereço | base.html |
| **itens.html** | Catálogo com filtros | base.html |
| **item_form.html** | Create/Edit item | base.html |
| **orcamentos.html** | Listagem com filtros | base.html |
| **orcamento_form.html** | Create/Edit + items | base.html |
| **orcamento_detalhes.html** | Visualização completa | base.html |

---

## ✅ VALIDAÇÕES

### Models (SQLAlchemy)
| Campo | Validação | Tipo |
|-------|-----------|------|
| Usuario.email | UNIQUE | PK |
| Usuario.senha_hash | NOT NULL | String |
| Cliente.nome | NOT NULL | String |
| Contato.tipo | IN ('telefone','whatsapp','email','outro') | Enum |
| Endereco.estado | 2 chars | String |
| Item.valor_unitario | > 0 | Decimal |
| Orcamento.data_validade | >= data_orcamento | Date |
| OrcamentoItem.quantidade | > 0 | Decimal |

### Forms (WTForms)
| Field | Validadores | Mensagem |
|-------|-----------|----------|
| Email | DataRequired, Email, Length | Email inválido |
| Senha | DataRequired | Campo obrigatório |
| CEP | Regex + Length | CEP inválido |
| Data | DataRequired | Data obrigatória |
| Decimal | NumberRange(min=0) | Valor inválido |

---

## 🔒 SEGURANÇA

| Aspecto | Implementação | Status |
|--------|---|--------|
| Autenticação | Flask-Login + werkzeug.security (bcrypt) | ✅ |
| CSRF | Flask-WTF em todos forms | ✅ |
| SQL Injection | SQLAlchemy ORM (parameterized) | ✅ |
| XSS | Jinja2 auto-escape | ✅ |
| Sessions | Flask-Login com timeout | ✅ |
| Senhas | Bcrypt via generate_password_hash | ✅ |
| Cookies | Secure, HttpOnly, SameSite (prod) | ✅ |

---

## 🚀 DEPLOY (Render)

### Ambiente Development
```
DATABASE_URL = sqlite:///orcamentos.db
FLASK_ENV = development
DEBUG = True
```

### Ambiente Production (Render)
```
DATABASE_URL = postgresql://user:pass@host:5432/db
FLASK_ENV = production
DEBUG = False
SECRET_KEY = (32+ chars random)
```

### Build & Start
```
Build:  pip install -r requirements.txt
Start:  gunicorn wsgi:app
Port:   3000 (Render default)
```

### PostgreSQL no Render
| Recurso | Limite (Free) | Custo |
|---------|---|---|
| Armazenamento | 256 MB | R$ 0 |
| Conexões | 5 | R$ 0 |
| Backup | Diário | R$ 0 |
| Snapshots | 7 dias | R$ 0 |

---

## 📋 FUNCIONALIDADES PRINCIPAIS

| Feature | Status | Detalhes |
|---------|--------|----------|
| Autenticação | ✅ | Email + Senha com bcrypt |
| CRUD Usuários | ✅ | Create, Read, Update, Delete |
| CRUD Clientes | ✅ | + contatos + endereços múltiplos |
| CRUD Itens | ✅ | Catálogo com tipos (produto/serviço) |
| CRUD Orçamentos | ✅ | + adição dinâmica de itens |
| Cálculo Totais | ✅ | Automático no BD |
| Dashboard | ✅ | Cards com estatísticas |
| Filtros | ✅ | Por status, data, cliente |
| Flash Messages | ✅ | Feedback de ações |
| Responsive Design | ✅ | Bootstrap 5 mobile-first |

---

## 🔧 ARQUIVOS PRINCIPAIS

| Arquivo | Linhas | Propósito |
|---------|--------|----------|
| `wsgi.py` | ~20 | Entry point Gunicorn |
| `app/__init__.py` | ~30 | Factory pattern, configs |
| `app/models.py` | ~100 | 7 models SQLAlchemy |
| `app/forms.py` | ~120 | 8+ WTForms com validação |
| `app/routes.py` | ~400+ | 28+ endpoints |
| `templates/base.html` | ~50 | Layout base |
| `templates/*.html` | ~30 cada | Templates específicos |
| `requirements.txt` | 8 linhas | Dependências exatas |
| `init_db.py` | ~40 | Inicializar BD local |
| `create_tables.sql` | ~150 | Schema PostgreSQL |

---

## 📈 MÉTRICAS DO SISTEMA

| Métrica | Valor |
|---------|-------|
| Total de Models | 7 |
| Total de Endpoints | 28+ |
| Total de Templates | 15 |
| Total de Forms | 8+ |
| Validadores Customizados | 5+ |
| Relacionamentos | 10 |
| Campos de BD | 50+ |
| Linhas de Código (Backend) | ~600 |
| Linhas de Templates | ~600 |
| Dependências | 7 |
| Versão Python | 3.10+ |

---

## 🎯 FLUXO DE DADOS

```
┌─────────────────────────────────────────────────────────┐
│                    BROWSER (User)                       │
│              (Bootstrap 5 HTML/CSS/JS)                  │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP Request
                 ↓
┌─────────────────────────────────────────────────────────┐
│              FLASK ROUTES (app/routes.py)               │
│         Validação @login_required, Query DB             │
└────────────────┬────────────────────────────────────────┘
                 │ SQLAlchemy ORM Queries
                 ↓
┌─────────────────────────────────────────────────────────┐
│           SQLALCHEMY MODELS (app/models.py)             │
│              (7 Models com Relacionamentos)             │
└────────────────┬────────────────────────────────────────┘
                 │ SQL Queries
                 ↓
┌─────────────────────────────────────────────────────────┐
│        DATABASE (SQLite dev / PostgreSQL prod)          │
│              (7 Tabelas Relacionadas)                   │
└──────────────────────────────────────────────────────────┘
```

---

## 📚 ARQUIVOS DE DOCUMENTAÇÃO CRIADOS

| Arquivo | Tipo | Tamanho | Leitura |
|---------|------|---------|---------|
| LEIA_PRIMEIRO.md | Guia Rápido | 2K | 5 min |
| RESUMO_EXECUTIVO.md | Visão Geral | 3K | 10 min |
| INDICE.md | Mapa | 4K | 15 min |
| PROMPT_SISTEMA_DETALHADO.md | Spec | 8.5K | 20 min |
| PROMPT_GENERAR_SISTEMA.md | Prompt IA | 5K | 15 min |
| INSTRUCOES_DEPLOY_RENDER.md | Deploy | 6K | 30 min |
| SQLITE_VS_POSTGRESQL.md | Análise | 3K | 10 min |
| **TOTAL** | - | **31.5K** | **105 min** |

---

## 🚀 GUIA RÁPIDO DE SETUP

```bash
# 1. Clone ou crie diretório
mkdir app-web-orcamento && cd app-web-orcamento

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicialize BD
python init_db.py

# 5. Rode aplicação
python wsgi.py

# 6. Acesse
# http://localhost:5000
# Login: admin@example.com / admin123
```

---

## 🎯 PRÓXIMOS PASSOS

1. **Entender**: Leia [PROMPT_SISTEMA_DETALHADO.md](PROMPT_SISTEMA_DETALHADO.md)
2. **Desenvolver**: Use [PROMPT_GENERAR_SISTEMA.md](PROMPT_GENERAR_SISTEMA.md) com IA
3. **Testar**: Execute localmente
4. **Deploy**: Siga [INSTRUCOES_DEPLOY_RENDER.md](INSTRUCOES_DEPLOY_RENDER.md)
5. **Produção**: Use PostgreSQL (veja [SQLITE_VS_POSTGRESQL.md](SQLITE_VS_POSTGRESQL.md))

---

**Resumo Técnico Rápido | Fevereiro 2026**
