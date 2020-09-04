import backend
from flask import Flask, jsonify, redirect, Response, request
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

@app.route("/scoreboard", methods=['POST','GET'])
def scoreboard():
	if request.method == "POST":
		name,score = request.args.get("name"), request.args.get("score")
		if not name or not score:
			return {
				"content": {
					"error": "missing params. syntax should be: ?name=<string>&score=<number>"
				},
				"status": 400
			}
		try:
			with open("./scoreboard.csv", "a") as f:
				f.write(f"\n{name},{score}")
			return {
				"content": {
					"name":name,
					"score":score
				},
				"status": 200
			}
		except:
			return {
				"content": {
					"error": "failed to write score to 'scoreboard.csv'"
				},
				"status": 500
			}
	elif request.method == "GET":
		with open("./scoreboard.csv", "r") as f:
			return f.read(), 200

if __name__ == "__main__":
	app.run(debug=True)