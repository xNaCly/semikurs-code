import main
import tkinter as t
r = t.Tk()


def rerun():
    mainiac()

def all_children() :
    _list = r.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

widget_list = all_children()

for item in widget_list:
    item.pack_forget()

def mainiac():
    widget_list = all_children()

    for item in widget_list:
        item.pack_forget()

    content = main.reader("contents.json")
    question = main.format_questions(content)
    answer_array = main.access_data_from_question_key(question, content)
    right_answer = answer_array[0]


    def answer_compare_one():
        text = first_button["text"]
        if text == right_answer:
            print("richtig")
        else:
            print("falsch")

    def answer_compare_two():
        text = second_button["text"]
        if text == right_answer:
            print("richtig")
        else:
            print("falsch")

    def answer_compare_three():
        text = third_button["text"]
        if text == right_answer:
            print("richtig")
        else:
            print("falsch")

    def answer_compare_four():
        text = last_button["text"]
        if text == right_answer:
            print("richtig")
        else:
            print("falsch")

    r.title("Choose or Loose")
    r.geometry("320x220")

    t.Label(r, text=question, width=250).pack()

    def random_answer_value():
        copy_array = answer_array
        main.random.shuffle(copy_array)
        return copy_array
    
    t.Button(r, text="Neue Frage", width=25, command=rerun).pack()
    array = random_answer_value()
    first_button  = t.Button(r, text=array[0], width=250, command=answer_compare_one)
    second_button = t.Button(r, text=array[1], width=250, command=answer_compare_two)
    third_button  = t.Button(r, text=array[2], width=250, command=answer_compare_three)
    last_button   = t.Button(r, text=array[3], width=250, command=answer_compare_four)


    first_button.pack()
    second_button.pack()
    third_button.pack()  
    last_button.pack()
    r.mainloop()

mainiac()