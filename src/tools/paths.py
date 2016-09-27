import os

def getPathData(path):
	'''
	This method returns the data from the given path
	basename : name without extension (ussualy plt)
	fileName : name of the file, it includes the extension
	mainpath : pathToFile
	'''
	if not path:
		return False

	pathToFile = str2path(path)

	if not pathToFile:
		return False
	# takes the path to the folder where the file is located
	folder = os.path.dirname(pathToFile)
	# saves if it is possible to write in that folder
	isValid = os.access(folder, os.W_OK)

	if not isValid:
		# if it is not possible to write there, nothing to do
		return False
	# up to here, the file is valid and it is possible to write in the folder, then
	# it creates the dictionary with the data

	projectFiles = {}
	projectFiles["folder"] = os.path.dirname(pathToFile)
	projectFiles["fileName"] = os.path.basename(pathToFile)
	projectFiles["baseName"] = os.path.splitext(projectFiles["fileName"])[0]
	projectFiles["mainPath"] = pathToFile

	return projectFiles


def str2path(str_):
	return os.path.abspath(str(str_))


def folderPlusFile(folder, file_):
	return makePath([folder, file_])


def makePath(components):
	return os.path.join(*components)
