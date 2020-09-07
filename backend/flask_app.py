import backend
from flask import Flask, jsonify, redirect, Response, request
import json
import uuid
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
			useruuid = str(uuid.uuid4()) + str(uuid.uuid4())
			with open("./scoreboard.csv", "a") as f:
				f.write(f"\n{name},{score},{useruuid}")
			return {
				"content": {
					"name":name,
					"score":score
				},
				"status": 200
			}
		except Exception as EX:
			return f"failed to write score to 'scoreboard.csv'{EX}"
	elif request.method == "GET":
		with open("./scoreboard.csv", "r") as f:				
			scores = f.read()
		if not request.args.get("auth") in auth:
			return "Invalid auth",401
		log(request)
		if request.args.get("top"):
			scores = scores.split("\n")
			scores.pop(0)

			def test(x):
			    return int(x.split(",")[1])
			returndict = {
				"content":{},
				"status":200
			}
			scores.sort(reverse=True, key=test)
			y = 0
			for x in scores[0:10]:
				returndict["content"][y] = x
				y += 1
			return returndict,200
		else:
			return scores,200
			
if __name__ == "__main__":
	routes()
	app.run()