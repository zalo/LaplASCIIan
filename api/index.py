from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        # Attempt to read the body of the request
        body = self.rfile.read(int(self.headers.get("Content-Length")))

        message = 'Hello from Python from a ZEIT Now Serverless Function!   You submitted: '+str(body)
        self.wfile.write(message.encode())
        return