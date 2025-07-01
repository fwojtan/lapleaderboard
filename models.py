from google.cloud import firestore
from datetime import datetime

db = firestore.Client(database="lap-leaderboard-db")

def save_lap(data: dict, user_email: str):
    data["submitted_by"] = user_email
    data["submitted_at"] = datetime.utcnow()
    db.collection("laps").add(data)

def get_best_laps_by_car(make: str):
    """
    Returns one best time per player for the given car make.
    """
    query = db.collection("laps").where("car", "==", make)
    docs = query.stream()

    best = {}
    for doc in docs:
        d = doc.to_dict()
        player = d["player"].lower()
        if player not in best or d["time"] < best[player]["time"]:
            best[player] = d
    # sort by lap time ascending
    return sorted(best.values(), key=lambda x: x["time"])
