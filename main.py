# adrian & matteo 

# show question and possible answer 
# ask input
# compare to question with answers
# return right/false

from json import loads as loa
from json import dumps as dum
import random

def reading_module(file):
	with open(file, "r") as f:
		content = f.read()
	return content

def format_module(content):
	# takes json-dict --> adds questions to array --> returns a random question
	content = loa(content)
	question_array = []
	for key in content.keys():
		question_array.append(key)
	lenght = len(question_array)
	number = random.random() * lenght
	if int(round(number)) > 1:
		number = 1
	final_question = question_array[int(round(number))]
	return final_question

def access_data_from_question_key(final_question, content):
	content_json = loa(content)
	print(final_question)
	for x in content_json[final_question]:
		print(x)


def main_module():
	content = reading_module("contents.json")
	final_question = format_module(content)
	access_data_from_question_key(final_question, content)

main_module()