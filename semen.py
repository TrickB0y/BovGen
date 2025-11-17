from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("semen", __name__, url_prefix= "/semen")

@bp.route("/view/<int:id>", methods=("GET",))
@login_required
def view(id):
    db = get_db()
    error = None
    
    semen = db.execute(
        "SELECT * FROM Semens WHERE id = ?",
        (id,)
    ).fetchone()
    
    if semen is None:
        return "Semen não encontrado."
    
    coleta = db.execute(
        "SELECT c.id AS id, a.nome AS nomeAnimal, c.dataColeta AS data, t.nome AS tipoColetaNome "
        "FROM Coletas AS c JOIN Animais AS a ON c.animal_id = a.id JOIN TiposColeta AS t ON c.tipoColeta_id = t.id "
        "WHERE c.id = ?",
        (semen['coleta_id'],)
    ).fetchone()
    
    flash(error)
    return render_template("app/semen/view.html", semen=semen, coleta=coleta)

@bp.route("/add", methods=("GET","POST"))
@login_required
def add():
    db = get_db()
    error = None
    
    cursor = None
    
    coletas = db.execute(
        "SELECT c.id AS id, a.nome AS nomeAnimal, c.dataColeta AS data, t.nome AS tipoColetaNome "
        "FROM Coletas AS c JOIN Animais AS a ON c.animal_id = a.id JOIN TiposColeta AS t ON c.tipoColeta_id = t.id LEFT JOIN Semens AS s "
        "ON c.id = s.coleta_id "
        "WHERE s.coleta_id IS NULL"
    ).fetchall()
    
    for coleta in coletas:
        for i in coleta:
            print(i)
        print("\n\n")
    
    if request.method == "POST":
        coleta = request.form["coleta"]

        if coleta is None or coleta == "":
            error = "Uma Coleta deve ser selecionada."
            
        semenOfSameColeta = db.execute(
            "SELECT * FROM Semens AS s JOIN Coletas AS c WHERE s.coleta_id = ?",
            (coleta,)
        ).fetchone()
        
        if semenOfSameColeta is not None:
            error = "Já existe um cadastro dessa coleta."
        
        if error is None:
            try:
                cursor = db.execute(
                    "INSERT INTO Semens(coleta_id) VALUES (?)",
                    (coleta,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Já existe um cadastro dessa coleta."
            
            semenID = cursor.lastrowid
            
            try:
                cursor = db.execute(
                    "INSERT INTO SemensCaracteristicas(semen_id) VALUES (?)",
                    (semenID,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Já existe caracteristicas do mesmo semen."
            
            semenCaracteristicasID = cursor.lastrowid
            
            try:
                cursor = db.execute(
                    "INSERT INTO SemensParametrosDoConjunto(semen_id) VALUES (?)",
                    (semenID,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Já existe parametros do conjunto do mesmo semen."
                
            semenParametrosDoConjuntoID = cursor.lastrowid
            
            try:
                cursor = db.execute(
                    "INSERT INTO SemensMorfologiaEspermatica(semen_id) VALUES (?)",
                    (semenID,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Já existe morfologia espermatica do mesmo semen."
                
            semenMorfologiaEspermaticaID = cursor.lastrowid
            
            try:
                db.execute(
                    "UPDATE Semens SET semenCaracteristicas_id = ?, semenParametrosDoConjunto_id = ?, semenMorfologiaEspermatica_id = ?"
                    "WHERE id = ?",
                    (semenCaracteristicasID, semenParametrosDoConjuntoID, semenMorfologiaEspermaticaID, semenID)
                )
                db.commit()
            except db.IntegrityError:
                error = "Já contem cacteristicas ou parametros ou morfologia espermatica cadastrados no mesmo semen."
                
            return redirect(url_for("semen.view", id=semenID))
        flash(error)
    return render_template("app/semen/add.html", coletas=coletas)

@bp.route("/caracteristicas/edit/<int:id>", methods=("GET","POST"))
@login_required
def editCaracteristicas(id):
    db = get_db()
    error = None
    
    caracteristicas = db.execute(
        "SELECT * FROM SemensCaracteristicas WHERE id = ?",
        (id,)
    ).fetchone()
    
    if caracteristicas is None:
        return "Caracteristicas não encontradas."
    
    if request.method == "POST":
        contaminacao = request.form["contaminacao"]
        quantidade = request.form["quantidade"]
        consistencia = request.form["consistencia"]
        peso = request.form["peso"]
        cor = request.form["cor"]
        anotacao = request.form["anotacao"]
        
        if contaminacao != "" and contaminacao != "SIM" and contaminacao != "NÃO":
            error = "Contaminação inválida."
            
        if quantidade == "" or quantidade == None:
            quantidade = 0
        
        if consistencia != "" and consistencia != "CREMOSO" and consistencia != "AQUOSO":
            error = "Consistência inválida."
        
        if peso == "" or peso == None:
            peso = 0
            
        if cor != "" and cor != "BRANCO" and cor != "AMARELO" and cor != "ACINZENTADO":
            error = "Cor inválida."
            
        if error is None:
            try:
                db.execute(
                    "UPDATE SemensCaracteristicas SET contaminacao = ?, quantidade = ?, consistencia = ?, peso = ?, cor = ?, anotacao = ?"
                    "WHERE id = ?",
                    (contaminacao, quantidade, consistencia, peso, cor, anotacao, id,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Algo deu errado."
            else:
                return redirect(url_for('semen.view', id=caracteristicas['semen_id']))
        
        flash(error)
    return render_template("app/semen/caracteristicas/edit.html", caracteristicas=caracteristicas)

@bp.route("/parametrosdoconjunto/edit/<int:id>", methods=("GET","POST"))
@login_required
def editParametrosDoConjunto(id):
    db = get_db()
    error = None
    
    parametrosDoConjunto = db.execute(
        "SELECT * FROM SemensParametrosDoConjunto WHERE id = ?",
        (id,)
    ).fetchone()
    
    if parametrosDoConjunto is None:
        return "Parametros do conjunto não encontradas."
    
    if request.method == "POST":
        motilidade = request.form["motilidade"]
        motilidadeAprovacao = request.form["motilidadeAprovacao"]
        vigor = request.form["vigor"]
        vigorAprovacao = request.form["vigorAprovacao"]
        concentracao = request.form["concentracao"]
        concentracaoAprovacao = request.form["concentracaoAprovacao"]
        
        if motilidade == "" or motilidade == None:
            motilidade = 0
            
        if motilidadeAprovacao != "" and motilidadeAprovacao != "SIM" and motilidadeAprovacao != "NÃO":
            error = "Aprovação de motilidade inválida."
            
        if vigor == "" or vigor == None:
            vigor = 0
        
        if vigorAprovacao != "" and vigorAprovacao != "SIM" and vigorAprovacao != "NÃO":
            error = "Aprovação de vigor inválida."
        
        if concentracao == "" or concentracao == None:
            concentracao = 0
        
        if concentracaoAprovacao != "" and concentracaoAprovacao != "SIM" and concentracaoAprovacao != "NÃO":
            error = "Aprovação de concentração inválida."
            
        if error is None:
            try:
                db.execute(
                    "UPDATE SemensParametrosDoConjunto SET motilidade = ?, motilidadeAprovacao = ?, vigor = ?, vigorAprovacao = ?, concentracao = ?, concentracaoAprovacao = ?"
                    "WHERE id = ?",
                    (motilidade, motilidadeAprovacao, vigor, vigorAprovacao, concentracao, concentracaoAprovacao, id,)
                )
                db.commit()
            except db.IntegrityError:
                error = "Algo deu errado."
            else:
                return redirect(url_for('semen.view', id=parametrosDoConjunto['semen_id']))
        
        flash(error)
    return render_template("app/semen/parametrosdoconjunto/edit.html", parametrosDoConjunto=parametrosDoConjunto)

@bp.route("/morfologiaespermatica/edit/<int:id>", methods=("GET","POST"))
@login_required
def editMorfologiaEspermatica(id):
    db = get_db()
    error = None
    
    morfologiaEspermatica = db.execute(
        "SELECT * FROM SemensMorfologiaEspermatica WHERE id = ?",
        (id,)
    ).fetchone()
    
    if morfologiaEspermatica is None:
        return "Parametros do conjunto não encontradas."
    
    if request.method == "POST":
        normalContagem = request.form["normalContagem"]
        acromossomaContagem = request.form["acromossomaContagem"]
        gotaProximalContagem = request.form["gotaProximalContagem"]
        cabecaPequenaContagem = request.form["cabecaPequenaContagem"]
        caldaEnroladaCabecaContagem = request.form["caldaEnroladaCabecaContagem"]
        cabecaIsoladaPatologicaContagem = request.form["cabecaIsoladaPatologicaContagem"]
        cabecaEstreitaBaseContagem = request.form["cabecaEstreitaBaseContagem"]
        cabecaPiriformeContagem = request.form["cabecaPiriformeContagem"]
        cabecaPequenaNormalContagem = request.form["cabecaPequenaNormalContagem"]
        cabecaColoracaoAnormalContagem = request.form["cabecaColoracaoAnormalContagem"]
        cabecaContornoAnormalContagem = request.form["cabecaContornoAnormalContagem"]
        pouchFormationContagem = request.form["pouchFormationContagem"]
        cabecaUlceradaContagem = request.form["cabecaUlceradaContagem"]
        caldaDobradaContagem = request.form["caldaDobradaContagem"]
        formasTeratogenicaContagem = request.form["formasTeratogenicaContagem"]
        pecaIntermediariaContagem = request.form["pecaIntermediariaContagem"]
        caldaFortementeDobradaContagem = request.form["caldaFortementeDobradaContagem"]
        caldaDobradaGotaDistalContagem = request.form["caldaDobradaGotaDistalContagem"]
        cabecaDelgadaContagem = request.form["cabecaDelgadaContagem"]
        cabecaGiganteContagem = request.form["cabecaGiganteContagem"]
        cabecaIsoladaNormalContagem = request.form["cabecaIsoladaNormalContagem"]
        abaxialContagem = request.form["abaxialContagem"]
        obliquoContagem = request.form["obliquoContagem"]
        gotaDistalContagem = request.form["gotaDistalContagem"]
        totalAprovado = request.form["totalAprovado"]
        
        if normalContagem == "" or normalContagem == None:
            normalContagem = 0
            
        if acromossomaContagem == "" or acromossomaContagem == None:
            acromossomaContagem = 0
            
        if gotaProximalContagem == "" or gotaProximalContagem == None:
            gotaProximalContagem = 0
            
        if cabecaPequenaContagem == "" or cabecaPequenaContagem == None:
            cabecaPequenaContagem = 0
            
        if caldaEnroladaCabecaContagem == "" or caldaEnroladaCabecaContagem == None:
            caldaEnroladaCabecaContagem = 0
            
        if cabecaIsoladaPatologicaContagem == "" or cabecaIsoladaPatologicaContagem == None:
            cabecaIsoladaPatologicaContagem = 0
            
        if cabecaEstreitaBaseContagem == "" or cabecaEstreitaBaseContagem == None:
            cabecaEstreitaBaseContagem = 0
            
        if cabecaPiriformeContagem == "" or cabecaPiriformeContagem == None:
            cabecaPiriformeContagem = 0
            
        if cabecaPequenaNormalContagem == "" or cabecaPequenaNormalContagem == None:
            cabecaPequenaNormalContagem = 0
            
        if cabecaColoracaoAnormalContagem == "" or cabecaColoracaoAnormalContagem == None:
            cabecaColoracaoAnormalContagem = 0
            
        if cabecaContornoAnormalContagem == "" or cabecaContornoAnormalContagem == None:
            cabecaContornoAnormalContagem = 0
            
        if pouchFormationContagem == "" or pouchFormationContagem == None:
            pouchFormationContagem = 0
            
        if cabecaUlceradaContagem == "" or cabecaUlceradaContagem == None:
            cabecaUlceradaContagem = 0
            
        if caldaDobradaContagem == "" or caldaDobradaContagem == None:
            caldaDobradaContagem = 0
            
        if formasTeratogenicaContagem == "" or formasTeratogenicaContagem == None:
            formasTeratogenicaContagem = 0
            
        if pecaIntermediariaContagem == "" or pecaIntermediariaContagem == None:
            pecaIntermediariaContagem = 0
            
        if caldaFortementeDobradaContagem == "" or caldaFortementeDobradaContagem == None:
            caldaFortementeDobradaContagem = 0
            
        if caldaDobradaGotaDistalContagem == "" or caldaDobradaGotaDistalContagem == None:
            caldaDobradaGotaDistalContagem = 0
            
        if cabecaDelgadaContagem == "" or cabecaDelgadaContagem == None:
            cabecaDelgadaContagem = 0
            
        if cabecaGiganteContagem == "" or cabecaGiganteContagem == None:
            cabecaGiganteContagem = 0
            
        if cabecaIsoladaNormalContagem == "" or cabecaIsoladaNormalContagem == None:
            cabecaIsoladaNormalContagem = 0
            
        if abaxialContagem == "" or abaxialContagem == None:
            abaxialContagem = 0
            
        if obliquoContagem == "" or obliquoContagem == None:
            obliquoContagem = 0
            
        if gotaDistalContagem == "" or gotaDistalContagem == None:
            gotaDistalContagem = 0
        
        
        
        if totalAprovado != "" and totalAprovado != "SIM" and totalAprovado != "NÃO":
            error = "Aprovação inválida."
            
        
        if error is None:
            try:
                db.execute(
                    "UPDATE SemensMorfologiaEspermatica SET "
                    "normalContagem = ?, "
                    "acromossomaContagem = ?, "
                    "gotaProximalContagem = ?, "
                    "cabecaPequenaContagem = ?, "
                    "caldaEnroladaCabecaContagem = ?, "
                    "cabecaIsoladaPatologicaContagem = ?, "
                    "cabecaEstreitaBaseContagem = ?, "
                    "cabecaPiriformeContagem = ?, "
                    "cabecaPequenaNormalContagem = ?, "
                    "cabecaColoracaoAnormalContagem = ?, "
                    "cabecaContornoAnormalContagem = ?, "
                    "pouchFormationContagem = ?, "
                    "cabecaUlceradaContagem = ?, "
                    "caldaDobradaContagem = ?, "
                    "formasTeratogenicaContagem = ?, "
                    "pecaIntermediariaContagem = ?, "
                    "caldaFortementeDobradaContagem = ?, "
                    "caldaDobradaGotaDistalContagem = ?, "
                    "cabecaDelgadaContagem = ?, "
                    "cabecaGiganteContagem = ?, "
                    "cabecaIsoladaNormalContagem = ?, "
                    "abaxialContagem = ?, "
                    "obliquoContagem = ?, "
                    "gotaDistalContagem = ?, "
                    "totalAprovado = ? "
                    "WHERE id = ?",
                    (
                        normalContagem,
                        acromossomaContagem,
                        gotaProximalContagem,
                        cabecaPequenaContagem,
                        caldaEnroladaCabecaContagem,
                        cabecaIsoladaPatologicaContagem,
                        cabecaEstreitaBaseContagem,
                        cabecaPiriformeContagem,
                        cabecaPequenaNormalContagem,
                        cabecaColoracaoAnormalContagem,
                        cabecaContornoAnormalContagem,
                        pouchFormationContagem,
                        cabecaUlceradaContagem,
                        caldaDobradaContagem,
                        formasTeratogenicaContagem,
                        pecaIntermediariaContagem,
                        caldaFortementeDobradaContagem,
                        caldaDobradaGotaDistalContagem,
                        cabecaDelgadaContagem,
                        cabecaGiganteContagem,
                        cabecaIsoladaNormalContagem,
                        abaxialContagem,
                        obliquoContagem,
                        gotaDistalContagem,
                        totalAprovado,
                        id,
                    )
                )
                db.commit()
            except db.IntegrityError:
                error = "Algo deu errado."
            else:
                return redirect(url_for('semen.view', id=morfologiaEspermatica['semen_id']))
        
        flash(error)
    return render_template("app/semen/morfologiaespermatica/edit.html", morfologiaEspermatica=morfologiaEspermatica)

@bp.route("/caracteristicas/view/<int:id>", methods=("GET",))
@login_required
def viewCaracteristicas(id):
    db = get_db()
    error = None
    
    caracteristicas = db.execute(
        "SELECT * FROM SemensCaracteristicas WHERE id = ?",
        (id,)
    ).fetchone()
    
    if caracteristicas is None:
        return "Caracteristicas não encontradas."
    
    return render_template("app/semen/caracteristicas/view.html", caracteristicas=caracteristicas)

@bp.route("/parametrosdoconjunto/view/<int:id>", methods=("GET",))
@login_required
def viewParametrosDoConjunto(id):
    db = get_db()
    error = None
    
    parametrosDoConjunto = db.execute(
        "SELECT * FROM SemensParametrosDoConjunto WHERE id = ?",
        (id,)
    ).fetchone()
    
    if parametrosDoConjunto is None:
        return "Parametros não encontrados."
    
    return render_template("app/semen/parametrosdoconjunto/view.html", parametrosDoConjunto=parametrosDoConjunto)

@bp.route("/morfologiaespermatica/view/<int:id>", methods=("GET",))
@login_required
def viewMorfologiaEspermatica(id):
    db = get_db()
    error = None
    
    morfologiaEspermatica = db.execute(
        "SELECT * FROM SemensMorfologiaEspermatica WHERE id = ?",
        (id,)
    ).fetchone()
    
    if morfologiaEspermatica is None:
        return "Morfologia espermatica não encontrada."
    
    return render_template("app/semen/morfologiaespermatica/view.html", morfologiaEspermatica=morfologiaEspermatica)

@bp.route("/all", methods=("GET",))
@login_required
def all():
    db = get_db()
    semens = db.execute(
        "SELECT s.id as id, a.nome as animalNome, c.dataColeta as data, t.nome as tipoNome "
        "FROM Semens AS s JOIN Coletas AS c ON s.coleta_id = c.id JOIN Animais AS a ON c.animal_id = a.id JOIN TiposColeta AS t ON c.tipoColeta_id = t.id"
    ).fetchall()
    return render_template("app/semen/all.html", semens=semens)