# -*- coding: UTF-8 -*-

import json
from tools.strings import lineconcatenate
from tools.dictionaries import dic2sty
import tools.paths as Path

from Gplot import gnuplotVersion

GlobalDics = []
GPVERSION = gnuplotVersion()

manifest = {
	"name": "Default",
	"author": "Cristian Gonzalez",
	"comments": "These are the definitions to be used in the book.",
	"notes": '\"items to represent informations have different colors, the important factor for the lines is separed by geometry.\"',
	"version": float(GPVERSION)
}

dic2sty(manifest, Path.makePath(['styles', 'default', 'manifest.txt']))

BASECOLORS = ['#808080', '#0E3D59', '#88A61B', '#F29F05', '#F25C05', '#D92525']  # contrast
BASECOLORNAME = ['Gray', 'Blue', 'Green', 'Yellow', 'Orange', 'Red']  # contrast
EXTRACOLORS = ['#174F80', '#427097', '#7093B1', '#9AAFC3', '#313131']  # blue set
EXTRACOLORNAME = ['Blue 0', 'Blue 1', 'Blue 2', 'Blue 3', 'Blue 4']  # contrast


if GPVERSION < 5.0:
	DASHTYPE = [1, 2, 4, 5, 3]
else:
	DASHTYPE = [1, "_", ".-", "..-", "."]
DASHTYPENAME = ['Continus', "--", ".-", "..-", ".."]


class Format():
	def __init__(self):
		pass

	def getFormat(self):
		str_ = self.header_s
		for i in range(0, len(self.mapping)):
			key = self.mapping[i]
			value = '<value>'
			if key in ('comment', 'cmt'):
				key = '# <comment>'
				value = ''
			str_ += lineconcatenate([key, value])
		return str_

	def toSave(self):
		dict_ = self.getStyle(dict_=1)
		dict_['index'] = self.index
		return dict_

	def addParam(self, param, value):
		if value is None:
			return
		if param in self.alias.keys():
			param = self.alias[param]
		if param not in (self.lineStyle.keys() + self.alias.keys()):
			return
		str_ = lineconcatenate([param, value])
		self.lineStyle[param] = value
		return str_

	def getStyle(self, dict_=False):
		str_ = self.header
		style = {}
		for i in range(0, len(self.mapping)):
			key = self.mapping[i]
			value = self.lineStyle[key]
			if value is None and not dict_:
				continue
			style[key] = self.lineStyle[key]
			str_ += lineconcatenate([key, json.dumps(value)])
		if dict_:
			return style
		return str_


class NewArrowStyle(Format):
	def __init__(self, index, heads=None, size=None, head_style=None, plane=None, linestyle=None, dashtype=None, comment=' '):
		self.index = str(index)

		self.mapping = ['head', 'size', 'filled', 'arrange', 'linestyle', 'dashtype', 'comment']
		self.alias = {'ls': self.mapping[4], 'dt': self.mapping[5]}
		if GPVERSION < 5.0:
			self.mapping[5] = 'linetype'
			self.alias = {'ls': self.mapping[4], 'lt': self.mapping[5]}
		self.nokey = [self.mapping[4], self.mapping[5]]

		if GPVERSION < 5.0:
			head_style = None
			self.alias = {'ls': self.mapping[4], 'lt': self.mapping[5]}
		map_ = self.mapping

		self.header = lineconcatenate(['set style arrow ', index])
		self.header_s = 'set style arrow <index>'

		self.lineStyle = {
			map_[0]: heads,
			map_[1]: size,
			map_[2]: head_style,
			map_[3]: plane,
			map_[4]: linestyle,
			map_[5]: dashtype,
			map_[6]: "#" + comment.replace('#', '').strip()
		}
		GlobalDics.append(self.toSave())
		print self.getStyle()

	def getStyle(self, dict_=False):
		str_ = self.header
		style = {}
		for i in range(0, len(self.mapping)):
			key = self.mapping[i]
			value = self.lineStyle[key]
			if value is None and not dict_:
				continue
			style[key] = self.lineStyle[key]
			if key in (self.nokey):
				str_ += lineconcatenate([key, json.dumps(value)])
			else:
				str_ += lineconcatenate([value, ])

		if dict_:
			return style
		return str_


