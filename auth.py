import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from BovGen.db import get_db # type: ignore



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('login', methods=("GET", "POST"))
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["senha"]
        db = get_db()
        error = None
        
        user = db.execute(
            "SELECT * FROM Users WHERE login = ?",
            (login,)
        ).fetchone()
        
        if user is None:
            error = "login ou senha incorretos."
            
        elif not check_password_hash(user["password"], password):
            error = "login ou senha incorretos."
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for("menu.index"))
        
        flash(error)
        
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    
    return wrapped_view