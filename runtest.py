#!/usr/bin/env python

import socket #socket implementation
import argparse #parser for opt-line
import os #system command execution
import time #sleep function
import sys #system-level information

def test_case1(ip_addr, ip_port):

	# Connect to the server
	# Send send a sequence of messages
	# Sent messages shall be equal to recieved messages

	print 'Test Case 1 started'
	print 'Trying to send echo messages......\n'
	os.system("g++ server.cpp -lpthread -o echo_server.out")
	os.system("./echo_server.out " + ip_port + " > /dev/null 2>&1 &") #run server at background "> /dev/null 2>&1" means no output

	TCP_IP = ip_addr
	TCP_PORT = ip_port
	test_string = 'HELLO SERVER!'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(2) #sleep for sometime until server will start
	s.connect ( ( TCP_IP, int(TCP_PORT) ) )

	result = 0
	for x in range(0, 5) :
		print test_string

		s.send(test_string) # echo
		recv_string = s.recv(len(test_string)) # recieve echo message
		print recv_string, '\n'
		if recv_string != test_string :
			result = -1
			break
		test_string = test_string + str(x)

	s.close()

	if result == 0 :
		print 'PASSED \n'
	else:
		print 'FAILED \n'
	
	if os.system("pidof echo_server.out > /dev/null 2>&1") != 256:
		os.system("pkill echo_server.out") 
	os.system("rm -f ./echo_server.out") 
	return result

def test_case2(ip_addr, ip_port) :

	# Connect to the server
	# Send "exit" message
	# Server shall shutdown

	print 'Test Case 2 started'
	print 'Trying to test "exit" message - server must shutdown......\n'
	os.system("g++ server.cpp -lpthread -o echo_server.out")
	os.system("./echo_server.out " + ip_port + " > /dev/null 2>&1 &")

	test_string = 'exit'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(2) 
	s.connect ( ( ip_addr, int( ip_port ) ) )

	s.send(test_string) #send 'exit' message to stop the server
	s.close()

	result = 0
	if os.system("pidof echo_server.out > /dev/null 2>&1") == 256:
		print 'PASSED \n'
		result = 0
	else :
		print 'FAILED \n'
		os.system("pkill echo_server.out") 
		result = -1
	os.system("rm -f ./echo_server.out")
	return result

def test_case3(ip_addr, ip_port) :
	
	# Connect to the server;
	# Terminate connection;
	# Connect to the server again.
	# Server shall wait for the new connection.

	print 'Test Case 3 started'
	print 'Trying to connect to the server two times, one after another. Server must wait for the new connection......\n'
	os.system("g++ server.cpp -lpthread -o echo_server.out")
	os.system("./echo_server.out " + ip_port + " > /dev/null 2>&1 &")

	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(2) 
	try:
		s1.connect ( ( ip_addr, int( ip_port ) ) )
	except socket.error, e:
		print 'Failed to connect Client_1 %s' % (e)
	s1.close()

	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(2) 
	result = 0
	try:
		s2.connect ( ( ip_addr, int( ip_port ) ) )
		print 'PASSED \n' 
	except socket.error, e:
		print 'Failed to connect Client_2 %s' % (e)
		print 'FAILED \n'
		result = -1 # means error
	s2.close()

	if os.system("pidof echo_server.out > /dev/null 2>&1") != 256:
		os.system("pkill echo_server.out") 
	os.system("rm -f ./echo_server.out")
	return result

def test_case4(ip_addr, ip_port) :

	# Connect to the server
	# Send an echo message
	# Wait for 10 sec
	# Read message
	# Server shall not close the connection

	print 'Test Case 4 started'
	print 'Trying to send message and read it after 10 sec......\n'
	os.system("g++ server.cpp -lpthread -o echo_server.out")
	os.system("./echo_server.out " + ip_port + " > /dev/null 2>&1 &")

	test_string = 'HELLO SERVER!'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(2) 
	s.connect ( ( ip_addr, int( ip_port ) ) )

	print test_string

	result = 0
	s.send(test_string) # echo
	time.sleep(10)
	recv_string = s.recv(len(test_string)) # recieve echo message
	print recv_string, '\n'
	
	if recv_string != test_string :
		print 'FAILED \n'
		result = -1
	else :
		print 'PASSED \n'

	if os.system("pidof echo_server.out > /dev/null 2>&1") != 256:
		os.system("pkill echo_server.out") 
	os.system("rm -f ./echo_server.out") 
	return result



def main():

	print '\n\n\n'
	ip_addr = '127.0.0.1' # server address
	parser = argparse.ArgumentParser(add_help=False, description='## This runtest.py builds the server executable and runs automated tests ##')
	parser.add_argument('-p', '--port', default='1234', 
				help='server connection port number (if no port provided, PORT=1234)') # if no port number supplied, 1234 is a default one
	if len(sys.argv)==1:
		parser.print_help()
	args=parser.parse_args()
	print '\n\n\n'
	print '----------------TEST FRAMEWORK for TCP server---------------'
	print 'Ip adress for testing server is: [%s]\n' % ip_addr
	print 'Port number for testing server is: [%s]\n' % args.port
	print 'Start testing......................\n\n\n\n\n\n\n\n'
	counter = 0
	counter += test_case1(ip_addr, args.port)
	counter += test_case2(ip_addr, args.port)
	counter += test_case3(ip_addr, args.port)
	counter += test_case4(ip_addr, args.port)
	print '----TOTALLY----\n'
	print 'tests passed ', (4-counter)
	print 'tests failed ', (counter)
	print '----------------TEST FRAMEWORK---------------'

main()