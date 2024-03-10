from flask import Flask,redirect, url_for, render_template

app = Flask(__name__)
@app.route("/")
def home():
    return "HELLO TEST! <h1>xdxd</h1>"

@app.route("/about")
def about():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()