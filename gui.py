import main
import tkinter as t 
r = t.Tk()
content = main.reader("contents.json")
question = main.format_questions(content)
answer_array = main.access_data_from_question_key(question, content)
# Answerpossibilities
def answer_compare():
	pass
def a():
    print("a")
def b():
    print("b")
def c():
    print("c")
def d():
    print("d")
r.title("Choose or Loose")
r.geometry("320x220")
t.Label(r, text=question, width=250).pack()
times = 0
for answers in answer_array:
	times +=1
	t.Label(r, text=str(times) + ".  " + answers, width=150).pack()
t.Button(r, text="1", command=a, width="10").pack(side="left")
t.Button(r, text="2", command=b, width="10").pack(side="left")
t.Button(r, text="3", command=c, width="10").pack(side="left")
t.Button(r, text="4", command=d, width="10").pack(side="left")
r.mainloop()