from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("animais", __name__, url_prefix= "/animais")

@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    db = get_db()
    error = None

    racas = db.execute(
        "SELECT * FROM Racas"
    ).fetchall()

    localidades = db.execute(
        "SELECT * FROM Localidades"
    ).fetchall()

    machos = db.execute(
        "SELECT * FROM Animais WHERE sexo = 'MASCULINO'"
    ).fetchall()

    femeas = db.execute(
        "SELECT * FROM Animais WHERE sexo = 'FEMININO'"
    ).fetchall()

    if request.method == "POST":
        rgd = request.form["rgd"]
        raca = request.form["raca"]
        nome = request.form["nome"]
        sexo = request.form["sexo"]
        categoria = request.form["categoria"]
        nascimento = request.form["nascimento"]
        local = request.form["local"]
        pai = request.form["pai"]
        mae = request.form["mae"]
        propietario = request.form["propietario"]

        
        if rgd is None or rgd == "":
            error = "O animal precisa ter um RGD."
        elif raca is None or raca == "":
            error = "O animal precisa ter uma raça."
        elif nome is None or nome == "":
            error = "O animal precisa ter um nome."
        elif sexo is None or sexo == "":
            error = "O sexo do animal precisa ser selecionado."
        
        if sexo != "MASCULINO" and sexo != "FEMININO" and sexo != "":
            error = "Sexo invalido."
            
        if categoria != "PO" and categoria != "PA" and categoria != "":
            error = "Categoria invalida."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Animais(rgd, raca_id, nome, sexo, categoria, nascimento, localidade_id, pai_id, mae_id, propietario)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (rgd, raca, nome, sexo, categoria, nascimento, local, pai, mae, propietario,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Este RGD já esta cadastrado."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/animais/add.html", racas=racas, localidades=localidades, machos=machos, femeas=femeas)


@bp.route("/view/<int:id>", methods=("GET",))
@login_required
def view(id):
    db = get_db()

    animal = db.execute(
        "SELECT * FROM Animais WHERE id = ?",
        (id,)
    ).fetchone()

    if animal is None:
        return "Animal não encontrado."

    raca = db.execute(
        "SELECT * FROM Racas WHERE id = ?",
        (animal['raca_id'],)
    ).fetchone()

    local = db.execute(
        "SELECT * FROM Localidades WHERE id = ?",
        (animal['localidade_id'],)
    ).fetchone()

    pai = db.execute(
        "SELECT * FROM Animais WHERE id = ?",
        (animal['pai_id'],)
    ).fetchone()

    mae = db.execute(
        "SELECT * FROM Animais WHERE id = ?",
        (animal['mae_id'],)
    ).fetchone()

    return render_template("app/animais/view.html", animal=animal, raca=raca, local=local, pai=pai, mae=mae)


@bp.route("/all", methods=("GET",))
@login_required
def all():
    db = get_db()

    animais = db.execute(
        "SELECT a.*, r.name AS raca FROM Animais AS a JOIN Racas AS r ON a.raca_id = r.id"
    ).fetchall()
    return render_template("app/animais/all.html", animais=animais)


@bp.route("/edit/<int:id>", methods=("GET", "POST"))
@login_required
def edit(id):
    db = get_db()
    error = None

    animal = db.execute(
        "SELECT * FROM Animais WHERE id = ?",
        (id,)
    ).fetchone()
    print(animal)
    print(animal['nome'])

    racas = db.execute(
        "SELECT * FROM Racas"
    ).fetchall()

    localidades = db.execute(
        "SELECT * FROM Localidades"
    ).fetchall()

    machos = db.execute(
        "SELECT * FROM Animais WHERE sexo = 'MASCULINO'"
    ).fetchall()

    femeas = db.execute(
        "SELECT * FROM Animais WHERE sexo = 'FEMININO'"
    ).fetchall()

    if request.method == "POST":
        rgd = request.form["rgd"]
        raca = request.form["raca"]
        nome = request.form["nome"]
        sexo = request.form["sexo"]
        categoria = request.form["categoria"]
        nascimento = request.form["nascimento"]
        local = request.form["local"]
        pai = request.form["pai"]
        mae = request.form["mae"]
        propietario = request.form["propietario"]

        
        if rgd is None or rgd == "":
            error = "O animal precisa ter um RGD."
        elif raca is None or raca == "":
            error = "O animal precisa ter uma raça."
        elif nome is None or nome == "":
            error = "O animal precisa ter um nome."
        elif sexo is None or sexo == "":
            error = "O sexo do animal precisa ser selecionado."
        
        if sexo != "MASCULINO" and sexo != "FEMININO" and sexo != "":
            error = "Sexo invalido."
            
        if categoria != "PO" and categoria != "PA" and categoria != "":
            error = "Categoria invalida."
        
        if error is None:
            try:
                db.execute(
                    "UPDATE Animais SET rgd = ?, raca_id = ?, nome = ?, sexo = ?, categoria = ?, nascimento = ?, localidade_id = ?, pai_id = ?, mae_id = ?, propietario = ?"
                    "WHERE id = ?",
                    (rgd, raca, nome, sexo, categoria, nascimento, local, pai, mae, propietario, id,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Este RGD já esta cadastrado."
            else:
                return redirect(url_for('menu.index'))
    
        flash(error)
    return render_template("app/animais/edit.html", animal=animal, racas=racas, localidades=localidades, machos=machos, femeas=femeas)