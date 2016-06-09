# -*- coding: UTF-8 -*-
from files import writestring2File

import yaml


def dic2sty(GlobalDics, file_):
	# needs to be removed
	dic2file(GlobalDics, file_)


def dic2file(dict_, file_):
	''' This method saves the given dictionary in the given file '''
	writestring2File(file_, yaml.dump(dict_, Dumper=yaml.Dumper, default_flow_style=False))


def str2dic(str_):
	return yaml.load(str_)


def file2dic(path):
	return yaml.load(file(path, 'r'))


def dic2str(dict_):
	return yaml.dump(dict_, default_flow_style=False)
