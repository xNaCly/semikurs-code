import backend
from flask import Flask, jsonify
import json
app = Flask(__name__)
data = backend.reader("contents.json")

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

@app.route("/random/")
def hello():
	return jsonify(newQuestion())
@app.route("/all/")
def all():
	return jsonify(json.loads(data))


if __name__ == "__main__":
	app.run(debug=True)