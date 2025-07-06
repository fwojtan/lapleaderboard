from datetime import timedelta
from flask import Blueprint, render_template, request, redirect, url_for, g, abort
from models import save_lap
from config import Config

admin_bp = Blueprint("admin", __name__)


def admin_required(view):
    def wrapper(*args, **kwargs):
        print("Session in admin_required:", session)  # Debug
        if (
            "user" not in session
            or "email" not in session["user"]
            or session["user"]["email"] not in Config.ALLOWED_ADMINS
        ):
            abort(403)
        return view(*args, **kwargs)

    wrapper.__name__ = view.__name__
    return wrapper


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin.html")


from flask import session, jsonify
from firebase_admin import auth as firebase_auth


@admin_bp.route("/login", methods=["POST"])
def admin_login():
    id_token = request.json.get("idToken")
    print("Received ID token:", id_token)
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token["email"].lower()
        name = decoded_token["name"]
        if email in Config.ALLOWED_ADMINS:
            session["user"] = {
                "email": email,
                "name": name,
            }
            print("Session set:", session)  # Debug
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Forbidden"}), 403
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid token"}), 401


@admin_bp.route("/submit", methods=["POST"])
@admin_required
def submit():
    form = request.form
    minutes = int(request.form["minutes"])
    seconds = int(request.form["seconds"])
    milliseconds = int(request.form["milliseconds"])
    time = timedelta(  # noqa: F821
        minutes=minutes, seconds=seconds, milliseconds=milliseconds
    ).total_seconds()
    lap = {
        "time": time,  # seconds or ms as float
        "car": form["car"],
        "wet": form.get("wet") == "on",
        "comment": form["comment"].strip(),
        "player": form["player"].strip(),
    }

    user = session.get("user")
    if not user:
        return redirect("/")
    save_lap(lap, user["email"])
    return redirect(url_for("admin.dashboard"))
