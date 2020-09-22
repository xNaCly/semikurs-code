from flask import Flask, jsonify, redirect, Response, request
import schedule
import backend
import os
from random import shuffle
import time
import json
import uuid
app = Flask(__name__)

# flags
lock_down_api = False
disable_post = False
disable_dash_all_request = False


# fix for not working paths on server:
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data = backend.reader(os.path.join(THIS_FOLDER, 'contents.json'))
endpointers = backend.reader(os.path.join(THIS_FOLDER, 'endpoints.json'))


users = {}
auth = ",".join(users.keys()).split(",")

def clear_cache():
	del auth[:]
	users.clear()

def check_for_time():
	schedule.every().day.at("21:00").do(clear_cache)



if lock_down_api:
	print("! API LOCKED DOWN !")

"""
prints stuff
---------------------

 __  ___   _    _    ____ _  __   __
 \ \/ / \ | |  / \  / ___| | \ \ / /
  \  /|  \| | / _ \| |   | |  \ V /
  /  \| |\  |/ ___ \ |___| |___| |
 /_/\_\_| \_/_/   \_\____|_____|_|

Routes:
++ /all
++ /random
++ /endpoints
++ /scoreboard
++ /graphs
++ /check

---------------------
"""
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

"""
format questions
"""
def newQuestion():
	question = backend.getQuestion(data)
	answers = backend.getValuesFromQuestion(question, data)
	returnanswers = answers
	shuffle(returnanswers)

	showObject = {
		"question": question,
		"answers": returnanswers,
	}
	return showObject

"""
get all endpoints

-----------
/endpoints
[
  "/all",
  "/random",
  "/endpoints",
  "/scoreboard",
  "/graphs",
  "/check"
]
-----------

- returns array
"""
@app.route("/endpoints",methods=["GET"])
def endpoints():
	check_for_time()
	if not request.args.get("sid") in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
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

"""
get a question:

-----------
/random
{
  "answers": [ 
	  "awnser1",
	  "awnser2",
	  "awnser3",
	  "awnser4"
  ],
  "question": ""
}
-----------

- returns json
"""
@app.route("/random",methods=["GET"])
def random():
	check_for_time()
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403	
	if not request.args.get("sid") in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
	resp = jsonify(newQuestion())
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

"""
get answer for query:

-----------
/check?q=<question>&a=<answer>
{
  "content": {
    "feedback": "<answer> is right",
    "success": true
  },
  "status": 200
}
-----------

- returns json
"""
@app.route("/check",methods=["GET"])
def check():
	check_for_time()	
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	if not request.args.get("sid") in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
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
	answer = content[q][0]
	if not answer:
		resp = jsonify({
				"content": {
					"error": "couldnt find " + q 
				},
				"status": 404
			})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,404
	if not a == answer:
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
- would return:

-----------
/all
{
  "question": [
	  "answer1",
	  "answer2",
	  "answer3",
	  "answer4"
  ],
  "question": [
	  "answer1",
	  "answer2",
	  "answer3",
	  "answer4"
  ],
  "question": [
	  "answer1",
	  "answer2",
	  "answer3",
	  "answer4"
  ],
}
-----------

-returns json
"""
@app.route("/all",methods=["GET"])
def all():
	check_for_time()	
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
	if not request.args.get("sid") in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
	resp = jsonify(json.loads(data))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp, 200

"""
get scoreboard

-----------
/scoreboard

name,score,uuiduuid
player,score,uuid

- returns csv
-----------

-----------
/scoreboard?top=True

