from app import app
import json

with open('secrets.json', 'r') as f:
    app.secrets = json.load(f)
