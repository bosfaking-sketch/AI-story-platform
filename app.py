from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        print("Username:", username)
        print("Email:", email)
        print("Password:", password)

        return "Registration successful!"

    return render_template("register.html")


@app.route("/submit")
def submit():
    return render_template("submit.html")


if __name__ == "__main__":
    app.run(debug=True)