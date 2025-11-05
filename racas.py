from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("racas", __name__, url_prefix= "/racas")

@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    db = get_db()
    error = None
    if request.method == "POST":
        name = request.form["name"]
        
        if name is None:
            error = "A raça precisa ter nome."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Racas(name) VALUES (?)",
                    (name,)
                )
                db.commit()
            except db.IntegrityError:
                error = "A raça já existe."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/racas/add.html")


@bp.route("/view", methods=("GET",))
@login_required
def view():
    db = get_db()

    racas = db.execute(
        "SELECT * FROM Racas"
    ).fetchall()
    return render_template("app/racas/view.html", racas=racas)


@bp.route("/edit/<int:id>", methods=("GET", "POST"))
@login_required
def edit(id):
    db = get_db()
    error = None
    raca = db.execute(
        "SELECT * FROM Racas WHERE id = ?",
        (id,)
    ).fetchone()
    if raca is None:
        return "Raça não encontrada"
    if request.method == "POST":
        name = request.form["name"]
        
        if name is None:
            error = "A raça precisa ter nome."
        
        if error is None:
            try:
                db.execute(
                    "UPDATE Racas SET name = ? WHERE id = ?",
                    (name,id)
                )
                db.commit()
            except db.IntegrityError:
                error = "A raça já existe."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/racas/edit.html", raca=raca)