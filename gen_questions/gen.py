import json

questions = {}

frage_inhalt = input("Syntax => <Frage>|<richtige_Antwort>|<antwort>|<antwort>|<antwort>|<context>")
frage_inhalt = frage_inhalt.split("|")
questions[frage_inhalt[0]] = [
    frage_inhalt[1],
    frage_inhalt[2],
    frage_inhalt[3],
    frage_inhalt[4]
]
print(questions)
with open("temp.json","w") as f:
    json.dump(questions, f)