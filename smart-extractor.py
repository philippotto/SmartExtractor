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

	sp.wait()

# with open("output.txt", "w") as f:
# 	f.write(str(sys.argv))

archiveName = sys.argv[1]
pureArchiveName = ".".join(archiveName.split(".")[0:-1]) if "." in archiveName else archiveName

targetPath = disambiguate(pureArchiveName)
os.makedirs(targetPath)


cmd = ["C:\\Program Files\\7-Zip\\7z.exe", "x", archiveName, "-o" + targetPath, "-aou"]
execute(cmd)

folderElements = os.listdir(targetPath)

if len(folderElements) == 1:
	fileToMove = folderElements[0]
	hoistedPath = disambiguate(fileToMove)

 	shutil.move(targetPath + "\\" + fileToMove, hoistedPath)
 	os.rmdir(targetPath)

