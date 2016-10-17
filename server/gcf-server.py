#!/usr/bin/env python

# create a web server that accepts post requests with code snippets and sends back formatted code

import http.server
import argparse

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
        self.wfile.write('test response'.encode('utf-8'))
        print('wrote response')

def parse_args(args):
    parser = argparse.ArgumentParser(description='')

if __name__ == '__main__':
    print('+++ Grand Central Format Server Startup +++')
    serv = http.server.HTTPServer(('', 8010), GrandCentralFormatHandler)
    
    print('INFO: starting server on port {}', 8010)
    
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
    
    serv.server_close()
    
    print('--- Grand Central Format Server Shutdown ---')