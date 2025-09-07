from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "events.db"

def query_db(query, args=(), one=False, commit=False):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, args)
    if commit:
        conn.commit()
        conn.close()
        return
    rv = c.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    query_db("""CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, type TEXT, college TEXT)""", commit=True)

    query_db("""CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, college TEXT)""", commit=True)

    query_db("""CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INT, event_id INT,
                    UNIQUE(student_id, event_id))""", commit=True)

    query_db("""CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INT, event_id INT)""", commit=True)

    query_db("""CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INT, event_id INT, rating INT)""", commit=True)


# ---------- Routes ----------
@app.route("/event", methods=["POST"])
def create_event():
    data = request.json
    query_db("INSERT INTO events (name, type, college) VALUES (?, ?, ?)",
             (data["name"], data["type"], data["college"]), commit=True)
    return jsonify({"message": "Event created"}), 201


@app.route("/student", methods=["POST"])
def create_student():
    data = request.json
    query_db("INSERT INTO students (name, college) VALUES (?, ?)",
             (data["name"], data["college"]), commit=True)
    return jsonify({"message": "Student added"}), 201


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        query_db("INSERT INTO registrations (student_id, event_id) VALUES (?, ?)",
                 (data["student_id"], data["event_id"]), commit=True)
        return jsonify({"message": "Registered successfully"}), 201
    except:
        return jsonify({"error": "Already registered"}), 400


@app.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.json
    query_db("INSERT INTO attendance (student_id, event_id) VALUES (?, ?)",
             (data["student_id"], data["event_id"]), commit=True)
    return jsonify({"message": "Attendance marked"}), 201


@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.json
    query_db("INSERT INTO feedback (student_id, event_id, rating) VALUES (?, ?, ?)",
             (data["student_id"], data["event_id"], data["rating"]), commit=True)
    return jsonify({"message": "Feedback submitted"}), 201


@app.route("/report/event_popularity", methods=["GET"])
def event_popularity():
    rows = query_db("""SELECT events.name, COUNT(r.id) as registrations
                       FROM events
                       LEFT JOIN registrations r ON events.id = r.event_id
                       GROUP BY events.id
                       ORDER BY registrations DESC""")
    return jsonify(rows)


@app.route("/report/student_participation", methods=["GET"])
def student_participation():
    rows = query_db("""SELECT students.name, COUNT(a.id) as attended_events
                       FROM students
                       LEFT JOIN attendance a ON students.id = a.student_id
                       GROUP BY students.id
                       ORDER BY attended_events DESC""")
    return jsonify(rows)


@app.route("/report/top_students", methods=["GET"])
def top_students():
    rows = query_db("""SELECT students.name, COUNT(a.id) as attended_events
                       FROM students
                       LEFT JOIN attendance a ON students.id = a.student_id
                       GROUP BY students.id
                       ORDER BY attended_events DESC
                       LIMIT 3""")
    return jsonify(rows)


@app.route("/report/feedback", methods=["GET"])
def avg_feedback():
    rows = query_db("""SELECT events.name, AVG(f.rating) as avg_rating
                       FROM events
                       LEFT JOIN feedback f ON events.id = f.event_id
                       GROUP BY events.id""")
    return jsonify(rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
