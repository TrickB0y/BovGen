from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("botijoes", __name__, url_prefix= "/botijoes")

@bp.route("/all", methods=("GET",))
@login_required
def all():
    db = get_db()
    error = None
    
    botijoes = db.execute(
        "SELECT * FROM Botijoes"
    ).fetchall()
    
    return render_template("app/botijoes/all.html", botijoes=botijoes)


@bp.route("/view/<int:id>", methods=("GET",))
@login_required
def view(id):
    db = get_db()
    error = None
    
    botijao = db.execute(
        "SELECT * FROM Botijoes WHERE id = ?",
        (id,)
    ).fetchone()
    
    if botijao is None:
        return "Botijão não encontrado"
    else:
        caneco1 = db.execute(
            "SELECT * FROM Canecos WHERE id = ?",
            (botijao['caneco1_id'],)
        ).fetchone()
        
        racks_caneco1 = db.execute(
            "SELECT r.nome AS nome, "
            "r.id AS id, "
            "a.nome AS animalNome, "
            "a.id AS animalID, "
            "r.semen_id AS semen_id, "
            "r.quantidade AS quantidade, "
            "r.anotacao AS anotacao "
            "FROM Racks AS r "
            "JOIN Semens AS s ON r.semen_id = s.id "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "WHERE r.caneco_id = ?",
            (caneco1['id'],)
        ).fetchall()
        
        caneco2 = db.execute(
            "SELECT * FROM Canecos WHERE id = ?",
            (botijao['caneco2_id'],)
        ).fetchone()
        
        racks_caneco2 = db.execute(
            "SELECT r.nome AS nome, "
            "r.id AS id, "
            "a.nome AS animalNome, "
            "a.id AS animalID, "
            "r.semen_id AS semen_id, "
            "r.quantidade AS quantidade, "
            "r.anotacao AS anotacao "
            "FROM Racks AS r "
            "JOIN Semens AS s ON r.semen_id = s.id "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "WHERE r.caneco_id = ?",
            (caneco2['id'],)
        ).fetchall()
        
        caneco3 = db.execute(
            "SELECT * FROM Canecos WHERE id = ?",
            (botijao['caneco3_id'],)
        ).fetchone()
        
        racks_caneco3 = db.execute(
            "SELECT r.nome AS nome, "
            "r.id AS id, "
            "a.nome AS animalNome, "
            "a.id AS animalID, "
            "r.semen_id AS semen_id, "
            "r.quantidade AS quantidade, "
            "r.anotacao AS anotacao "
            "FROM Racks AS r "
            "JOIN Semens AS s ON r.semen_id = s.id "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "WHERE r.caneco_id = ?",
            (caneco3['id'],)
        ).fetchall()
        
        caneco4 = db.execute(
            "SELECT * FROM Canecos WHERE id = ?",
            (botijao['caneco4_id'],)
        ).fetchone()
        
        racks_caneco4 = db.execute(
            "SELECT r.nome AS nome, "
            "r.id AS id, "
            "a.nome AS animalNome, "
            "a.id AS animalID, "
            "r.semen_id AS semen_id, "
            "r.quantidade AS quantidade, "
            "r.anotacao AS anotacao "
            "FROM Racks AS r "
            "JOIN Semens AS s ON r.semen_id = s.id "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "WHERE r.caneco_id = ?",
            (caneco4['id'],)
        ).fetchall()
        
        caneco5 = db.execute(
            "SELECT * FROM Canecos WHERE id = ?",
            (botijao['caneco5_id'],)
        ).fetchone()
        
        racks_caneco5 = db.execute(
            "SELECT r.nome AS nome, "
            "r.id AS id, "
            "a.nome AS animalNome, "
            "a.id AS animalID, "
            "r.semen_id AS semen_id, "
            "r.quantidade AS quantidade, "
            "r.anotacao AS anotacao "
            "FROM Racks AS r "
            "JOIN Semens AS s ON r.semen_id = s.id "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "WHERE r.caneco_id = ?",
            (caneco5['id'],)
        ).fetchall()
        
        caneco6 = db.execute(
            "SELECT * FROM Canecos WHERE id = ?",
            (botijao['caneco6_id'],)
        ).fetchone()
        
        racks_caneco6 = db.execute(
            "SELECT r.nome AS nome, "
            "r.id AS id, "
            "a.nome AS animalNome, "
            "a.id AS animalID, "
            "r.semen_id AS semen_id, "
            "r.quantidade AS quantidade, "
            "r.anotacao AS anotacao "
            "FROM Racks AS r "
            "JOIN Semens AS s ON r.semen_id = s.id "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "WHERE r.caneco_id = ?",
            (caneco6['id'],)
        ).fetchall()
     
    return render_template("app/botijoes/view.html", 
                           botijao=botijao,
                           caneco1=caneco1,
                           racks_caneco1=racks_caneco1,
                           caneco2=caneco2,
                           racks_caneco2=racks_caneco2,
                           caneco3=caneco3,
                           racks_caneco3=racks_caneco3,
                           caneco4=caneco4,
                           racks_caneco4=racks_caneco4,
                           caneco5=caneco5,
                           racks_caneco5=racks_caneco5,
                           caneco6=caneco6,
                           racks_caneco6=racks_caneco6
                           )


