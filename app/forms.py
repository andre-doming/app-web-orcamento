from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DecimalField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from .models import Usuario, Cliente, ContatoCliente, EnderecoCliente, Item, Orcamento

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.usuario_original = kwargs.get('obj')

    def validate_email(self, email):
        if self.usuario_original and self.usuario_original.email == email.data:
            return
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado.')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    observacoes = TextAreaField('Observações')
    submit = SubmitField('Salvar')

class ContatoClienteForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[('telefone', 'Telefone'), ('whatsapp', 'WhatsApp'), ('email', 'Email'), ('outro', 'Outro')], validators=[DataRequired()])
    valor = StringField('Valor', validators=[DataRequired(), Length(max=100)])
    principal = BooleanField('Principal')
    submit = SubmitField('Salvar')

class EnderecoClienteForm(FlaskForm):
    logradouro = StringField('Logradouro', validators=[DataRequired(), Length(max=200)])
    numero = StringField('Número', validators=[DataRequired(), Length(max=10)])
    complemento = StringField('Complemento', validators=[Length(max=100)])
    bairro = StringField('Bairro', validators=[DataRequired(), Length(max=100)])
    cidade = StringField('Cidade', validators=[DataRequired(), Length(max=100)])
    estado = StringField('Estado (UF)', validators=[DataRequired(), Length(min=2, max=2)])
    cep = StringField('CEP', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Salvar')

class ItemForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    tipo = SelectField('Tipo', choices=[('produto', 'Produto'), ('serviço', 'Serviço')], validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    unidade = StringField('Unidade', validators=[Length(max=20)], default='unidade')
    valor_unitario = DecimalField('Valor Unitário', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Salvar')

def coerce_int_or_none(value):
    if value == '' or value is None:
        return None
    return int(value)

class OrcamentoForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    endereco_cliente_id = SelectField('Endereço do Cliente', coerce=coerce_int_or_none, validate_choice=False)
    data_orcamento = DateField('Data do Orçamento', validators=[DataRequired()])
    data_validade = DateField('Data de Validade', validators=[DataRequired()])
    aprovado = BooleanField('Aprovado')
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(OrcamentoForm, self).__init__(*args, **kwargs)
        self.cliente_id.choices = [(c.id, c.nome) for c in Cliente.query.all()]
        self.endereco_cliente_id.choices = []  # Lista vazia para permitir validação dinâmica

    def validate_endereco_cliente_id(self, field):
        if not field.data:
            raise ValidationError('Selecione um endereço do cliente.')
        # Verificar se o endereço existe e pertence ao cliente selecionado
        endereco = EnderecoCliente.query.filter_by(id=field.data, cliente_id=self.cliente_id.data).first()
        if not endereco:
            raise ValidationError('Endereço inválido para o cliente selecionado.')

class OrcamentoItemForm(FlaskForm):
    item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    quantidade = DecimalField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Adicionar Item')

    def __init__(self, *args, **kwargs):
        super(OrcamentoItemForm, self).__init__(*args, **kwargs)
        self.item_id.choices = [(i.id, f"{i.nome} - R$ {i.valor_unitario}") for i in Item.query.all()]
