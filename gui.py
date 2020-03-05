import main
import tkinter as t 
r = t.Tk()
content = main.reader("contents.json")
question = main.format_questions(content)
answer_array = main.access_data_from_question_key(question, content)
# Answerpossibilities
def answer_compare():
    print("right anwser :) " + right_answer)
r.title("Choose or Loose")
r.geometry("320x220")
t.Label(r, text=question, width=250).pack()
right_answer = answer_array[0]
right_answer_button = t.Button(r, text=right_answer, width=250, command=answer_compare)
right_answer_button.pack()
del answer_array[0]
for answers in answer_array:
    t.Button(r, text=answers, width=250).pack()
r.mainloop()