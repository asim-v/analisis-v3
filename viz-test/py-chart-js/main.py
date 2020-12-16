
from flask import Flask,render_template,redirect,url_for

app = Flask(__name__)


@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/<name>")
def user(name):
	return "hello-- {}".format(name)

@app.route("/admin")
def admin():
	return redirect(url_for("home"))





if __name__ == '__main__':
	app.run(debug=True)
