import os
import sys
import json
import base64
import subprocess
from flask import Flask, request, jsonify, session, render_template

def install_dependencies():
    for pkg in ["flask", "cryptography"]:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_dependencies()

from utils import set_master_password, verify_master_password
from generator import generate_password
from storage import derive_key, load_encrypted_vault, save_encrypted_vault, backup_vault
from strength import check_strength

META_FILE = "meta.json"
app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_vault_key():
    master = session.get("master")
    if not master:
        return None, None
    with open(META_FILE) as f:
        salt = base64.b64decode(json.load(f)["salt"])
    key = derive_key(master, salt)
    vault = load_encrypted_vault(key)
    return vault, key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    setup = os.path.exists(META_FILE)
    logged_in = "master" in session
    return jsonify({"setup": setup, "logged_in": logged_in})

@app.route("/api/setup", methods=["POST"])
def setup():
    data = request.json
    master = data.get("password", "")
    if not master or len(master) < 6:
        return jsonify({"ok": False, "error": "Password too short (min 6 chars)"}), 400
    if os.path.exists(META_FILE):
        return jsonify({"ok": False, "error": "Already set up"}), 400
    set_master_password(master)
    session["master"] = master
    return jsonify({"ok": True})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    master = data.get("password", "")
    if verify_master_password(master):
        session["master"] = master
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Wrong password"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("master", None)
    return jsonify({"ok": True})

@app.route("/api/vault")
def vault_list():
    if "master" not in session:
        return jsonify({"error": "Not logged in"}), 401
    vault, _ = get_vault_key()
    return jsonify({"services": list(vault.keys())})

@app.route("/api/vault/<service>")
def vault_get(service):
    if "master" not in session:
        return jsonify({"error": "Not logged in"}), 401
    vault, _ = get_vault_key()
    pw = vault.get(service)
    if pw is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"service": service, "password": pw})

@app.route("/api/vault", methods=["POST"])
def vault_add():
    if "master" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.json
    service = data.get("service", "").strip()
    password = data.get("password", "").strip()
    if not service or not password:
        return jsonify({"ok": False, "error": "Service and password required"}), 400
    vault, key = get_vault_key()
    if service in vault:
        return jsonify({"ok": False, "error": "Service already exists"}), 400
    vault[service] = password
    save_encrypted_vault(vault, key)
    return jsonify({"ok": True})

@app.route("/api/vault/<service>", methods=["DELETE"])
def vault_delete(service):
    if "master" not in session:
        return jsonify({"error": "Not logged in"}), 401
    vault, key = get_vault_key()
    if service not in vault:
        return jsonify({"ok": False, "error": "Not found"}), 404
    del vault[service]
    save_encrypted_vault(vault, key)
    return jsonify({"ok": True})

@app.route("/api/generate")
def api_generate():
    length = int(request.args.get("length", 16))
    upper = request.args.get("upper", "true") == "true"
    digits = request.args.get("digits", "true") == "true"
    symbols = request.args.get("symbols", "true") == "true"
    pw = generate_password(length, upper, digits, symbols)
    result = check_strength(pw)
    return jsonify({"password": pw, "strength": result})

@app.route("/api/strength", methods=["POST"])
def api_strength():
    pw = request.json.get("password", "")
    return jsonify(check_strength(pw))

@app.route("/api/backup", methods=["POST"])
def api_backup():
    if "master" not in session:
        return jsonify({"error": "Not logged in"}), 401
    backup_vault()
    return jsonify({"ok": True})

if __name__ == "__main__":
    print("Password Manager running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)