import backend
from flask import Flask, jsonify, redirect, Response, request
import json
app = Flask(__name__)
data = backend.reader("./contents.json")
endpointers = backend.reader("./endpoints.json")

with open("./authss.csv", "r") as f:
	auth = f.read().split("\n")

def log(request):
	with open("./logs","a") as f:
		f.write("\n"+str(request) + "|" + request.remote_addr)

def routes():
	routes = endpointers.replace("[","").replace("]","").replace("\"","").replace(" ","").split(",")
	print("Routes:")
	for route in routes:
		print(f"++ {route}")

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
	if not request.args.get("auth") in auth:
		return "Invalid auth",401
	log(request)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

@app.route("/random")
def random():
	resp = jsonify(newQuestion())
	if not request.args.get("auth") in auth:
		return "Invalid auth",401
	log(request)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200


@app.route("/all")
def all():
	resp = jsonify(json.loads(data))
	if not request.args.get("auth") in auth:
		return "Invalid auth",401
	log(request)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

@app.route("/scoreboard", methods=['POST','GET'])
def scoreboard():
	if request.method == "POST":
		log(request)
		if not request.args.get("auth") in auth:
			return "Invalid auth",401
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
		if not request.args.get("auth") in auth:
			return "Invalid auth",401
		log(request)
		with open("./scoreboard.csv", "r") as f:
			return f.read(), 200

if __name__ == "__main__":
	routes()
	app.run()