from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from BovGen.auth import login_required # type: ignore
from BovGen.db import get_db # type: ignore

bp = Blueprint("racas", __name__, url_prefix= "/")