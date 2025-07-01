from flask import Blueprint, render_template, jsonify
from models import get_best_laps_by_car, db

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    # List of distinct car makes for tabs
    makes = {doc.get("car") for doc in db.collection("laps").stream()}
    return render_template("index.html", makes=sorted(makes))

@public_bp.route("/car/<make>")
def car_page(make):
    return render_template("car.html", make=make)

@public_bp.route("/api/leaderboard/<make>")
def api_leaderboard(make):
    data = get_best_laps_by_car(make)
    return jsonify(data)

@public_bp.route("/api/cars")
def api_cars():
    cars = {doc.get("car") for doc in db.collection("laps").stream()}
    return jsonify(sorted(cars))
