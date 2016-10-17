#!/usr/bin/env python

# create a web server that accepts post requests with code snippets and sends back formatted code

# TODO: handle diff mode for format/diff

import http.server
import argparse
import subprocess

class GrandCentralFormatHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # TODO: validate content type?
        print(self.path)
        print(self.headers.get('Content-type'))
        content_len = int(self.headers.get('Content-length'))
        body = self.rfile.read(content_len)
        print('body: {}'.format(body.decode('utf-8')))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(format_input(body.decode('utf-8')).encode('utf-8'))
        print('wrote response')

def parse_args():
    parser = argparse.ArgumentParser(description='Server application for Grand Central Format, the centralized formatting server.')
    parser.add_argument('--port', '-p', type=int, default=8010, help='Port to listen on for incoming connections. Defaults to 8010.')
    return parser.parse_args()

'''
Format the given input text and return the formatted version.
'''
def format_input(unformatted):
    proc = subprocess.run(['clang-format', '-style=file'], input=unformatted, stdout=subprocess.PIPE, universal_newlines=True)
    return proc.stdout

if __name__ == '__main__':
    print('+++ Grand Central Format Server Startup +++')
    args = parse_args()
    
    serv = http.server.HTTPServer(('', args.port), GrandCentralFormatHandler)
    
    print('INFO: starting server on port {}'.format(args.port))
    
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
    
    serv.server_close()
    
    print('--- Grand Central Format Server Shutdown ---')