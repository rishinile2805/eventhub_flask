import csv
import io
import sqlite3
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response,
)

app = Flask(__name__)
app.secret_key = "college_eventhub_secret"
ADMIN_PASSWORD = "admin123"
DB_NAME = "eventhub.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                venue TEXT NOT NULL,
                description TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                student_email TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        """)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin login required.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def index():
    with get_db() as conn:
        events = conn.execute("""
            SELECT e.*, COUNT(r.id) AS reg_count
            FROM events e
            LEFT JOIN registrations r ON e.id = r.event_id
            GROUP BY e.id
            ORDER BY e.date ASC
        """).fetchall()
    return render_template("index.html", events=events)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Logged in as Admin.")
            return redirect(url_for("index"))
        flash("Incorrect password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route("/create", methods=["GET", "POST"])
@admin_required
def create_event():
    if request.method == "POST":
        title = request.form["title"].strip()
        date = request.form["date"]
        venue = request.form["venue"].strip()
        description = request.form["description"].strip()

        if title and date and venue:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO events (title, date, venue, description) VALUES (?, ?, ?, ?)",
                    (title, date, venue, description),
                )
            flash("Event created successfully!")
            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    student_name = request.form["student_name"].strip()
    student_email = request.form["student_email"].strip()

    if student_name and student_email:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO registrations (event_id, student_name, student_email) VALUES (?, ?, ?)",
                (event_id, student_name, student_email),
            )
        flash("Registration confirmed!")

    return redirect(url_for("index"))


@app.route("/event/<int:event_id>/participants")
@admin_required
def participants(event_id):
    with get_db() as conn:
        event = conn.execute(
            "SELECT * FROM events WHERE id = ?", (event_id,)
        ).fetchone()
        students = conn.execute(
            "SELECT * FROM registrations WHERE event_id = ? ORDER BY id ASC",
            (event_id,),
        ).fetchall()
    return render_template("participants.html", event=event, students=students)


@app.route("/event/<int:event_id>/export")
@admin_required
def export_csv(event_id):
    with get_db() as conn:
        event = conn.execute(
            "SELECT title FROM events WHERE id = ?", (event_id,)
        ).fetchone()
        students = conn.execute(
            "SELECT student_name, student_email FROM registrations WHERE event_id = ? ORDER BY id ASC",
            (event_id,),
        ).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["S.No", "Student Name", "College Email"])
    for idx, s in enumerate(students, start=1):
        writer.writerow([idx, s["student_name"], s["student_email"]])

    filename = f"{event['title'].replace(' ', '_')}_participants.csv"
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/delete/<int:event_id>", methods=["POST"])
@admin_required
def delete_event(event_id):
    with get_db() as conn:
        conn.execute("DELETE FROM registrations WHERE event_id = ?", (event_id,))
        conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    flash("Event deleted.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
