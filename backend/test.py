with open("./scoreboard.csv", "r") as f:				
	scores = f.read()
scores = scores.split("\n")
scores.pop(0)

def test(x):
    return int(x.split(",")[1])

scores.sort(reverse=True, key=test)
print(scores[0:9])