{
  "content": {
    "0": "player,score,uuid",
    "1": "player,score,uuid",
    "2": "player,score,uuid",
    "3": "player,score,uuid",
    "4": "player,score,uuid",
    "5": "player,score,uuid",
    "6": "player,score,uuid",
    "7": "player,score,uuid",
    "8": "player,score,uuid",
    "9": "player,score,uuid"
  },
  "status": 200
}
-returns json
-----------
"""
@app.route("/scoreboard", methods=['POST','GET'])
def scoreboard():
	check_for_time()	
	if lock_down_api:
		resp = jsonify({
			"content": {
					"error": "API currently locked down, try again later"
				},
				"status": 403
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	sid = request.args.get("sid")
	if not sid in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
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
		name = request.args.get("name")
		if not name or not sid:
			resp = jsonify({
				"content": {
					"error": "missing params. syntax should be: ?name=<string>&sid=<sessionID>"
				},
				"status": 400
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			return resp,400
		try:
			score = users[sid]["score"]
		except:
			resp = jsonify({
				"content": {
					"error": "invalid sid"
				},
				"status": 401
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			return resp,401
		try:
			with open(os.path.join(THIS_FOLDER, 'scoreboard.csv'), "a") as f:
				f.write(f"\n{name},{score},{sid}")
			resp = jsonify({
				"content": {
					"name":name,
					"score":score,
					"message":"wrote the above to the db"
				},
				"status": 200
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			users.pop(sid)
			auth.remove(sid)
			return resp,200
		except Exception as EX:
			resp = jsonify({
				"content": {
					"error": "couldnt write to scoreboardDB:" + EX
				},
				"status": 500
			})
			resp.headers['Access-Control-Allow-Origin'] = '*'
			users.pop(sid)
			auth.remove(sid)
			return resp,500
	elif request.method == "GET":
		with open(os.path.join(THIS_FOLDER, 'scoreboard.csv'), "r") as f:				
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

"""
get stats
-----------
{
  "all_scores_sorted": [...],
  "all_scores_unsorted": [...],
  "highest_score": int,
  "lowest_score": Int,
  "players": int,
  "registered_players": int
}
"""
@app.route("/graphs",methods=["GET"])
def stats():
	check_for_time()	
	if lock_down_api:
		resp = jsonify({
					"content": {
							"error": "API currently locked down, try again later"
						},
						"status": 403
					})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,403
	if not request.args.get("sid") in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
	statsdict = {}
	with open(os.path.join(THIS_FOLDER, 'scoreboard.csv'), "r") as f:
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

@app.route("/register",methods=["GET"])
def register():
	check_for_time()
	sessionid = uuid.uuid4()
	auth.append(str(sessionid))
	users[str(sessionid)] = {"lifes":5,"score":0}
	resp = jsonify({
		"content": {
				"session_id": sessionid,
				"message":"sessionid generated, userobject created."
			},
			"status": 201
		})
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp,201

@app.route("/update",methods=["GET"])
def update():	
	sid = request.args.get("sid")
	if not sid in auth:
		resp = jsonify({
			"content": {
				"error": "invalid sid"
			},
			"status": 401
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,401
	if request.args.get("del"):
		users.pop(sid)
		auth.remove(sid)
		resp = jsonify({
				"content": {
						"message":f"{sid} removed from the current users",
					},
					"status": 200
				})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,200
	correct = request.args.get("cr")
	if users[sid]["lifes"] == 0:
		resp = jsonify({
			"content": {
					"error":"Game over",
					"body":{
						"score": users[sid]["score"],
						"lifes": users[sid]["lifes"],
					}
				},
				"status": 201
		})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,201
	if correct == "yes":
		users[sid]["score"] += 100
		resp = jsonify({
			"content": {
					"message":"userobject updated.",
					"body":{
						"score": users[sid]["score"],
						"lifes": users[sid]["lifes"],
					}
				},
				"status": 201
			})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,201
	elif correct == "no":
		users[sid]["score"] -= 100
		users[sid]["lifes"] -= 1
		resp = jsonify({
			"content": {
					"message":"userobject updated.",
					"body":{
						"score": users[sid]["score"],
						"lifes": users[sid]["lifes"],
					}
				},
				"status": 201
			})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,201
	else:
		resp = jsonify({
				"content": {
						"message":sid,
						"body":{
							"score": users[sid]["score"],
							"lifes": users[sid]["lifes"],
						}
					},
					"status": 200
				})
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp,200


if __name__ == "__main__":
	routes()
	app.run()
else:
	routes()