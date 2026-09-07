from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AI Story Platform</h1>
    <p>Website đang chạy thành công!</p>
    """

if __name__ == "__main__":
    app.run(debug=True)