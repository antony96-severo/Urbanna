from UrbannaSite import database
from datetime import datetime, UTC

class Produto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String(200), nullable=False)
    descricao = database.Column(database.String(300), nullable=False)
    preco = database.Column(database.Numeric(10, 2), nullable=False)
    categoria = database.Column(database.String(100), nullable=False)
    is_destaque = database.Column(database.Boolean, default=False, nullable=False)
    criado_em = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(UTC))

