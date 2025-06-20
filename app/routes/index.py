from flask import Blueprint, render_template

bp = Blueprint("index", __name__)

@bp.route("/")
def go_index():
    return render_template("index.html")

@bp.route("/test")
def go_test():
    return render_template("test.html")