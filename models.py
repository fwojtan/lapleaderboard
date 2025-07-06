from google.cloud import firestore
from datetime import datetime

db = firestore.Client(database="lap-leaderboard-db")


class Car:
    displayName: str
    id: str
    acceleration: float
    braking: float
    handling: float
    launch: float
    speed: float
    image: str

    def __init__(self, id, doc):
        print("init", id, doc)

        self.displayName = doc.get("displayName")
        self.acceleration = doc.get("acceleration")
        self.braking = doc.get("braking")
        self.handling = doc.get("handling")
        self.launch = doc.get("launch")
        self.speed = doc.get("speed")
        self.image = doc.get("image")
        self.id = id

    def __lt__(self, other):
        self.id < other.id


def save_lap(data: dict, user_email: str):
    data["submitted_by"] = user_email
    data["submitted_at"] = datetime.utcnow()
    db.collection("laps").add(data)


def get_best_laps_by_car(car: Car):
    """
    Returns one best time per player for the given car make.
    """
    query = db.collection("laps").where("car", "==", car.id)
    docs = query.stream()

    best = {}
    for doc in docs:
        d = doc.to_dict()
        player = d["player"].lower()
        if player not in best or d["time"] < best[player]["time"]:
            best[player] = d
    # sort by lap time ascending
    return sorted(best.values(), key=lambda x: x["time"])
