import network
import node
import sys
import os

""" things to send: filename, filetype, timestamp,  """

#global number of backups
NUM_BACKUPS = 1	

def main():
	n = node.Node(True)

	#argv[3] is the ip address for the server
	if (sys.argv[1] == "-c"):
		n.quiz(sys.argv[2], sys.argv[3], NUM_BACKUPS)

	elif (sys.argv[1] == "-s"):
		n.serve()

if __name__ == "__main__":
	main()