class ArrowStyle(Format):
	def __init__(self, style):
		self.Style = style
		if 'index' not in self.Style.keys():
			self.Style['index'] = 1
		self.properties()

	def properties(self):
		self.keys = ['head', 'size', 'filled', 'arrange', 'linestyle', 'dashtype', 'comment']
		if GPVERSION < 5.0:
			self.keys[5] = 'linetype'

		if self.Style['comment'].strip()[0] is not '#':
			self.Style['comment'] = '#' + str(self.Style['comment'])

		self.header = 'set style arrow ' + str(self.Style['index']) + ' '
		self.header_f = 'set style arrow <int>'

		map_ = self.keys
		self.alias = {'ls': map_[3], 'dt': map_[4]}
		if GPVERSION < 5.0:
			self.alias = {'ls': map_[3], 'lt': map_[4]}
		self.nokey = [map_[0], map_[2], map_[3], map_[6]]
		self.nouse = []

	def getStyle(self, dict_=False):
		str_ = self.header
		style = {}
		for i in range(0, len(self.keys)):
			key = self.keys[i]
			value = self.Style[key]
			if value is None and not dict_:
				continue
			style[key] = self.Style[key]
			if key in (self.nouse):
				continue
			if key in (self.nokey):
				str_ += lineconcatenate([value, ])
			elif 'color' in key:
				str_ += lineconcatenate([key, 'rgb ', json.dumps(value)])
			else:
				if key == 'size':
					str_ += lineconcatenate([key, value])
				else:
					str_ += lineconcatenate([key, json.dumps(value)])
		if dict_:
			return style
		return str_

	def getInsert(self):
		return 'set arrow ' + str(self.Style['index']) + ' from <x1>,<y1> to <x2>,<y2> arrowstyle ' + str(self.Style['index']) + '# vector'


class LineStyle(Format):
	def __init__(self, style):
		self.Style = style
		if 'index' not in self.Style.keys():
			self.Style['index'] = 1
		self.properties()

	def properties(self):
		self.keys = ['linetype', 'linecolor', 'linewidth', 'pointtype', 'pointsize', 'comment', 'index']

		if self.Style['comment'].strip()[0] is not '#':
			self.Style['comment'] = '#' + str(self.Style['comment']).strip()

		if GPVERSION < 5.0:
			self.header = 'set linestyle ' + str(self.Style['index']) + ' '
			self.header_f = 'set linestyle <int>'
		else:
			self.header = 'set style line ' + str(self.Style['index']) + ' '
			self.header_f = 'set style line <int>'

		map_ = self.keys
		self.alias = {'lt': map_[0], 'lc': map_[1], 'lw': map_[2], 'pt': map_[3], 'ps': map_[4], 'cmt': map_[5], 'idx': map_[6]}
		self.nokey = [map_[5]]
		self.nouse = [map_[6]]

	def getStyle(self, dict_=False):
		str_ = self.header
		style = {}
		for i in range(0, len(self.keys)):
			key = self.keys[i]
			value = self.Style[key]
			if value is None and not dict_:
				continue
			style[key] = self.Style[key]
			if key in (self.nouse):
				continue
			if key in (self.nokey):
				str_ += lineconcatenate([value, ])
			elif 'color' in key:
				str_ += lineconcatenate([key, 'rgb ', json.dumps(value)])
			else:
				str_ += lineconcatenate([key, json.dumps(value)])
		if dict_:
			return style
		return str_

	def getInsert(self):
		return 'set arrow from <x1>,<y1> to <x2>,<y2> linestyle ' + str(self.Style['index']) + '# flat line, no heads'


class NewLineStyle(Format):
	def __init__(self, index, linetype=None, linecolor=None, linewidth=None, pointtype=None, pointsize=None, comment=None):
		self.index = int(index)
		self.mapping = ['linetype', 'linecolor', 'linewidth', 'pointtype', 'pointsize', 'comment']
		self.nouse = []
		self.nokey = [self.mapping[5]]
		map_ = self.mapping
		self.alias = {'lt': map_[0], 'lc': map_[1], 'lw': map_[2], 'pt': map_[3], 'ps': map_[4], 'cmt': map_[5]}

		if comment:
			comment = '# ' + str(comment)
		if GPVERSION < 5.0:
			self.header = 'set linestyle ' + str(self.index) + ' '
			self.header_s = 'set linestyle <int>'
		else:
			self.header = 'set styleline ' + str(self.index) + ' '
			self.header_s = 'set styleline <int>'
		self.lineStyle = {
			map_[0]: linetype,
			map_[1]: linecolor,
			map_[2]: linewidth,
			map_[3]: pointtype,
			map_[4]: pointsize,
			map_[5]: comment
		}

		GlobalDics.append(self.toSave())
		print self.getStyle()

	def getStyle(self, dict_=False):
		str_ = self.header
		style = {}
		for i in range(0, len(self.mapping)):
			key = self.mapping[i]
			value = self.lineStyle[key]
			if value is None and not dict_:
				continue
			style[key] = self.lineStyle[key]
			if key in (self.nouse):
				str_ += lineconcatenate([value, ])
			if key in (self.nokey):
				str_ += lineconcatenate([value, ])
			elif key == self.mapping[1]:
				str_ += lineconcatenate([key, 'rgb ', json.dumps(value)])
			else:
				str_ += lineconcatenate([key, json.dumps(value)])
		if dict_:
			return style
		return str_


