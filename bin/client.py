import socket, sys
import os
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__),'...'))

#######################################################################
#This script takes 2 command line arguments (host and port)
#  Test a straight up GET
#  Test a form submission GET (unit_conversion)
#  Image retrieval
#
#Reference:
#    http://effbot.org/zone/socket-intro.htm
#    "Example: read a document via HTTP (File:httpget1.py)"
#How to run:
#   python client.py arctic.cse.msu.edu  portNumber
#####################################################################

def test_main(args):
	#check for # of inputs
	if len(args) < 3:
		print "There must be 3 inputs you lose.... fine I'll show you the correct format"
		print "Correct formatting is: client.py url port"
		return -1
		#program exits out

	host = args[1]
	port = int(args[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.send ("GET / HTTP/1.0\r\n\r\n")

	result = ""
	while True:
		buf = s.recv(1000)  #why is buffer a type?????
		if not buf:
			break
		result += buf

	s.close()

	present = False
	if "Drinkz" in result:
		present = True

	assert present


#################################
# test the unit_conversion form
# pass in 1 gallon
# result should be 3785.41 ml
#################################

def test_form_unit_conversion(args):
		#check for # of inputs
	if len(args) < 3:
		print "There must be 3 inputs you lose.... fine I'll show you the correct format"
		print "Correct formatting is: client.py url port"
		return -1
		#program exits out

	host = args[1]
	port = int(args[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.send ("GET /convert_all_the_things_recv?InputAmt=1+gallon HTTP/1.0\r\n\r\n")

	result = ""
	while True:
		buf = s.recv(1000)  #why is buffer a type?????
		if not buf:
			break
		result += 

	s.close()

	present = False
	if "3785.41 mL" in result:
		present = True

	assert present




