"""
file to show usage of backend.py
"""
import backend

# to make readable
import json

data = backend.reader("contents.json")
frage = backend.getQuestion(data)
antworten = backend.getValuesFromQuestion(frage, data)
richtigeAntwort = antworten[0]

showObject = {
"frage": frage,
"antworten": antworten,
"richtigeAntwort": richtigeAntwort
}

print(json.dumps(showObject, indent=2))
