import network
import os

class Node:
	""" class for nodes """
	#node's ip address
	my_ip = 0
	
	#true if node is a bs
	is_bs = False
	
	#ctor
	def __init__(self, is_bs):
		self.is_bs = is_bs
		self.my_ip = network.get_ip()
	
	def query(self, filename, dest_ip, query_type, timestamp, bs_ip):
		#retrieve my node's ip
		os.system('echo "' + filename + ' ' + dest_ip + ' ' + query_type + ' ' + str(timestamp) + ' " > bsfile.txt')
	 	
		#tell ip my_ip and filename
		return (network.put("bsfile.txt", bs_ip) == 0)

	#check ip_list for existence of file (only called if node is bs)
	def search(self, filename, dest_ip, query_type, timestamp):
		timestamp = int(timestamp) - 1
		
		with open("Addresses/ip_list.txt") as file:
			ip_list = [x.replace("\n", "") for x in file.read().splitlines()]
			
		with open("Addresses/bs_list.txt") as file:
			bs_list = [x.replace("\n", "") for x in file.read().splitlines()]
		
		if (timestamp == -1):
			#ask original query if received
			finished = (network.put("", dest_ip) != 0)
			if finished: return

			timestamp = NUM_BACKUPS
			for bs_ip in bs_list:
				if self.query(filename, dest_ip, query_type, timestamp, bs_ip):
					break
		
		for bs_ip in bs_list:
			if query(filename, dest_ip, query_type, timestamp, bs_ip):
				break

		for ip in ip_list:
			if (ip == dest_ip): continue
			os.system("python main.py -c " + filename + " " + ip)
			with open("Posts/" + filename) as file:
				result = file.read()
			
			#if found file
			if (result != ""):
				finished = True
				network.put(filename, dest_ip)
			else:
				finished = False
				
			os.system("rm -f Posts/" + filename)
			
			if (finished):
				return

	def serve(self):
		while (True):
			#start network server daemon
			os.system("nc -l 4444 > input_file.txt")
			
			if (not self.is_bs):	
				#start pam up
				network.pamela_handle_request()
			else:
				#start handgie up
				l = network.handgelina_jolie_request()
				#string to save content
				content = ""
				filename = l[0]
				dest_ip = l[1]
				query_type = l[2]

				if (query_type == 'query'):
					timestamp = l[3]
					self.search(filename, dest_ip, query_type, timestamp)
				else:
					for i in range(3, len(l)):
						content = content + l[i] + " "
					
					content = content[:-1]
					self.distribute(l[0], l[1], content)
					
	def distribute(self, user, num_posts, content):
		with open("Addresses/ip_list.txt") as file:
			ip_list = [x.replace("\n", "") for x in file.read().splitlines()]

		index = hash(user + num_posts) % len(ip_list)
		ip = ip_list[index]
		os.system('echo "' + user + ' ' + num_posts + ' post ' + content + '" > puddin.txt')
		network.put("puddin.txt", ip)
		
	def post(self, content):
		with open("Meta/profile.txt") as file:
			user, num_posts = file.read().split()
		
		with open("Addresses/bs_list.txt") as file:
			bs_list = [x.replace("\n", "") for x in file.read().splitlines()]
		
		os.system('echo "' + user + ' ' + num_posts + ' post ' + content + '" > post.txt')
		
		for bs_ip in bs_list:
			if bs_ip == self.my_ip:
				continue
			if (network.put("post.txt", bs_ip) == 0):
				break
		
		if self.is_bs:
			self.distribute(user, num_posts, content)
		
		updated = user + " " + str(int(num_posts) + 1)
		with open("Meta/profile.txt", "w") as file:
			file.write(updated)
		
	def quiz(self, filename, query_type, timestamp):
		if (query_type == 'post'):
			with open('Posts/' + filename) as file:
				stuff = file.read()
				self.post(stuff)
		else:
			with open('Addresses/bs_list.txt') as file:
				bs_list = [x.replace("\n", "") for x in file.read().splitlines()]
			for bs_ip in bs_list:
				if self.query(filename, self.my_ip, 'query', timestamp, bs_ip):
					break
		
