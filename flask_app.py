import backend
from flask import Flask, jsonify
import json
app = Flask(__name__)
data = backend.reader("contents.json")
endpointers = backend.reader("endpoints.json")

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


#routing
@app.route("/endpoints")
def endpoints():
	return jsonify(json.loads(endpointers))

@app.route("/random/")
def random():
	return jsonify(newQuestion())

@app.route("/all/")
def all():
	return jsonify(json.loads(data))


if __name__ == "__main__":
	app.run(debug=True)