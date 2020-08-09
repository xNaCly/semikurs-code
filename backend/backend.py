"""
backend for semikurscode aka Quintic
\n-- --
\ncontains:
\n`reader(file)`
\n`getQuestion(reader(file))`
\n`getValuesFromQuestion(getQuestion(reader(file)), reader(file))`
"""
# json import to store and access data
from json import loads as loa
# random import to randomise answers and questions
import random

def reader(file):
	"""
basicly a snippet to read and store the content of the specifed file in the 'content'-variable
\n-- --
\n``file:`` jsonFile as jsonReadableString
\n-- --
\ninput: `"contents.json"`
\noutput: `content` `(jsonObject)`
	"""
	with open(file, "r") as f:
		content = f.read()

	return content



def getQuestion(content):
	"""
returns a random Question from the given JSONfile
\n--  --
\n``content:`` jsonFile as jsonReadableString
\n--  --
\ninput: `reader("contents.json")` 
\noutput: `Welches der folgenden ist kein Dateisystem?` `(String)`
	"""
	content = loa(content)

	question_array = []
	for key in content.keys():
		question_array.append(key)

	lenght = len(question_array)
	number = random.randint(0,lenght-1)

	final_question = question_array[int(round(number))]

	return final_question


def getValuesFromQuestion(getQuestion, content):
	"""
returns an array of values for a given question:
\n!first value is always the right value!
\n--  --
\n``getQuestion:`` questionString as String
\n``content:`` jsonFile as jsonReadableString
\n--  --
>\ninput: `Welches der folgenden ist kein Dateisystem?`, `reader("contents.json")`
>\noutput: `['JHB52', 'Fat32', 'George 3', 'DOS 3.x']` `(Array)`
	"""
	content_json = loa(content)

	answer_array = []
	for x in content_json[getQuestion]:
		answer_array.append(x)

	# answer_array[0] --> right anwser
	return answer_array

if __name__ == "__main__":
	print("Backend-file -- do not execute as mainfile")
	input()
	exit()