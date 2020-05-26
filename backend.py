# adrian & matteo 

# show question and possible answer 
# ask input
# compare to question with answers
# return right/false

### - Backend - ###

# json import to store and access data
from json import loads as loa
# random import to randomise answers and questions
import random

# function to read and store the content of the specifed file in the 'content'-variable
def reader(file):

	with open(file, "r") as f:
		content = f.read()

	return content


# function to read json-dict --> adds questions to array --> returns a random question
def format_questions(content):

	content = loa(content)

	question_array = []
	for key in content.keys():
		question_array.append(key)

	lenght = len(question_array)
	number = random.randint(0,lenght-1)

	final_question = question_array[int(round(number))]

	return final_question


# combines the questions with the corresponding values
def access_data_from_question_key(final_question, content):
	
	content_json = loa(content)

	answer_array = []
	for x in content_json[final_question]:
		answer_array.append(x)

	# answer_array[0] --> right anwser
	return answer_array

if __name__ == "__main__":
	print("Backend-file -- do not execute as mainfile")
	input()
	exit()