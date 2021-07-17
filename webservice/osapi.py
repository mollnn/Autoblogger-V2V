import os
def getFileList(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def getBinaryFile(filename):
	f = open(filename, "rb")
	data = f.read()
	f.close()
	return data