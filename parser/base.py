from typing import TextIO
from parser.types import File, Section, Variable, Docs


class Parser:
	@staticmethod
	def parse(file: TextIO) -> File:
		res_file = File(file.name)
		section = None
		variables = []
		start = True
		for row in file.readlines():
			if start:
				if Docs.is_docs(row):
					res_file.docs = Docs.parse(row)
					start = False
					continue

			if Section.is_section(row):
				start = False
				if section:
					section.vars = variables
					res_file.sections.append(section)
				variables = []
				section = Section(row)

			elif Docs.is_docs(row):
				start = False
				if section.docs:
					section.docs += Docs.parse(row)
				else:
					section.docs = Docs.parse(row)

			elif Variable.is_variable(row):
				start = False
				variables.append(Variable(row))

		section.vars = variables
		res_file.sections.append(section)
		return res_file
