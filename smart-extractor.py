import sys, os, subprocess
import shutil


def disambiguate(path):

	newpath = path
	disambiguate = 2
	while os.path.exists(newpath):
		newpath = path + " " + str(disambiguate)
		disambiguate += 1
	return newpath


def execute(cmd):
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

	sp = subprocess.Popen(cmd,
		startupinfo=startupinfo,
		shell=True)

	exitcode = sp.wait()
	if exitcode != 0:
		raise Exception("Exception was raised while executing 7z. Exitcode " + str(exitcode))


def createWrappingFolder(archiveName):

	pureArchiveName = ".".join(archiveName.split(".")[0:-1]) if "." in archiveName else archiveName

	targetPath = disambiguate(pureArchiveName)
	os.makedirs(targetPath)
	return targetPath


def extractAndMove(archiveName, targetPath):

	execute(["7z.exe", "x", archiveName, "-o" + targetPath, "-aou"])

	folderElements = os.listdir(targetPath)

	if len(folderElements) == 1:
		fileToMove = folderElements[0]
		hoistedPath = disambiguate(fileToMove)

	 	shutil.move(targetPath + "\\" + fileToMove, hoistedPath)
	 	os.rmdir(targetPath)


def smartExtract(archiveName):

	try:
		targetPath = createWrappingFolder(archiveName)
		extractAndMove(archiveName, targetPath)
	except Exception, e:
		print(e)
		# delete the wrapping folder
	 	shutil.rmtree(targetPath)
	 	input("Press Enter to exit...")

smartExtract(sys.argv[1])