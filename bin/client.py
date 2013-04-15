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


##########################################
#Test image_retrieval
#########################################
def test_image_retrieval(args):
    #Check for right number of inputs
    if len(args) < 3:
        #Show error message
        print "Incorrect number of inputs"
        print "Try: client.py url port"
        #Terminate the program
        return -1

    host = args[1]
    port = int(args[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("GET /view_image.html HTTP/1.0\r\n\r\n")
    
    fp = s.makefile("request_image")
    #search for the length of the image
    for line in fp:
	if "Content-Length: " in line:
		length = int(line.strip("Content-Length: "))
		break

     
    #manually get the image length
    pth = os.path.dirname(__file__)
    filename = pth +"/../drinkz/searchbyspirit.jpg"
    manual = open(filename,"r")
    value = ""
    for line in manual:
	value+=line

    s.close()

    #Check if image has the same length
    assert length == len(value)
    print "Test image retrieval: passed"

if __name__ == '__main__':
    #Test a straight up GET
    test_main(sys.argv)
    #test form unit_conversion
    test_form_unit_conversion(sys.argv)
    #test image retrieval
    test_image_retrieval(sys.argv)



