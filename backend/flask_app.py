import backend
from flask import Flask, jsonify, redirect, Response
import json
app = Flask(__name__)
data = backend.reader("./contents.json")
endpointers = backend.reader("./endpoints.json")

def newQuestion():
	frage = backend.getQuestion(data)
	antworten = backend.getValuesFromQuestion(frage, data)
	richtigeAntwort = antworten[0]

	showObject = {
		"frage": frage,
		"antworten": antworten,
		"richtigeAntwort": richtigeAntwort
	}
	return showObject


@app.route("/endpoints")
def endpoints():
	resp = jsonify(json.loads(endpointers))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

@app.route("/random")
def random():
	resp = jsonify(newQuestion())
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200


@app.route("/all")
def all():
	resp = jsonify(json.loads(data))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

# @app.route("/")
# def redi():
    # return redirect("https://github.com/xNaCly/semikurs-code/blob/master/server/README.md", code=302)

if __name__ == "__main__":
	app.run(debug=True)