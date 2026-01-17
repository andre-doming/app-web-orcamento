from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Usuario, Cliente, ContatoCliente, EnderecoCliente, Item, Orcamento, OrcamentoItem
from .forms import LoginForm, UsuarioForm, ClienteForm, ContatoClienteForm, EnderecoClienteForm, ItemForm, OrcamentoForm, OrcamentoItemForm
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha_hash, form.senha.data):
            login_user(usuario)
            return redirect(url_for('main.index'))
        flash('Credenciais inválidas.')
    return render_template('login.html', form=form, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Usuarios CRUD
@bp.route('/usuarios')
@login_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/usuario/novo', methods=['GET', 'POST'])
@login_required
def usuario_novo():
    form = UsuarioForm()
    if form.validate_on_submit():
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=generate_password_hash(form.senha.data),
            ativo=form.ativo.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário criado com sucesso.')
        return redirect(url_for('main.usuarios'))
    return render_template('usuario_form.html', form=form, titulo='Novo Usuário', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def usuario_editar(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        if form.senha.data:
            usuario.senha_hash = generate_password_hash(form.senha.data)
        usuario.ativo = form.ativo.data
        db.session.commit()
        flash('Usuário atualizado.')
        return redirect(url_for('main.usuarios'))
    return render_template('usuario_form.html', form=form, titulo='Editar Usuário', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/usuario/<int:id>/deletar')
@login_required
def usuario_deletar(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado.')
    return redirect(url_for('main.usuarios'))

# Clientes CRUD
@bp.route('/clientes')
@login_required
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/cliente/novo', methods=['GET', 'POST'])
@login_required
def cliente_novo():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(nome=form.nome.data, observacoes=form.observacoes.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente criado.')
        return redirect(url_for('main.clientes'))
    return render_template('cliente_form.html', form=form, titulo='Novo Cliente', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/cliente/<int:id>')
@login_required
def cliente_detalhes(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('cliente_detalhes.html', cliente=cliente, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/cliente/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.observacoes = form.observacoes.data
        db.session.commit()
        flash('Cliente atualizado.')
        return redirect(url_for('main.clientes'))
    return render_template('cliente_form.html', form=form, titulo='Editar Cliente', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/cliente/<int:id>/deletar')
@login_required
def cliente_deletar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente deletado.')
    return redirect(url_for('main.clientes'))

# Contatos do Cliente
@bp.route('/cliente/<int:cliente_id>/contato/novo', methods=['GET', 'POST'])
@login_required
def contato_cliente_novo(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = ContatoClienteForm()
    if form.validate_on_submit():
        contato = ContatoCliente(
            cliente_id=cliente_id,
            tipo=form.tipo.data,
            valor=form.valor.data,
            principal=form.principal.data
        )
        db.session.add(contato)
        db.session.commit()
        flash('Contato adicionado.')
        return redirect(url_for('main.cliente_detalhes', id=cliente_id))
    return render_template('contato_form.html', form=form, cliente=cliente, titulo='Novo Contato', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

# Enderecos do Cliente
@bp.route('/cliente/<int:cliente_id>/endereco/novo', methods=['GET', 'POST'])
@login_required
def endereco_cliente_novo(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = EnderecoClienteForm()
    if form.validate_on_submit():
        endereco = EnderecoCliente(
            cliente_id=cliente_id,
            logradouro=form.logradouro.data,
            numero=form.numero.data,
            bairro=form.bairro.data,
            cidade=form.cidade.data,
            estado=form.estado.data,
            cep=form.cep.data
        )
        db.session.add(endereco)
        db.session.commit()
        flash('Endereço adicionado.')
        return redirect(url_for('main.cliente_detalhes', id=cliente_id))
    return render_template('endereco_form.html', form=form, cliente=cliente, titulo='Novo Endereço', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

# Itens CRUD
@bp.route('/itens')
@login_required
def itens():
    itens = Item.query.all()
    return render_template('itens.html', itens=itens, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/item/novo', methods=['GET', 'POST'])
@login_required
def item_novo():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            nome=form.nome.data,
            tipo=form.tipo.data,
            descricao=form.descricao.data,
            unidade=form.unidade.data,
            valor_unitario=form.valor_unitario.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Item criado.')
        return redirect(url_for('main.itens'))
    return render_template('item_form.html', form=form, titulo='Novo Item', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/item/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def item_editar(id):
    item = Item.query.get_or_404(id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.nome = form.nome.data
        item.tipo = form.tipo.data
        item.descricao = form.descricao.data
        item.unidade = form.unidade.data
        item.valor_unitario = form.valor_unitario.data
        db.session.commit()
        flash('Item atualizado.')
        return redirect(url_for('main.itens'))
    return render_template('item_form.html', form=form, titulo='Editar Item', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/item/<int:id>/deletar')
@login_required
def item_deletar(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deletado.')
    return redirect(url_for('main.itens'))

# Orcamentos CRUD
@bp.route('/orcamentos')
@login_required
def orcamentos():
    orcamentos = Orcamento.query.all()
    return render_template('orcamentos.html', orcamentos=orcamentos, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/orcamento/novo', methods=['GET', 'POST'])
@login_required
def orcamento_novo():
    form = OrcamentoForm()
    if request.method == 'POST' and form.validate_on_submit():
        orcamento = Orcamento(
            cliente_id=form.cliente_id.data,
            usuario_id=current_user.id,
            endereco_cliente_id=form.endereco_cliente_id.data,
            data_orcamento=form.data_orcamento.data,
            data_validade=form.data_validade.data,
            valor_total=0,  # Será calculado depois
            aprovado=form.aprovado.data
        )
        db.session.add(orcamento)
        db.session.commit()
        flash('Orçamento criado.')
        return redirect(url_for('main.orcamento_detalhes', id=orcamento.id))
    return render_template('orcamento_form.html', form=form, titulo='Novo Orçamento', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/orcamento/<int:id>')
@login_required
def orcamento_detalhes(id):
    orcamento = Orcamento.query.get_or_404(id)
    item_form = OrcamentoItemForm()
    return render_template('orcamento_detalhes.html', orcamento=orcamento, item_form=item_form, app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/orcamento/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def orcamento_editar(id):
    orcamento = Orcamento.query.get_or_404(id)
    if orcamento.aprovado:
        flash('Orçamento aprovado não pode ser editado.')
        return redirect(url_for('main.orcamento_detalhes', id=id))
    form = OrcamentoForm(obj=orcamento)
    if form.validate_on_submit():
        orcamento.cliente_id = form.cliente_id.data
        orcamento.endereco_cliente_id = form.endereco_cliente_id.data
        orcamento.data_orcamento = form.data_orcamento.data
        orcamento.data_validade = form.data_validade.data
        orcamento.aprovado = form.aprovado.data
        db.session.commit()
        flash('Orçamento atualizado.')
        return redirect(url_for('main.orcamentos'))
    return render_template('orcamento_form.html', form=form, titulo='Editar Orçamento', app_nome='OrçaWeb', empresa_nome='Sua Empresa', logo_url='')

@bp.route('/orcamento/<int:id>/deletar')
@login_required
def orcamento_deletar(id):
    orcamento = Orcamento.query.get_or_404(id)
    if orcamento.aprovado:
        flash('Orçamento aprovado não pode ser deletado.')
        return redirect(url_for('main.orcamento_detalhes', id=id))
    db.session.delete(orcamento)
    db.session.commit()
    flash('Orçamento deletado.')
    return redirect(url_for('main.orcamentos'))

@bp.route('/orcamento/<int:id>/aprovar')
@login_required
def orcamento_aprovar(id):
    orcamento = Orcamento.query.get_or_404(id)
    orcamento.aprovado = True
    db.session.commit()
    flash('Orçamento aprovado.')
    return redirect(url_for('main.orcamento_detalhes', id=id))

@bp.route('/orcamento/<int:orcamento_id>/item/adicionar', methods=['POST'])
@login_required
def orcamento_item_adicionar(orcamento_id):
    orcamento = Orcamento.query.get_or_404(orcamento_id)
    if orcamento.aprovado:
        flash('Orçamento aprovado não pode ser editado.')
        return redirect(url_for('main.orcamento_detalhes', id=orcamento_id))
    form = OrcamentoItemForm()
    if form.validate_on_submit():
        item = Item.query.get(form.item_id.data)
        quantidade = form.quantidade.data
        valor_total = quantidade * item.valor_unitario
        orcamento_item = OrcamentoItem(
            orcamento_id=orcamento_id,
            item_id=form.item_id.data,
            quantidade=quantidade,
            valor_unitario=item.valor_unitario,
            valor_total=valor_total
        )
        db.session.add(orcamento_item)
        # Atualizar valor_total do orçamento
        orcamento.valor_total += valor_total
        db.session.commit()
        flash('Item adicionado.')
    return redirect(url_for('main.orcamento_detalhes', id=orcamento_id))

@bp.route('/orcamento/<int:orcamento_id>/item/<int:item_id>/remover')
@login_required
def orcamento_item_remover(orcamento_id, item_id):
    orcamento = Orcamento.query.get_or_404(orcamento_id)
    if orcamento.aprovado:
        flash('Orçamento aprovado não pode ser editado.')
        return redirect(url_for('main.orcamento_detalhes', id=orcamento_id))
    orcamento_item = OrcamentoItem.query.filter_by(orcamento_id=orcamento_id, id=item_id).first_or_404()
    orcamento.valor_total -= orcamento_item.valor_total
    db.session.delete(orcamento_item)
    db.session.commit()
    flash('Item removido.')
    return redirect(url_for('main.orcamento_detalhes', id=orcamento_id))

@bp.route('/orcamento/item/<int:item_id>/editar', methods=['POST'])
@login_required
def orcamento_item_editar(item_id):
    try:
        data = request.get_json()
        quantidade = data.get('quantidade')
        print(f"Editando item {item_id} com quantidade {quantidade}")

        if not quantidade or quantidade <= 0:
            return jsonify({'success': False, 'message': 'Quantidade inválida.'})

        orcamento_item = OrcamentoItem.query.get_or_404(item_id)
        orcamento = orcamento_item.orcamento
        if orcamento.aprovado:
            return jsonify({'success': False, 'message': 'Orçamento aprovado não pode ser editado.'})

        # Atualizar quantidade e valor_total
        orcamento.valor_total -= orcamento_item.valor_total
        orcamento_item.quantidade = quantidade
        orcamento_item.valor_total = quantidade * orcamento_item.valor_unitario
        orcamento.valor_total += orcamento_item.valor_total

        db.session.commit()
        print(f"Item {item_id} atualizado com sucesso")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Erro ao editar item {item_id}: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

# AJAX para enderecos do cliente
@bp.route('/cliente/<int:cliente_id>/enderecos')
@login_required
def cliente_enderecos(cliente_id):
    enderecos = EnderecoCliente.query.filter_by(cliente_id=cliente_id).all()
    return jsonify([{'id': e.id, 'text': f"{e.logradouro}, {e.numero} - {e.cidade}/{e.estado}"} for e in enderecos])
