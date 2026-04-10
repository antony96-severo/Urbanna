from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class FormProduto(FlaskForm):

    foto = FileField("Imagem",validators=[FileRequired(),FileAllowed([  "jpg", "jpeg", "png", "webp"], "Apenas imagens!")])
    descricao = StringField("Descrição", validators=[DataRequired()])
    preco = DecimalField("Preço",places=2,validators=[DataRequired()])
    categoria = SelectField("Categoria",choices=[("masculino", "Masculino"),("feminino", "Feminino")], validators=[DataRequired(message="Selecione uma categoria.")])
    destaque = BooleanField("Aparecer na Home")
    botao = SubmitField("Publicar")



