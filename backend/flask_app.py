import backend
from flask import Flask, jsonify, redirect, Response, request
import json
import uuid
app = Flask(__name__)
data = backend.reader("./contents.json")
endpointers = backend.reader("./endpoints.json")

lock_down_api = False
disable_post = True
disable_dash_all_request = True

if lock_down_api:
	print("! API LOCKED DOWN !")

def routes():
	routes = endpointers.replace("[","").replace("]","").replace("\"","").replace(" ","").split(",")
	print("---------------------")
	print("""
 __  ___   _    _    ____ _  __   __
 \ \/ / \ | |  / \  / ___| | \ \ / /
  \  /|  \| | / _ \| |   | |  \ V / 
  /  \| |\  |/ ___ \ |___| |___| |  
 /_/\_\_| \_/_/   \_\____|_____|_|  
""")
	print("Routes:")
	for route in routes:
		print(f"++ {route}")
	print("---------------------\n\n\n")
def newQuestion():
	question = backend.getQuestion(data)
	answers = backend.getValuesFromQuestion(question, data)
	rightanswer = answers[0]

	showObject = {
		"question": question,
		"answers": answers,
		# "richtigeAntwort": richtigeAntwort
	}
	return showObject


@app.route("/endpoints")
def endpoints():
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	resp = jsonify(json.loads(endpointers))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

@app.route("/random")
def random():
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	resp = jsonify(newQuestion())
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

"""
get answer for query 
"""
@app.route("/check")
def check():
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	q = request.args.get("q")
	a = request.args.get("a")
	if not q or not a:
		resp = jsonify({
				"content": {
					"error": "missing params. syntax should be: ?q=<question>&a=<answer>"
				},
				"status": 400
			})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,400
	content = json.loads(data)
	awnser = content[q][0]
	if not awnser:
		resp = jsonify({
				"content": {
					"error": "couldnt find " + q 
				},
				"status": 404
			})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,404
	if not a == awnser:
		resp = jsonify({
				"content": {
					"success": False,
					"error": a + " isnt right" 
				},
				"status": 409
			})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,409
	resp = jsonify({
			"content": {
				"success": True,
				"feedback": a + " is right" 
			},
			"status": 200
		})
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp,200
		


"""
endpoint disabled due to abuse
"""
@app.route("/all")
def all():
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	if disable_dash_all_request:
		resp = jsonify({
				"content": {
						"error": "'GET' requests to this Endpoint, due to abuse, not allowed!"
					},
					"status": 403
				})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	resp = jsonify(json.loads(data))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

@app.route("/scoreboard", methods=['POST','GET'])
def scoreboard():
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	if request.method == "POST":
		if disable_post:
			resp = jsonify({
				"content": {
						"error": "Post requests not allowed!"
					},
					"status": 403
				})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			return resp,403
		name,score = request.args.get("name"), request.args.get("score")
		if not name or not score:
			resp = jsonify({
				"content": {
					"error": "missing params. syntax should be: ?name=<string>&score=<number>"
				},
				"status": 400
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			return resp,400
		try:
			useruuid = str(uuid.uuid4()) + str(uuid.uuid4())
			with open("./scoreboard.csv", "a") as f:
				f.write(f"\n{name},{score},{useruuid}")
			resp = jsonify({
				"content": {
					"name":name,
					"score":score
				},
				"status": 200
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			return resp,200
		except Exception as EX:
			jsonify({
				"content": {
					"error": "couldnt write to scoreboardDB:" + EX
				},
				"status": 500
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			return resp,500
	elif request.method == "GET":
		with open("./scoreboard.csv", "r") as f:				
			scores = f.read()
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
			returndict = jsonify(returndict)
			returndict.headers['Access-Control-Allow-Origin'] = '*'
			return returndict,200
		else:
			return scores,200

@app.route("/stats",methods=["GET"])
def stats():
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	statsdict = {}
	with open("./scoreboard.csv") as f:
		data = f.read()
	data = data.split("\n")
	data.pop(0)
	scores = []
	names = []
	unsorted = []
	for x in data:
		scores.append(int(x.split(",")[1]))	
		unsorted.append(int(x.split(",")[1]))
		if "Player" in x.split(",")[0]:
			names.append(x.split(",")[0])
		else:
			continue
	scores.sort(reverse=True)
	statsdict["highest_score"] = scores[0]
	scores.sort(reverse=False)
	statsdict["lowest_score"] = scores[0]
	statsdict["players"] = len(data)
	statsdict["registered_players"] = len(data) - len(names)
	statsdict["all_scores_unsorted"] = unsorted
	statsdict["all_scores_sorted"] = scores
	statsdict = jsonify(statsdict)
	statsdict.headers['Access-Control-Allow-Origin'] = '*'
	return statsdict,200

if __name__ == "__main__":
	routes()
	app.run()
else:
	routes()