import re
from typing import Any


class Docs:
	_regex = re.compile(
		r"^\s*;(?P<value>.*)"
	)

	@classmethod
	def is_docs(cls, row: str) -> bool:
		return bool(cls._regex.search(row))

	@classmethod
	def parse(cls, row: str) -> str:
		return cls._regex.search(row).group(0)


class Variable:
	_regex_with_docs = re.compile(
		r"(?P<key>[_\w\[\]]*)\s*=(?P<value>.*)\s*;(?P<docs>.*)?"
	)
	_regex = re.compile(
		r"(?P<key>[_\w\[\]]*)\s*=(?P<value>.*)"
	)

	def __init__(self, row: str):
		match = self._regex_with_docs.search(row) or self._regex.search(row)
		data = match.groupdict()
		self.key: str = data["key"]
		self.value: Any = data["value"]
		self.docs: str = data.get("docs", "")

	def __repr__(self):
		return f"{self.key} = {repr(self.value)}" + (f"  # {self.docs}" if self.docs else "")

	@classmethod
	def is_variable(cls, row: str) -> bool:
		return bool(cls._regex.search(row))


class Section:
	_regex = re.compile(
		r"\[(?P<title>.+)\]\s*(?P<docs>;.*)?"
	)

	def __init__(self, row: str):
		data = self._regex.search(row).groupdict()
		self.title: str = data["title"]
		self.docs: str = data["docs"]
		self.vars: list[Variable] = []

	def __repr__(self):
		res = f"[{self.title}]"
		if self.docs:
			res += f"\n{self.docs}"
		for i in self.vars:
			res += f"\n{i}"
		return res

	@classmethod
	def is_section(cls, row: str) -> bool:
		return bool(cls._regex.search(row))


class File:
	def __init__(self, name):
		self.name = name
		self.sections: list[Section] = []
		self.docs: str = ''

	def __repr__(self):
		res = f"==========================={self.name}==========================="
		if self.docs:
			res += f"\n{self.docs}"
		for i in self.sections:
			res += f"\n{i}"
		return res
