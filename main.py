from flask import Flask, render_template
import urllib

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run()


@app.route("/requirements")
def requirements():
    req = open("requirements.txt")
    return render_template('requirements.html', requirements_string=req.read())




