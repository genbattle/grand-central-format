#!/usr/bin/env python

# create a web server that accepts post requests with code snippets and sends back formatted code

# TODO: implement proper logging

import http.server
import argparse
import subprocess
import os.path

clang_path = '/usr/share/clang'

class GrandCentralFormatHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('Content-type') == 'text/plain':
            print(self.path)
            print(self.headers.get('Content-type'))
            content_len = int(self.headers.get('Content-length'))
            body = self.rfile.read(content_len)
            print('body: {}'.format(body.decode('utf-8')))
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            output = body
            if self.path == 'format/full':
                output = format_input(body.decode('utf-8')).encode('utf-8')
            elif self.path == 'format/diff':
                output = format_diff(body.decode('utf-8')).encode('utf-8')
            self.wfile.write(output)
            print('wrote response')
        else:
            self.send_error(400, 'Incorrect content type, must be text/plain')

'''
Format the given input text and return the formatted version.
'''
def format_input(unformatted):
    proc = subprocess.run(['clang-format', '-style=file'], input=unformatted, stdout=subprocess.PIPE, universal_newlines=True)
    return proc.stdout

'''
Format the given diff and return the formatted version.
'''
def format_diff(unformatted):
    proc = subprocess.run([clang_path + 'clang-format-diff.py', '-style=file'], input=unformatted, stdout=subprocess.PIPE, universal_newlines=True)
    return proc.stdout

def parse_args():
    parser = argparse.ArgumentParser(description='Server application for Grand Central Format, the centralized formatting server.')
    parser.add_argument('--port', '-p', type=int, default=8010, help='Port to listen on for incoming connections. Defaults to 8010.')
    parser.add_argument('--clang-format-path', default='/usr/share/clang', help='Clang tools folder path, continaing clang-format-diff.py. Defaults to /usr/share/clang.')
    return parser.parse_args()

if __name__ == '__main__':
    print('+++ Grand Central Format Server Startup +++')
    args = parse_args()
    clang_path = os.path.normpath(args.clang_format_path)
    
    serv = http.server.HTTPServer(('', args.port), GrandCentralFormatHandler)
    
    print('INFO: starting server on port {}'.format(args.port))
    
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
    
    serv.server_close()
    
    print('--- Grand Central Format Server Shutdown ---')