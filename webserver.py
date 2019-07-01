from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith("/hello"):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			message = ""
			message += "<html><body>Hello!</body></html>"
			message += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'> </form>"
			message +="</body></html>"
			self.wfile.write(message.encode())
			print (message)
			return


		else:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		#try:
		self.send_response(301)
		self.send_header('Content-type','text/html')
		self.end_headers()

		ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
		pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

		if ctype == 'multipart/form-data':
			fields = cgi.parse_multipart(self.rfile,pdict)
			messagecontent = fields.get('message')

			message = ""
			message +="<html><body>"
			message += " <h2> Okay, how about this?</h2> "
			message += " <h1> %s </h1> " % messagecontent[0].decode()
			message +=''' <form method=""POST" enctype= "multipart/form-data" action="/hello"><h2> What would you like me to say?</h2><input name ="message" type ="text"> <input type = "submit" value = "Submit"> </form> '''
			message +="</body></html>"

			self.wfile.write(message.encode())
			print('next goes message')
			print(message)


		#except:
		#	print('things don\'t work out, they never do at the beginning')
		#	pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print ("Web Server running on port %s" % port)
		server.serve_forever()
	except KeyboardInterrupt:
		print (" ^C entered, stopping web server....")        
		server.socket.close()


if __name__ == '__main__':
	main()

