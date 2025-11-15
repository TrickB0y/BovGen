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
        animal = request.form["animal"]
        dataColeta = request.form["data"]
        tipoColeta = request.form["tipo"]
        sucesso = request.form["sucesso"]
        exposicao = request.form["exposicao"]
        anotacao = request.form["anotacao"]
        quantidade = request.form["quantidade"]
        
        tipoColetaInt = 0
        
        if animal is None or animal == "":
            error = "O animal precisa ser selecionado."
        elif dataColeta is None or dataColeta == "":
            error = "A data precisa ser informada."
        elif tipoColeta is None or tipoColeta == "":
            error = "O tipo precisa ser informado."
        elif sucesso is None or sucesso == "":
            error = "O sucesso precisa ser informado."
        elif exposicao is None or sucesso == "":
            error = "O sucesso precisa ser informado."
        
        if tipoColeta != "1" and tipoColeta != "2" and tipoColeta != "3":
            error = "Tipo invalido."
        else:
            tipoColetaInt = int(tipoColeta)
        
        if tipoColetaInt != 1 and tipoColetaInt != 2 and tipoColetaInt != 3:
            error = "Tipo de coleta invalida."
        
        if sucesso != "SIM" and sucesso != "NÃO" and sucesso != "":
            error = "Sucesso da coleta invalido."
        
        if exposicao != "SIM" and exposicao != "NÃO" and exposicao != "":
            error = "Exposição invalida."
            
        if quantidade == "":
            quantidade = 0
        
        cursor = None
        if error is None:
            try:
                cursor = db.execute(
                    "INSERT INTO Coletas(animal_id, dataColeta, tipoColeta_id, sucesso, exposicao, anotacao, quantidade)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (animal, dataColeta, tipoColetaInt, sucesso, exposicao, anotacao, quantidade,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Algo deu errado."
            
            coleta_rowid = cursor.lastrowid
            print(coleta_rowid)
            print(type(coleta_rowid))
            coleta_table = db.execute(
                "SELECT * FROM Coletas WHERE id = ?",
                (coleta_rowid,)
            ).fetchone()
            print(coleta_table['id'])
            if tipoColetaInt == 1:
                try:
                    cursor = db.execute(
                        "INSERT INTO ColetasEletroEjaculador(coleta_id)"
                        "VALUES (?)",
                        (coleta_table['id'],)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                    
                dadosColeta_rowid = cursor.lastrowid
                dadosColeta_table = db.execute(
                    "SELECT * FROM ColetasEletroEjaculador WHERE coleta_id = ?",
                    (coleta_rowid,)
                ).fetchone()
                
                try:
                    db.execute(
                        "UPDATE Coletas SET dadosColeta_id = ?"
                        "WHERE id = ?",
                        (dadosColeta_table['id'], coleta_table['id'],)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                    
                return redirect(url_for("coleta.editEletroEjaculador", id=dadosColeta_table['id']))
            
            elif tipoColetaInt == 2:
                try:
                    cursor = db.execute(
                        "INSERT INTO ColetasVaginaArtificial(coleta_id)"
                        "VALUES (?)",
                        (coleta_table['id'],)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                    
                dadosColeta_rowid = cursor.lastrowid
                dadosColeta_table = db.execute(
                    "SELECT * FROM ColetasVaginaArtificial WHERE coleta_id = ?",
                    (coleta_rowid,)
                ).fetchone()
                
                try:
                    db.execute(
                        "UPDATE Coletas SET dadosColeta_id = ?"
                        "WHERE id = ?",
                        (dadosColeta_table['id'], coleta_table['id'],)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                
                return redirect(url_for("coleta.editVaginaArtificial", id=dadosColeta_table['id']))
            elif tipoColetaInt == 3:
                try:
                    cursor = db.execute(
                        "INSERT INTO ColetasEstimulacaoManual(coleta_id)"
                        "VALUES (?)",
                        (coleta_table['id'],)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                    
                dadosColeta_rowid = cursor.lastrowid
                dadosColeta_table = db.execute(
                    "SELECT * FROM ColetasEstimulacaoManual WHERE coleta_id = ?",
                    (coleta_rowid,)
                ).fetchone()
                
                try:
                    db.execute(
                        "UPDATE Coletas SET dadosColeta_id = ?"
                        "WHERE id = ?",
                        (dadosColeta_table['id'], coleta_table['id'],)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = "Algo deu errado."
                
                return redirect(url_for("coleta.editEstimulacaoManual", id=dadosColeta_table['id']))
    
        flash(error)
    return render_template("app/coleta/add.html", animais=animais)


@bp.route("/eletroejaculador/edit/<int:id>", methods=("GET", "POST"))
@login_required
def editEletroEjaculador(id):
    db = get_db()
    error = None
    
    dadosColeta = db.execute(
        "SELECT * FROM ColetasEletroEjaculador WHERE id = ?",
        (id,)
    ).fetchone()
    
    if request.method == "POST":
        modo = request.form['modo']
        intensidade = request.form['intensidade']
        quantidadeEstimulos = request.form['quantidadeEstimulos']

        quantidadeEstimulosInt = 0
        if quantidadeEstimulos != "":
            quantidadeEstimulosInt = int(quantidadeEstimulos)
            if quantidadeEstimulosInt < 0 or quantidadeEstimulosInt > 30:
                error = "Quantidade de estimulos invalida."
            
        try:
            db.execute(
                "UPDATE ColetasEletroEjaculador SET modo = ?, intensidade = ?, quantidadeEstimulos = ?"
                "WHERE id = ?",
                (modo, intensidade, quantidadeEstimulosInt, id,)
            )
            db.commit()
        except db.IntegrityError:
            error = "Algo deu errado."
        else:
            return redirect(url_for("menu.index"))
    
        flash(error)
    return render_template("app/coleta/eletroejaculador/edit.html", dadosColeta = dadosColeta)


@bp.route("/vaginaartificial/edit/<int:id>", methods=("GET", "POST"))
@login_required
def editVaginaArtificial(id):
    db = get_db()
    error = None
    
    dadosColeta = db.execute(
        "SELECT * FROM ColetasVaginaArtificial WHERE id = ?",
        (id,)
    ).fetchone()
    
    if request.method == "POST":
        vacaORmanequim = request.form['vacaORmanequim']
        vaca = request.form['vaca']
        
        if vacaORmanequim != "VACA" and vacaORmanequim != "MANEQUIM":
            error = "Opção desconhecida."
            
        try:
            db.execute(
                "UPDATE ColetasVaginaArtificial SET vacaORmanequim = ?, vaca = ?"
                "WHERE id = ?",
                (vacaORmanequim, vaca, id,)
            )
            db.commit()
        except db.IntegrityError:
            error = "Algo deu errado."
        else:
            return redirect(url_for("menu.index"))
    
        flash(error)
    return render_template("app/coleta/vaginaartificial/edit.html", dadosColeta = dadosColeta)
    

@bp.route("/estimulacaomanual/edit/<int:id>", methods=("GET", "POST"))
@login_required
def editEstimulacaoManual(id):
    db = get_db()
    error = None
    
    dadosColeta = db.execute(
        "SELECT * FROM ColetasEstimulacaoManual WHERE id = ?",
        (id,)
    ).fetchone()
    
    if request.method == "POST":
        tempoMinutos = request.form['tempoMinutos']
        
        tempoMinutosInt = 0
        if tempoMinutos != "":
            tempoMinutosInt = int(tempoMinutos)
            if tempoMinutosInt < 0:
                error = "Tempo invalido."
        
        
            
        try:
            db.execute(
                "UPDATE ColetasEstimulacaoManual SET tempoMinutos = ?"
                "WHERE id = ?",
                (tempoMinutosInt, id,)
            )
            db.commit()
        except db.IntegrityError:
            error = "Algo deu errado."
        else:
            return redirect(url_for("menu.index"))
    
        flash(error)
    return render_template("app/coleta/estimulacaomanual/edit.html", dadosColeta = dadosColeta)
    

@bp.route("/edit/<int:id>", methods=("GET", "POST"))
@login_required
def edit(id):
    db = get_db()
    error = None
    
    sameType = False
    
    coleta = db.execute(
        "SELECT * FROM Coletas WHERE id = ?",
        (id,)
    ).fetchone()
    print(coleta)
    for i in coleta:
        print(i)
    animais = db.execute(
        "SELECT * FROM Animais WHERE sexo = 'MASCULINO'"
    ).fetchall()
    
    if request.method == "POST":
        animal = request.form["animal"]
        dataColeta = request.form["data"]
        tipoColeta = request.form["tipo"]
        sucesso = request.form["sucesso"]
        exposicao = request.form["exposicao"]
        anotacao = request.form["anotacao"]
        quantidade = request.form["quantidade"]
        
        
        
        if animal is None or animal == "":
            error = "O animal precisa ser selecionado."
        elif dataColeta is None or dataColeta == "":
            error = "A data precisa ser informada."
        elif tipoColeta is None or tipoColeta == "":
            error = "O tipo precisa ser informado."
        elif sucesso is None or sucesso == "":
            error = "O sucesso precisa ser informado."
        elif exposicao is None or sucesso == "":
            error = "O sucesso precisa ser informado."
            
        tipoColetaInt = 0
        
        if tipoColeta != "1" and tipoColeta != "2" and tipoColeta != "3" and tipoColeta != "":
            error = "Tipo invalido."
        else:
            tipoColetaInt = int(tipoColeta)
        
        if tipoColetaInt != 1 and tipoColetaInt != 2 and tipoColetaInt != 3:
            error = "Tipo de coleta invalida."
        
        if sucesso != "SIM" and sucesso != "NÃO" and sucesso != "":
            error = "Sucesso da coleta invalido."
        
        if exposicao != "SIM" and exposicao != "NÃO" and exposicao != "":
            error = "Exposição invalida."
            
        if tipoColetaInt == coleta['tipoColeta_id']:
            sameType = True
        else:
            sameType = False
        
        cursor = None
        if error is None:
            try:
                cursor = db.execute(
                    "UPDATE Coletas SET animal_id = ?, dataColeta = ?, tipoColeta_id = ?, sucesso = ?, exposicao = ?, anotacao = ?, quantidade = ?"
                    "WHERE id = ?",
                    (animal, dataColeta, tipoColetaInt, sucesso, exposicao, anotacao, quantidade, id,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Algo deu errado."
                
            if sameType:
                if tipoColetaInt == 1:
                    return redirect(url_for("coleta.editEletroEjaculador", id=coleta['dadosColeta_id']))
                elif tipoColetaInt == 2:
                    return redirect(url_for("coleta.editVaginaArtificial", id=coleta['dadosColeta_id']))
                elif tipoColetaInt == 3:
                    return redirect(url_for("coleta.editEstimulacaoManual", id=coleta['dadosColeta_id']))
            else:
                
                coletaNext = db.execute(
                    "SELECT * FROM Coletas WHERE id = ?",
                    (id,)
                ).fetchone()
                if tipoColetaInt == 1:
                    previous = db.execute(
                        "SELECT * FROM ColetasEletroEjaculador WHERE coleta_id = ?",
                        (id ,)
                    ).fetchone()
                    
                    if previous:
                        print("have previous, id = ", previous['id'])
                        try:
                            db.execute(
                                "UPDATE Coletas SET dadosColeta_id = ?"
                                "WHERE id = ?",
                                (previous['id'], id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                        
                        return redirect(url_for("coleta.editEletroEjaculador", id=previous['id']))
                    else:
                        try:
                            cursor = db.execute(
                                "INSERT INTO ColetasEletroEjaculador(coleta_id)"
                                "VALUES (?)",
                                (id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                            
                        dadosColeta_rowid = cursor.lastrowid
                        dadosColeta_table = db.execute(
                            "SELECT * FROM ColetasEletroEjaculador WHERE coleta_id = ?",
                            (id,)
                        ).fetchone()
                        
                        try:
                            db.execute(
                                "UPDATE Coletas SET dadosColeta_id = ?"
                                "WHERE id = ?",
                                (dadosColeta_table['id'], id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                            
                        return redirect(url_for("coleta.editEletroEjaculador", id=dadosColeta_table['id']))
                
                elif tipoColetaInt == 2:
                    previous = db.execute(
                        "SELECT * FROM ColetasVaginaArtificial WHERE coleta_id = ?",
                        (id ,)
                    ).fetchone()
                    
                    if previous:
                        print("have previous, id = ", previous['id'])
                        try:
                            db.execute(
                                "UPDATE Coletas SET dadosColeta_id = ?"
                                "WHERE id = ?",
                                (previous['id'], id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                        
                        return redirect(url_for("coleta.editVaginaArtificial", id=previous['id']))
                    else:
                        try:
                            cursor = db.execute(
                                "INSERT INTO ColetasVaginaArtificial(coleta_id)"
                                "VALUES (?)",
                                (id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                            
                        dadosColeta_rowid = cursor.lastrowid
                        dadosColeta_table = db.execute(
                            "SELECT * FROM ColetasVaginaArtificial WHERE coleta_id = ?",
                            (id,)
                        ).fetchone()
                        
                        try:
                            db.execute(
                                "UPDATE Coletas SET dadosColeta_id = ?"
                                "WHERE id = ?",
                                (dadosColeta_table['id'], id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                            
                        return redirect(url_for("coleta.editVaginaArtificial", id=dadosColeta_table['id']))
                    
                elif tipoColetaInt == 3:
                    previous = db.execute(
                        "SELECT * FROM ColetasEstimulacaoManual WHERE coleta_id = ?",
                        (id ,)
                    ).fetchone()
                    
                    if previous:
                        print("have previous, id = ", previous['id'])
                        try:
                            db.execute(
                                "UPDATE Coletas SET dadosColeta_id = ?"
                                "WHERE id = ?",
                                (previous['id'], id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                        
                        return redirect(url_for("coleta.editEstimulacaoManual", id=previous['id']))
                    else:
                        try:
                            cursor = db.execute(
                                "INSERT INTO ColetasEstimulacaoManual(coleta_id)"
                                "VALUES (?)",
                                (id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                            
                        dadosColeta_rowid = cursor.lastrowid
                        dadosColeta_table = db.execute(
                            "SELECT * FROM ColetasEstimulacaoManual WHERE coleta_id = ?",
                            (id,)
                        ).fetchone()
                        
                        try:
                            db.execute(
                                "UPDATE Coletas SET dadosColeta_id = ?"
                                "WHERE id = ?",
                                (dadosColeta_table['id'], id,)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = "Algo deu errado."
                            
                        return redirect(url_for("coleta.editEstimulacaoManual", id=dadosColeta_table['id']))
    
        flash(error)
    return render_template("app/coleta/edit.html", animais=animais, coleta=coleta)


@bp.route("/view/<int:id>")
@login_required
def view(id):
    db = get_db()
    
    coleta = db.execute(
        "SELECT * FROM Coletas WHERE id = ?",
        (id,)
    ).fetchone()
    dadosColeta = None
    animal = None
    tipoColeta = None
    
    if coleta is None:
        return "Coleta não encontrada"
    else:
        if coleta['tipoColeta_id'] == 1:
            dadosColeta = db.execute(
                "SELECT * FROM ColetasEletroEjaculador WHERE id = ?",
                (coleta['dadosColeta_id'],)
            ).fetchone()
            animal = db.execute(
                "SELECT * FROM Animais WHERE id = ?",
                (coleta['animal_id'],)
            ).fetchone()
            tipoColeta = db.execute(
                "SELECT * FROM TiposColeta WHERE id = ?",
                (coleta['tipoColeta_id'] ,)
            ).fetchone()
        if coleta['tipoColeta_id'] == 2:
            dadosColeta = db.execute(
                "SELECT * FROM ColetasVaginaArtificial WHERE id = ?",
                (coleta['dadosColeta_id'],)
            ).fetchone()
            animal = db.execute(
                "SELECT * FROM Animais WHERE id = ?",
                (coleta['animal_id'],)
            ).fetchone()
            tipoColeta = db.execute(
                "SELECT * FROM TiposColeta WHERE id = ?",
                (coleta['tipoColeta_id'] ,)
            ).fetchone()
        if coleta['tipoColeta_id'] == 3:
            dadosColeta = db.execute(
                "SELECT * FROM ColetasEstimulacaoManual WHERE id = ?",
                (coleta['dadosColeta_id'],)
            ).fetchone()
            animal = db.execute(
                "SELECT * FROM Animais WHERE id = ?",
                (coleta['animal_id'],)
            ).fetchone()
            tipoColeta = db.execute(
                "SELECT * FROM TiposColeta WHERE id = ?",
                (coleta['tipoColeta_id'] ,)
            ).fetchone()
    
    return render_template("app/coleta/view.html", coleta=coleta, dadosColeta=dadosColeta, animal=animal, tipoColeta=tipoColeta)


@bp.route("/all")
@login_required
def all():
    db = get_db()
    coletas = db.execute(
        "SELECT c.id as id, a.nome as animalNome, c.dataColeta as data, t.nome as tipoNome "
        "FROM Coletas AS c JOIN Animais AS a ON c.animal_id = a.id JOIN TiposColeta AS t ON c.tipoColeta_id = t.id"
    ).fetchall()
    return render_template("app/coleta/all.html", coletas=coletas)