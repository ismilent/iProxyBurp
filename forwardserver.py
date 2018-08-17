# coding: utf-8

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

ECHO_PORT = 27080

class RequestHandler(BaseHTTPRequestHandler):

    def do_REQUEST(self):
        request_path = self.path
        print('Recving request connction...')
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0

        self.send_response(200)
        self.end_headers()

        self.wfile.write(self.rfile.read(length))

    def do_RESPONSE(self):
        request_path = self.path
        print('Recving Response connction...')
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0

        self.send_response(200)
        self.end_headers()

        self.wfile.write(self.rfile.read(length))


def main():
    print('Listening on localhost: %d' % ECHO_PORT)
    server = HTTPServer(('', ECHO_PORT), RequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    print('Staring echo server on port %d' % ECHO_PORT)
    main()