def reading_module(file):
	with open(file, "r") as f:
		content = f.read()
	return content

def main():
	# ask input
	# compare to question with answers
	# return right/false
	shit = reading_module("contents")
	print()

main()