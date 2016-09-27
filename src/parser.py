# -*- coding: utf-8 -*-
from tools.dictionaries import file2dic
from tools.dictionaries import existsKeyInDictionary
import tools.paths as paths

def plotConfig(path, filename, new=False):
	dict_ = {}
	if not path or not filename:
		return
	if not new:
		dict_ = file2dic(path)

	'''
	Checks for missing information. If something does not exist in the
	dictionary, it will be created.
	'''
	if not existsKeyInDictionary('FIGoutput', dict_):
		dict_['FIGoutput'] = filename
	if not existsKeyInDictionary('template', dict_):
		dict_['template'] = paths.makePath(['styles', 'default'])
	if not existsKeyInDictionary('scriptFile', dict_):
		dict_['scriptFile'] = filename + '.gnu'
	if not existsKeyInDictionary('size', dict_):
		dict_['size'] = [5, 5]
	if not existsKeyInDictionary('xfig', dict_):
		dict_['xfig'] = True
	if not existsKeyInDictionary('replacements', dict_):
		dict_['replacements'] = []

	return dict_
