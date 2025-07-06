from flask import Blueprint, render_template, jsonify, session, abort
from models import Car, get_best_laps_by_car, db

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    makes = {doc.id: doc.to_dict() for doc in db.collection("cars").stream()}
    return render_template(
        "index.html", cars=[Car(id, doc) for id, doc in makes.items()]
    )


@public_bp.route("/car/<make>")
def car_page(make):
    makes = {doc.id: doc.to_dict() for doc in db.collection("cars").stream()}
    if make not in makes:
        return jsonify({"error": "Car not found"}), 404
    return render_template(
        "car.html",
        car=Car(make, makes[make]),
        cars=[Car(id, doc) for id, doc in makes.items()],
    )


@public_bp.route("/api/leaderboard/<make>")
def api_leaderboard(make):
    doc = db.collection("cars").document(make).get()
    if not doc.exists:
        return jsonify({"error": "Car not found"}), 404
    data = get_best_laps_by_car(Car(make, doc))
    return jsonify(data)


@public_bp.route("/api/cars")
def api_cars():
    makes = [
        (doc.id, doc.to_dict().get("displayName"))
        for doc in db.collection("cars").stream()
    ]
    return jsonify(sorted(makes))
