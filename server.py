#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data.decode())
        response = self.parse(self.data.decode())
        self.request.sendall(response.encode())
    
    def parse(self,request):
    	request_content = request.split("\r")
    	method = request_content[0].split()[0]
    	url = request_content[0].split()[1]
    	if method != "GET":
    		response = "HTTP/1.1 405 Method Not Allowed\r\n"
    		return response
    	path = "www"+url

    	if not self.path_secure(path):
    		response = "HTTP/1.1 404 Not FOUND\r\n"
    		return response
    	try:
    		file = open(path, "r")
    		content = file.read()
    		response = "HTTP/1.1 200 OK\r\nContent-Type: text/"+os.path.splitext(path)[1][1:]+"\r\n\r\n"+content
    	except FileNotFoundError:
    		response = "HTTP/1.1 404 Not FOUND\r\n"
    	except:
    		if path[-1] != "/":
    			redirection = "http://127.0.0.1:8080"+ url + "/"
    			print("Redirect to:    ",redirection)
    			path = os.path.join(path, "index.html")
    			file = open(path, "r")
    			content = file.read()
    			response = "HTTP/1.1 307 Temporary Redirect\r\nLocation: " + redirection + "\r\nContent-Type: text/html\r\n\r\n"+content
    		else:
    			path = os.path.join(path, "index.html")	
    			file = open(path, "r")
    			content = file.read()
    			response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"+content

    	return response

    def path_secure(self, path):
    	current_path = os.path.abspath("www")
    	request_path = os.path.abspath(path)
    	if current_path in request_path:
    		return True
    	return False


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
