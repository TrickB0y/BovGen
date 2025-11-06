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
        name = request.form["name"]
        estado = request.form["estado"]
        cidade = request.form["cidade"]
        propietario = request.form["propietario"]
        
        if name is None:
            error = "A fazenda precisa ter nome."
        if estado is None:
            error = "O estado precisa ser informado."
        if cidade is None:
            error = "A cidade precisa ser informado."
        if propietario is None:
            error = "O propietario precisa ser informado."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Localidades(nome_fazenda, estado, cidade, propietario)"
                    "VALUES (?, ?, ?, ?)",
                    (name, estado, cidade, propietario)
                )
                db.commit()
            except db.IntegrityError:
                error = "A fazenda já esta cadastrada."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/local/add.html")