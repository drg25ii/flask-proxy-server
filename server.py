from flask import Flask, request, jsonify
import requests

app = Flask(_name_)

@app.route("/")
def home():
    return "Proxy online", 200

@app.route("/get_ip")
@app.route("/proxy/get_ip")
def get_ip():
    # ia IP real din X-Forwarded-For dacă există (bun pentru platforme cloud)
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        ip = xff.split(",")[0].strip()
    else:
        ip = request.remote_addr
    return jsonify({"ip": ip})

@app.route("/proxy")
def proxy():
    target = request.args.get("url")
    if not target:
        return jsonify({"error": "Missing url param"}), 400
    try:
        r = requests.get(target, timeout=15, stream=True)
        return (r.content, r.status_code, list(r.headers.items()))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8080)
