# main.py
from flask import Flask, request, g, abort
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from config import Config
from blueprints.public import public_bp
from blueprints.admin import admin_bp

HTTP_REQ = grequests.Request()

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")

# In main.py, add proper Firebase initialization:
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    # For App Engine, use default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)


@app.before_request
def verify_token():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.split()[1]
        try:
            claims = id_token.verify_firebase_token(token, HTTP_REQ, audience=Config.PROJECT_ID)  # [1]
            g.user = claims  # make claims available to views
        except Exception:
            abort(401, "Invalid token")
    else:
        g.user = None
