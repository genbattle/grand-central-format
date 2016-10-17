#!/usr/bin/env python

# Send a code formatting request to the server

# TODO: read input from stdin, output to stdout
# TODO: read input from a file
# TODO: write output to a file
# TODO: diff mode

import http.client
# import sys.stdin
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Server application for Grand Central Format, the centralized formatting server.')
    parser.add_argument('--server-address', '-s', default='localhost:8010', help='Address of the server to connect to in "address:port" format. Defaults to localhost:8010.')
    parser.add_argument('--input-file', '-f', help='Read input from a file rather than the stdin.')
    parser.add_argument('--output-file', '-o', help='Write output to a file rather than the stdout.')
    parser.add_argument('--diff', '-d', help='Indicates the input to be formatted is a version control diff rather than a complete file or snippet.')
    return parser.parse_args()

if __name__ == '__main__':
    conn = http.client.HTTPConnection('localhost', 8010)
    unformatted_code = '''
    #include <iostream>

int main()   {
std::cout <<"Hello, world!" <<  std::endl;
 return 0;
}

'''
    conn.request('POST', 'format/full', body=unformatted_code.encode('utf-8'), headers={'Content-type': 'text/plain'})
    response = conn.getresponse()
    print('got response!')
    formatted_code = response.read().decode('utf-8')
    # TODO: test 'format/diff'
    print('formatted code:')
    print(formatted_code)