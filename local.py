from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("local", __name__, url_prefix= "/local")

@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    db = get_db()
    error = None
    if request.method == "POST":
        nome_fazenda = request.form["nome_fazenda"]
        estado = request.form["estado"]
        cidade = request.form["cidade"]
        
        if nome_fazenda is None:
            error = "A fazenda precisa ter nome."
        if estado is None:
            error = "O estado precisa ser informado."
        if cidade is None:
            error = "A cidade precisa ser informado."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Localidades(nome_fazenda, estado, cidade)"
                    "VALUES (?, ?, ?)",
                    (nome_fazenda, estado, cidade,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Existe uma fazenda com mesmo nome."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/local/add.html")


@bp.route("/all", methods=("GET",))
@login_required
def all():
    db = get_db()

    localidades = db.execute(
        "SELECT * FROM Localidades"
    ).fetchall()
    return render_template("app/local/all.html", localidades=localidades)

@bp.route("/view/<int:id>", methods=("GET",))
@login_required
def view(id):
    db = get_db()

    local = db.execute(
        "SELECT * FROM Localidades WHERE id = ?",
        (id,)
    ).fetchone()

    if local is None:
        return "Local não encontrado."
    
    return render_template("app/local/view.html", local=local)

@bp.route("/edit/<int:id>", methods=("GET", "POST"))
@login_required
def edit(id):
    db = get_db()
    error = None
    
    local = db.execute(
        "SELECT * FROM Localidades WHERE id = ?",
        (id,)
    ).fetchone()

    if local is None:
        return "Local não encontrado"

    if request.method == "POST":
        nome_fazenda = request.form["nome_fazenda"]
        estado = request.form["estado"]
        cidade = request.form["cidade"]
        
        if nome_fazenda is None:
            error = "A fazenda precisa ter nome."
        elif estado is None:
            error = "O estado precisa ser informado."
        elif cidade is None:
            error = "A cidade precisa ser informado."
        
        if error is None:
            try:
                db.execute(
                    "UPDATE Localidades SET nome_fazenda = ?, estado = ?, cidade = ?"
                    "WHERE id = ?",
                    (nome_fazenda, estado, cidade, id)
                )
                db.commit()
            except db.IntegrityError:
                error = "Existe uma fazenda com mesmo nome."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/local/edit.html", local=local)