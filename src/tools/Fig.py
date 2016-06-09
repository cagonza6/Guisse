import re
from files import Readfile

labelRegex = r'^(4)\s' + r'([^\s]*)\s' * 12 + r'(.*)\\001$'
font = 9


def formating(line):
	line = list(line)
	line[5] = str(0)  # font: 0= default font, used for latex format
	line[6] = str(font)  # font_flag: 2 = Use for latex
	line[8] = '2'  # latex friendly: flag special, font default
	return line


def replacing(line, replacements):
	if len(replacements) < 1:
		return line

	for change in replacements:
		orig = change[0]
		reps = change[1]
		for i in range(0, len(orig)):
			if str(line[-1]) == str(orig):
				line[-1] = reps
				break
	return line


def fig2latexFriendly(text, replacements):
	script = ''
	for i in range(0, len(text)):
		line = text[i].strip()
		if not re.match(labelRegex, line):
			script += line + '\n'
			continue
		line = re.findall(labelRegex, line)[0]
		line = formating(line)
		line = replacing(line, replacements)
		line = str(' '.join(line)).encode('string-escape') + '\\001'
		script += line + '\n'
	return script


if __name__ == '__main__':
	fig = Readfile('/home/blanko/Desktop/Gnuplotfiles/program/example/dot_prod.fig')
	rep = [['test2', '$test21'], ]
	fig2latexFriendly(fig, rep)
