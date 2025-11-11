from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("coleta", __name__, url_prefix= "/coleta")

@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    db = get_db()
    error = None
    
    animais = db.execute(
        "SELECT * FROM Animais WHERE sexo = 'MASCULINO'"
    ).fetchall()
    
    if request.method == "POST":
        animal = request.form["coleta-animal"]
        dataColeta = request.form["coleta-data"]
        tipoColeta = request.form["coleta-tipo"]
        sucesso = request.form["coleta-sucesso"]
        exposicao = request.form["coleta-exposicao"]
        anotacao = request.form["coleta-anotacao"]
        quantidade = request.form["coleta-quantidade"]
        
        
        if animal is None:
            error = "O animal precisa ser selecionado."
        elif dataColeta is None:
            error = "A data precisa ser informada."
        elif tipoColeta is None:
            error = "O tipo precisa ser informado."
        elif sucesso is None:
            error = "O sucesso precisa ser informado."
        elif exposicao is None:
            error = "O sucesso precisa ser informado."
        
        
        if tipoColeta != 1 and tipoColeta != 2 and tipoColeta != 3:
            error = "Tipo de coleta invalida."
        
        if sucesso != "SIM" and sucesso != "NÃO":
            error = "Sucesso invalido."
        
        if exposicao != "SIM" and exposicao != "NÃO":
            error = "Sucesso invalido."    
        

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Coletas(animal_id, dataColeta, tipoColeta_id, sucesso, exposicao, anotacao, quantidade)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (animal, dataColeta, tipoColeta, sucesso, exposicao, anotacao, quantidade,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Algo deu errado."
            else:
                if
                try:
                    db.execute(
                        "INSERT INTO Coletas(animal_id, dataColeta, tipoColeta_id, sucesso, exposicao, anotacao, quantidade)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (animal, dataColeta, tipoColeta, sucesso, exposicao, anotacao, quantidade,)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                else:
    
        flash(error)