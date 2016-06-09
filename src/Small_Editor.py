from PyQt4.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt4.QtGui import QWidget, QVBoxLayout, QPainter
from PyQt4.QtCore import Qt, QRect, QRegExp

NUMBER_BAR_COLOR = QColor(180, 215, 140)


'''
IMPORTANT:
1) The Highlighter is not my code and it comes directly from here: https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
I just did an implementation for some of the GNUplot, it is a copy and it does not belong to me, the skilled programmers are other people.

2) the bar with the green numbers to show the number of the line where the person is writting also does not belog to me,
it comes from one comment in https://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
From the same page I took the idea and code to show the current line in yellow
Again, I did a copy paste.
'''


def format(color, style=''):
	"""Return a QTextCharFormat with the given attributes.
	"""
	_color = QColor()
	_color.setNamedColor(color)

	_format = QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)

	return _format


# Syntax styles that can be shared by all languages
STYLES = {
	'command': format('blue', 'bold'),
	'keyword': format('blue'),
	'elements': format('black', 'bold'),
	'operator': format('red'),
	'brace': format('darkGray'),
	'string': format('magenta'),
	'string2': format('darkMagenta'),
	'comment': format('darkGreen', 'italic'),
	'numbers': format('brown'),
	'math': format('brown'),
}


