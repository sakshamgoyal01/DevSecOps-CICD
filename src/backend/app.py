from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import get_db_connection
import os

host = os.getenv("APP_HOST", "127.0.0.1")
port = int(os.getenv("APP_PORT", 5001))
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/people", methods=["POST"])
def add_person():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO people (name, age) VALUES (%s, %s)",
        (data["name"], data["age"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Person added"}), 201

@app.route("/people", methods=["GET"])
def get_people():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age FROM people")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"id": r[0], "name": r[1], "age": r[2]} for r in rows
    ])


if __name__ == "__main__":
    app.run(host=host, port=port)
