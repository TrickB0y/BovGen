from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore


bp = Blueprint("menu", __name__, url_prefix="/")

@bp.route("/", methods=("GET",))
@login_required
def index():
    return render_template("menu/index.html")