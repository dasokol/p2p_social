""" Python module for sending and retrieving files through telnet """

import os

""" handles incoming file requests from other nodes 
    returns true if file is found returns false otherwise
"""
def pamela_handle_request():
	#retrieve filename and dest ip address
	with open("input_file.txt") as file:
		l = file.read()
	
	if (l != ""):
		if len(l.split()) == 2:
			filename, dest_ip = (text.split())
		else:
			handle_hathaway(l)
			return

		#check for files existance and send file if exists
		with open ("Posts/" + filename) as file:
			if (file.read() == ""):
				os.system("sudo rm -f /Posts" + filename)
				network.put("", dest_ip)
			else:
				network.put(filename, dest_ip)

def handgelina_jolie_request():
	with open("input_file.txt") as file:
		return file.read().split()

def handle_hathaway(line):
	l = line.split()
	s = ""

	for i in range(3, len(l)):
		s = s + l[i] + " "

	s = s[:-1]
	with open("Posts/" + l[0] + l[1] + '.txt', "w") as file:
		file.write(s)
	
			
	
	

""" returns caller's ip address """
def get_ip():
	os.system('ip addr | grep "inet " | grep -v 127.0.0 > ipfile.txt')
	
	with open("ipfile.txt") as file:
		str = file.read()
	
	ip_str = str.split()[1]
	
	return ip_str.split("/")[0]

""" requests a netcat transfer from ip address ip """
def request(filename, ip):
	#retrieve my node's ip
	my_ip = get_ip()
	os.system('echo "' + filename + ' ' + my_ip + ' " > ipfile.txt')
	 
	#tell ip my_ip and filename
	put("ipfile.txt", ip)

""" retrieves filename from ip address ip """
def get(filename, ip):
	#request file from ip
	request(filename, ip)

	#open netcat listener
	os.system("nc -l 4444 > Posts/" + filename)	

""" sends file to ip """
def put(filename, ip):
	if (filename == ""):
		return os.system("echo '' | nc " + ip + " 4444")
	else:
		return os.system("cat " + filename + " | nc " + ip + " 4444")
