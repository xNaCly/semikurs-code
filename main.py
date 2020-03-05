# adrian & matteo 

# show question and possible answer 
# ask input
# compare to question with answers
# return right/false

from json import loads as loa
from os import system as s
import random


def reader(file):
	with open(file, "r") as f:
		content = f.read()
	return content

def format_questions(content):
	# takes json-dict --> adds questions to array --> returns a random question
	content = loa(content)
	question_array = []
	for key in content.keys():
		question_array.append(key)
	lenght = len(question_array)
	number = random.random() * lenght
	try:
		final_question = question_array[int(round(number))]
	except:
		lenght = len(question_array)
		number = random.random() * lenght
		final_question = question_array[int(round(number))]
		pass
	return final_question

def access_data_from_question_key(final_question, content):
	# combines the questions with the corresponding values
	content_json = loa(content)
	print("\n" + final_question + "\n")
	answer_array = []
	for x in content_json[final_question]:
		answer_array.append(x)
	return answer_array
	# answer_array[0] --> right anwser