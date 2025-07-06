import os
from pathlib import Path


class Config:
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "lapleaderboard")
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    ALLOWED_ADMINS = set(
        ["finlaywojtan@gmail.com", "alexanderanthonyyoungson@gmail.com"]
    )