class GNUplotHighlighter (QSyntaxHighlighter):
	"""Syntax highlighter for the Python language.
	"""
	# Python keywords
	commands = [
		'set', 'plot', 'reset',
		'replot', 'print', 'unset', 'reset', 'fit',
	]

	keywords = [
		# variables
		'using', 'with', 'linecolor', 'lc', 'linetype', 'lt', 'linewidth',
		'lw', 'linestyle', 'ls', 'line', 'at', 'via', 'errorbars',
		'xerrorbars', 'yerrorbars', 'xyerrorbars', 'pointtype', 'pointsize',
		'color', 'square',
		# Labels
		'from', 'to',
		'terminal', 'output', 'title', 'samples', 'style', 'label', 'xlabel',
		'ylabel', 'xrange', 'yrange', 'grid', 'border', 'datafile', 'multiplot',
		'origin', 'size', 'key', 'logscale'
	]

	# Math definitions
	math_functions = [
		'abs', 'acos', 'acosh', 'airy', 'arg', 'asin', 'asinh', 'atan', 'atan2',
		'atanh', 'EllipticK', 'EllipticE', 'EllipticPi', 'besj0', 'besj1',
		'besy0', 'besy1', 'ceil', 'cos', 'cosh', 'erf', 'erfc', 'exp', 'expint',
		'floor', 'gamma', 'ibeta', 'inverf', 'igamma', 'imag', 'invnorm', 'int',
		'lambertw', 'lgamma', 'log', 'log10', 'norm', 'rand', 'real', 'sgn', 'sin',
		'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'voigt'
	]

	# Python operators
	operators = [
		'=',
		# Comparison
		'==', '!=', '<', '<=', '>', '>=',
		# Arithmetic
		'\+', '-', '\*', '/', '//', '\%', '\*\*',
		# In-place
		'\+=', '-=', '\*=', '/=', '\%=',
		# Bitwise
		'\^', '\|', '\&', '\~', '>>', '<<',
		# more operators
		'\$'
	]

	# Python braces
	braces = [
		'\{', '\}', '\(', '\)', '\[', '\]',
	]

	def __init__(self, document):
		QSyntaxHighlighter.__init__(self, document)

		# Multi-line strings (expression, flag, style)
		# FIXME: The triple-quotes in these two lines will mess up the
		# syntax highlighting from this point onward
		self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
		self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

		rules = []

		# Keyword, operator, and brace rules
		rules += [(r'\b%s\b' % w, 0, STYLES['command']) for w in GNUplotHighlighter.commands]
		rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in GNUplotHighlighter.keywords]
		rules += [(r'\b%s\b' % w, 0, STYLES['math']) for w in GNUplotHighlighter.math_functions]
		rules += [(r'%s' % o, 0, STYLES['operator']) for o in GNUplotHighlighter.operators]
		rules += [(r'%s' % b, 0, STYLES['brace']) for b in GNUplotHighlighter.braces]

		# All other rules
		rules += [

			# From '#' until a newline
			(r'#[^\n]*', 0, STYLES['comment']),

			# Double-quoted string, possibly containing escape sequences
			(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
			# Single-quoted string, possibly containing escape sequences
			(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

			# Numeric literals
			(r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
		]

		# Build a QRegExp for each pattern
		self.rules = [(QRegExp(pat), index, fmt)for (pat, index, fmt) in rules]

	def highlightBlock(self, text):
		"""Apply syntax highlighting to the given block of text.
		"""
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)

			while index >= 0:
				# We actually want the index of the nth match
				index = expression.pos(nth)
				length = expression.cap(nth).length()
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		# Do multi-line strings
		in_multiline = self.match_multiline(text, *self.tri_single)
		if not in_multiline:
			in_multiline = self.match_multiline(text, *self.tri_double)

	def match_multiline(self, text, delimiter, in_state, style):
		"""Do highlighting of multi-line strings. ``delimiter`` should be a
		``QRegExp`` for triple-single-quotes or triple-double-quotes, and
		``in_state`` should be a unique integer to represent the corresponding
		state changes when inside those strings. Returns True if we're still
		inside a multi-line string when this function is finished.
		"""
		# If inside triple-single quotes, start at 0
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		# Otherwise, look for the delimiter on this line
		else:
			start = delimiter.indexIn(text)
			# Move past this match
			add = delimiter.matchedLength()

		# As long as there's a delimiter match on this line...
		while start >= 0:
			# Look for the ending delimiter
			end = delimiter.indexIn(text, start + add)
			# Ending delimiter on this line?
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			# No; multi-line string
			else:
				self.setCurrentBlockState(in_state)
				length = text.length() - start + add
			# Apply formatting
			self.setFormat(start, length, style)
			# Look for the next match
			start = delimiter.indexIn(text, start + length)

		# Return True if still inside a multi-line string, False otherwise
		if self.currentBlockState() == in_state:
			return True
		else:
			return False


class NumberBar(QWidget):
	def __init__(self, parent=None):
		super(NumberBar, self).__init__(parent)

	def construct(self, parent2):
		self.field_script = parent2
		layout = QVBoxLayout()
		self.setLayout(layout)
		self.field_script.blockCountChanged.connect(self.update_width)
		self.field_script.updateRequest.connect(self.update_on_scroll)
		self.update_width('1')

	def update_on_scroll(self, rect, scroll):
		if self.isVisible():
			if scroll:
				self.scroll(0, scroll)
			else:
				self.update()

	def update_width(self, string):
		width = self.fontMetrics().width(unicode(string)) + 20
		if self.width() != width:
			self.setFixedWidth(width)

	def paintEvent(self, event):
		if self.isVisible():
			block = self.field_script.firstVisibleBlock()
			height = self.fontMetrics().height()
			number = block.blockNumber()
			painter = QPainter(self)
			painter.fillRect(event.rect(), NUMBER_BAR_COLOR)
			font = painter.font()

			current_block = self.field_script.textCursor().block().blockNumber() + 1

			condition = True
			while block.isValid() and condition:
				block_geometry = self.field_script.blockBoundingGeometry(block)
				offset = self.field_script.contentOffset()
				block_top = block_geometry.translated(offset).top()
				number += 1

				rect = QRect(0, block_top, self.width() - 5, height)

				if number == current_block:
					font.setBold(True)
				else:
					font.setBold(False)

				painter.setFont(font)
				painter.drawText(rect, Qt.AlignRight, '%i' % number)

				if block_top > event.rect().bottom():
					condition = False
				block = block.next()
			painter.end()


if __name__ == '__main__':
	pass
