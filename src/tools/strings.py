# -*- coding: utf-8 -*-

def lineconcatenate(array):
	str_ = ' '
	for i in range(0, len(array)):
		str_ += str(array[i]).strip() + ' '
	return str_.strip() + ' '