class Label(Format):
	def __init__(self, type_, label, offset=None, font=None, linetype=None, pointtype=None, enhanced=None, angle=None):
		type_ = str(type_).lower()
		self.mapping = ['offset', 'font', 'textcolor', 'linetype', 'enhanced', 'rotate']
		map_ = self.mapping
		self.alias = {'tc': map_[2], 'lt': map_[3], 'angle': map_[5]}

		self.header = lineconcatenate(['set', type_, '"' + label + '"'])
		self.header_s = lineconcatenate(['set', '<xlabel|ylabel|title>', '"' + label + '"'])

		self.lineStyle = {
			map_[0]: offset,
			map_[1]: font,
			map_[2]: linetype,
			map_[3]: pointtype,
			map_[4]: enhanced,
			map_[5]: angle
		}


if __name__ == '__main__':

	lines_styles = True  # True
	vectors = True
	arrow_type = True
	lines_type = True

	colors = BASECOLORS + EXTRACOLORS
	names = BASECOLORNAME + EXTRACOLORNAME

	if lines_styles:  # base linetype
		'''
		Here defines all the kind of lines that might exist.
		The firstone is the gray for the axes and the come the basic one for the vectortype
		and the extra for the other lines
		'''
		GlobalDics = []
		for i in range(0, len(colors)):
			color = colors[i]
			name = 'Line ' + names[i]
			NewLineStyle(1 + i, linecolor=color, linetype=None, linewidth=0.3, comment=name)
		dic2sty(GlobalDics, Path.makePath(['styles', 'default', 'lines.sty']))

	count = 1
	if vectors:  # base arrowtype
		''' here are defined the axis options '''
		GlobalDics = []
		NewArrowStyle(1, heads='head', head_style='nofilled', plane='back', dashtype=1, linestyle=1, comment="Axis like, single head")
		NewArrowStyle(2, heads='heads', head_style='nofilled', plane='back', dashtype=1, linestyle=1, comment="Axis like, double head")
		count += 2

		'''
		here are defined all the posibilities for the vectors.
		They need to have different dashtype and color, the most important parameter is the dashtype
		beause is the only one that can be identified when printed in white an black
		'''
		combinations = min(len(BASECOLORS), len(DASHTYPE))
		for i in range(0, combinations):
			color = BASECOLORS[i]
			dash = DASHTYPE[i]
			dashN = DASHTYPENAME[i]
			NewArrowStyle(i + count, heads='head', size='screen 0.04,15,45', head_style='noborder', plane='front', dashtype=dash, linestyle=i + count-1, comment='Type ' + str(i + 1) + ':' + str(dashN))
		count += combinations
		dic2sty(GlobalDics, Path.makePath(['styles', 'default', 'vectors.sty']))
	vectors_end = count

	if arrow_type:  # base arrowtype
		'''
		Here defines all the kind of lines that might exist.
		The firstone is the gray for the axes
		'''
		GlobalDics = []
		for i in range(0, len(EXTRACOLORS)):
			color = EXTRACOLORS[i]
			name = EXTRACOLORNAME[i]
			NewArrowStyle(count + i, heads='head', head_style='noborder', plane='front', dashtype=1, linestyle=vectors_end + i, comment='simple ' + name + ' line')
		count += len(EXTRACOLORS)
		dic2sty(GlobalDics, Path.makePath(['styles', 'default', 'arrows.sty']))

	if lines_type:  # base arrowtype
		'''
		Here defines all the kind of lines that might exist.
		The firstone is the gray for the axes
		'''
		GlobalDics = []
		for i in range(0, len(EXTRACOLORS)):
			color = EXTRACOLORS[i]
			name = EXTRACOLORNAME[i]
			NewArrowStyle(count + i, heads='nohead', head_style='empty', plane='front', dashtype=1, linestyle=vectors_end + i, comment='simple ' + name + ' line')
		count += len(EXTRACOLORS)
		dic2sty(GlobalDics, Path.makePath(['styles', 'default', 'lines_raw.sty']))
	print "Total elements created: ", count
