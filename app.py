from flask import Flask, render_template, request, redirect, session
import sqlite3
from flask_bcrypt import Bcrypt
from database import create_database
from pdf_generator import generate_resume

app = Flask(__name__)
app.secret_key = "hasiverse_secret_key"

bcrypt = Bcrypt(app)

# Create database
create_database()
# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")
# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT fullname, password FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):

            session["user"] = user[0]
            session["email"] = email

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")
# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template(
                "signup.html",
                error="Passwords do not match"
            )

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template(
                "signup.html",
                error="Email already exists"
            )

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users(fullname, email, password)
            VALUES (?, ?, ?)
            """,
            (fullname, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")
# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"],
        email=session["email"]
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
# ---------------- RESUME ----------------
@app.route("/resume", methods=["GET", "POST"])
def resume():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        data = {
            "fullname": request.form["fullname"],
            "email": session["email"],
            "phone": request.form["phone"],
            "address": request.form["address"],
            "college": request.form["college"],
            "degree": request.form["degree"],
            "cgpa": request.form["cgpa"],
            "skills": request.form["skills"],
            "projects": request.form["projects"],
            "certificates": request.form["certificates"],
            "objective": request.form["objective"]
        }

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO resumes(
            user_email,
            fullname,
            phone,
            address,
            college,
            degree,
            cgpa,
            skills,
            projects,
            certificates,
            objective
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            session["email"],
            data["fullname"],
            data["phone"],
            data["address"],
            data["college"],
            data["degree"],
            data["cgpa"],
            data["skills"],
            data["projects"],
            data["certificates"],
            data["objective"]
        ))

        conn.commit()
        conn.close()

        generate_resume(data)

        return render_template(
            "preview.html",
            resume=data
        )

    return render_template(
        "resume.html",
        user=session["user"]
    )
# ---------------- MY RESUMES ----------------
@app.route("/my-resumes")
def my_resumes():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resumes
        WHERE user_email=?
        ORDER BY id DESC
    """, (session["email"],))

    resumes = cursor.fetchall()

    conn.close()

    return render_template(
        "my_resumes.html",
        resumes=resumes
    )
# ---------------- DOWNLOAD PDF ----------------
@app.route("/download")
def download():

    return generate_resume(None)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
    # ---------------- INTERNSHIPS ----------------

@app.route("/internships")
def internships():

    if "user" not in session:
        return redirect("/login")


    conn = sqlite3.connect("users.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
    SELECT * FROM internships
    """)


    internships = cursor.fetchall()


    conn.close()


    return render_template(
        "internships.html",
        internships=internships
    )
# ---------------- MY APPLICATIONS ----------------

@app.route("/my-applications")
def my_applications():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    internships.company,

    internships.role,

    internships.location,

    internships.duration,

    applications.applied_on

    FROM applications

    JOIN internships

    ON internships.id=applications.internship_id

    WHERE applications.user_email=?

    ORDER BY applications.id DESC

    """,(session["email"],))

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications
    )
# ---------------- APPLY INTERNSHIP ----------------

@app.route("/apply/<int:internship_id>")
def apply_internship():

    if "user" not in session:
        return redirect("/login")

    internship_id = request.view_args["internship_id"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Check already applied
    cursor.execute("""
        SELECT id
        FROM applications
        WHERE user_email=?
        AND internship_id=?
    """,(session["email"], internship_id))

    existing = cursor.fetchone()

    if existing:

        conn.close()

        return redirect("/internships")

    cursor.execute("""
        INSERT INTO applications(
            user_email,
            internship_id
        )
        VALUES(?,?)
    """,(session["email"], internship_id))

    conn.commit()
    conn.close()

    return redirect("/my-applications")