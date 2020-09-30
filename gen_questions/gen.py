import json

questions = {}

with open("content.csv","r") as f:
    content = f.read().split("\n")
    content.pop(0)

for x in content:
    x = x.split("|")
    questions[x[0]] = [
        x[1],
        x[2],
        x[3],
        x[4],
        x[5]
    ]

with open("temp.json","w") as f:
    json.dump(questions, f)