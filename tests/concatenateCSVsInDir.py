
from os import listdir
from os.path import isfile, join
import sys

def create_concatenated_csv(path, csvfiles,  output):
	fout=open(output,"a")
	for csvfile in csvfiles:
	    f = open(join(path, csvfile))
	    for line in f:
	         fout.write(line)
	    f.close() # not really needed
	fout.close()
	print "Done!"

def main(argv):
	if (3 != len(sys.argv)):
		print "incorrect argument length!"
		return 0

	path = str(sys.argv[1])
	csvfiles = [f for f in listdir(path) if isfile(join(path,f))]

	create_concatenated_csv(path, csvfiles, sys.argv[2])
	print "Successfully merged all csv files into ", sys.argv[2], ".csv"

if __name__ == '__main__': main(sys.argv[1:])