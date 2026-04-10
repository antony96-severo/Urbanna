from flask import render_template, url_for, redirect, request, flash, session
from UrbannaSite import app, database, bcrypt
from UrbannaSite.models import Produto
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os
from UrbannaSite.forms import FormProduto


@app.route("/")
def homepage():
    destaques = (Produto.query.filter_by(is_destaque=True).order_by(Produto.id.desc()).limit(8).all())
    return render_template( "homepage.html",destaques=destaques)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/masculino")
def masculino():
    produtos = Produto.query.filter_by(categoria="masculino").order_by(Produto.id.desc()).all()
    return render_template("masculino.html", produtos=produtos)

@app.route("/feminino")
def feminino():
    produtos = Produto.query.filter_by(categoria="feminino").order_by(Produto.id.desc()).all()
    return render_template("feminino.html", produtos=produtos)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_form = request.form.get("usuario").strip()
        senha_form = request.form.get("senha").strip()

        usuario_env = os.getenv("ADMIN_USERNAME")
        senha_hash_env = os.getenv("ADMIN_PASSWORD_HASH")

        if (
            usuario_form == usuario_env and
            bcrypt.check_password_hash(senha_hash_env, senha_form)
        ):
            session["admin_logado"] = True
            return redirect(url_for("admin"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin_logado"):
        return redirect(url_for("login"))

    form = FormProduto()

    if form.validate_on_submit():
        arquivo = form.foto.data
        nome_arquivo = secure_filename(arquivo.filename)

        upload_folder = os.getenv("UPLOAD_FOLDER", "static/fotos_posts")
        pasta_destino = os.path.join(app.root_path, upload_folder)
        os.makedirs(pasta_destino, exist_ok=True)

        arquivo.save(os.path.join(pasta_destino, nome_arquivo))
        produto = Produto(imagem=nome_arquivo,descricao=form.descricao.data,preco=form.preco.data,categoria=form.categoria.data,is_destaque=form.destaque.data)

        database.session.add(produto)
        database.session.commit()

        flash("Produto publicado com sucesso!", "success")
        return redirect(url_for("admin"))

    return render_template("admin.html", form=form)

@app.route("/logout")
def logout():
    session.pop("admin_logado", None)
    return redirect(url_for("homepage"))

@app.route("/buscar")
def buscar():
    termo = request.args.get("q", "").strip()

    if not termo:
        return redirect(url_for("homepage"))

    termo_like = f"%{termo}%"

    resultados = (Produto.query.filter(or_(Produto.descricao.ilike(termo_like),Produto.categoria.ilike(termo_like))).order_by(Produto.id.desc()).all())

    return render_template("buscar.html",resultados=resultados,termo=termo)

@app.route("/deletar/<int:produto_id>", methods=["POST"])
def deletar(produto_id):
    if not session.get("admin_logado"):
        return redirect(url_for("login"))

    produto = Produto.query.get_or_404(produto_id)

    database.session.delete(produto)
    database.session.commit()

    flash("Produto excluído com sucesso.", "success")
    return redirect(url_for("admin"))