@bp.route("/rack/add/<int:id>", methods=("GET","POST"))
@login_required
def addRack(id):
    db = get_db()
    error = None
    
    caneco = db.execute(
        "SELECT * FROM Canecos WHERE id = ?",
        (id,)
    ).fetchone()
    
    if caneco is None:
        return "Caneco não encontrado."
    else:
        semens = db.execute(
            "SELECT s.id AS id, a.nome AS nomeAnimal, c.dataColeta AS data, t.nome AS tipoColetaNome "
            "FROM Semens AS s "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "JOIN TiposColeta AS t ON c.tipoColeta_id = t.id"
        ).fetchall()
        
        if request.method == "POST":
            nome = request.form['nome']
            semen_id = request.form['semen_id']
            quantidade = request.form['quantidade']
            anotacao = request.form['anotacao']
            
            if nome is None or nome == "":
                error = "Nome é obrigatorio"
            elif semen_id is None or semen_id == "":
                error = "Sêmen é obrigatorio"
            elif quantidade is None or quantidade == "":
                quantidade = 0
            
            if error is None:
                try:
                    db.execute(
                        "INSERT INTO Racks(nome, botijao_id, caneco_id, semen_id, quantidade, anotacao) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (nome, caneco['botijao_id'], caneco['id'], semen_id, quantidade, anotacao,)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "algo deu errado."
                    
                return redirect(url_for('botijoes.view', id=caneco['botijao_id']))
            
        flash(error)
    return render_template("app/botijoes/rack/add.html", semens=semens)


@bp.route("/rack/edit/<int:id>", methods=("GET","POST"))
@login_required
def editRack(id):
    db = get_db()
    error = None
    
    rack = db.execute(
        "SELECT * FROM Racks WHERE id = ?",
        (id,)
    ).fetchone()
    
    if rack is None:
        return "Rack não encontrado."
    else:
        semens = db.execute(
            "SELECT s.id AS id, a.nome AS nomeAnimal, c.dataColeta AS data, t.nome AS tipoColetaNome "
            "FROM Semens AS s "
            "JOIN Coletas AS c ON s.coleta_id = c.id "
            "JOIN Animais AS a ON c.animal_id = a.id "
            "JOIN TiposColeta AS t ON c.tipoColeta_id = t.id"
        ).fetchall()
        
        if request.method == "POST":
            nome = request.form['nome']
            semen_id = request.form['semen_id']
            quantidade = request.form['quantidade']
            anotacao = request.form['anotacao']
            
            if nome is None or nome == "":
                error = "Nome é obrigatorio"
            elif semen_id is None or semen_id == "":
                error = "Sêmen é obrigatorio"
            elif quantidade is None or quantidade == "":
                quantidade = 0
            
            if error is None:
                try:
                    db.execute(
                        "UPDATE Racks SET nome = ?, semen_id = ?, quantidade = ?, anotacao = ? "
                        "WHERE id = ?",
                        (nome, semen_id, quantidade, anotacao, id,)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "algo deu errado."
                
                return redirect(url_for('botijoes.view', id=rack['botijao_id']))
            
        flash(error)
    return render_template("app/botijoes/rack/edit.html", rack=rack, semens=semens)


@bp.route("/rack/delete/<int:id>", methods=("GET","POST"))
@login_required
def deleteRack(id):
    db = get_db()
    error = None
    
    rack = db.execute(
        "SELECT * FROM Racks WHERE id = ?",
        (id,)
    ).fetchone()
    
    if rack is None:
        return "Rack não encontrado."
    else:
        if request.method == "POST":
            password = request.form["password"]
            
            user = db.execute(
            "SELECT * FROM Users WHERE id = ?",
            (session['user_id'],)
            ).fetchone()
            
            if not check_password_hash(user["password"], password):
                error = "Senha Incorreta."
            else:
                db.execute(
                    "DELETE FROM Racks WHERE id = ?",
                    (id,)
                )
                db.commit()
                
            return redirect(url_for('botijoes.view', id=rack['botijao_id']))
    flash(error)
    return render_template("app/botijoes/rack/delete.html")