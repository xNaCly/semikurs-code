# from terminaltables import SingleTable
# table_data = [["question","answers","context"]]
# print(SingleTable(table_data).table)
with open("content.csv","r") as f:
    questions = f.read().split("\n")
for item in questions:
    print("-----") 
    item = item.split("|")
    print(f"\t{item[0]}\n\t{item[1:-2]}\n\t{item[-1]}")
