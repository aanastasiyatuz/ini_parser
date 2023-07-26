from parser.base import Parser

with open("./test.ini") as f:
	parsed_file = Parser.parse(f)
	print(parsed_file)
	print("-----------------------------------")
	print(parsed_file.sections[0].vars)
