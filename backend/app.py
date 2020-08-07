import os
import logging

import requests
from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
# CORS only for local dev
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

logger = logging.getLogger(__name__)

SECRET_TOKEN = os.getenv("Z_TOKEN")
BASE_URL = os.getenv("Z_URL")

if not SECRET_TOKEN or not BASE_URL:
    logger.error('Missing conf env var(s)')

FIELDS = ("email", "category", "message", "title", "name")
TRAP_FIELD = "last_name"


def post_zammad_ticket(data):
    headers = {"Authorization": "Bearer %s" % SECRET_TOKEN}
    # try to create user, failure is not a problem
    name = data["name"]
    split = name.split(" ")
    firstname = split[0]
    lastname = " ".join(split[1:]) if len(split) > 1 else ""
    r = requests.post("%s/users" % BASE_URL, json={
        "firstname": firstname,
        "lastname": lastname,
        "email": data["email"],
        "roles": ["Customer"]
    }, headers=headers)
    logger.debug("Create user: %s", r.json())
    # create ticket
    post_data = {
        "title": data["title"],
        "group": data["category"],
        "article": {
            "body": data["message"],
            "type": "web",
            "from": data["email"],
            "to": data["category"],
            "internal": False,
        },
        "customer": data["email"],
    }
    headers["X-On-Behalf-Of"] = data["email"]
    r = requests.post("%s/tickets" % BASE_URL, json=post_data, headers=headers)
    logger.debug("Create ticket: %s", r.json())
    return r.status_code, r.json()


@app.route("/api", methods=["POST"])
def post_ticket():
    data = request.json
    for field in FIELDS:
        if field not in data:
            abort(400, jsonify(error="Missing json parameter"))
            return
    if TRAP_FIELD in data and data[TRAP_FIELD]:
        # dummy response for bot spammers
        abort(200)
    status, data = post_zammad_ticket(data)
    # except Exception as e:
    #     abort(500, jsonify(error=str(e)))
    return jsonify(data)


@app.route("/", defaults={"path": ""})
# allows routing in vuejs
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")
