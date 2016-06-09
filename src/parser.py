# -*- coding: utf-8 -*-
from tools.dictionaries import file2dic


def plotConfig(path, filename, new=False):
	dict_ = {}
	if not path or not filename:
		return
	if not new:
		dict_ = file2dic(path)

	if 'FIGoutput' not in dict_.keys():
		dict_['FIGoutput'] = filename + '.fig'
	if 'EPSoutput' not in dict_.keys():
		dict_['EPSoutput'] = filename + '.eps'
	if 'template' not in dict_.keys():
		dict_['template'] = 'styles/default'
	if 'scriptFile' not in dict_.keys():
		dict_['scriptFile'] = filename + '.gnu'
	if 'size' not in dict_.keys():
		dict_['size'] = [5, 5]
	if 'xfig' not in dict_.keys():
		dict_['xfig'] = False
	if 'replacements' not in dict_.keys():
		dict_['replacements'] = False

	return dict_
