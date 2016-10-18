#!/usr/bin/env python

# Send a code formatting request to the server

# TODO: write output to a file

import http.client
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Server application for Grand Central Format, the centralized formatting server.')
    parser.add_argument('--server-address', '-s', default='localhost:8010', help='Address of the server to connect to in "address:port" format. Defaults to localhost:8010.')
    parser.add_argument('--input-file', '-f', help='Read input from a file rather than the stdin.')
    parser.add_argument('--output-file', '-o', help='Write output to a file rather than the stdout.')
    parser.add_argument('--diff', '-d', help='Indicates the input to be formatted is a version control diff rather than a complete file or snippet.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    unformatted_code = ''
    if args.input_file:
        with open(args.input_file, 'rt') as infile:
            unformatted_code = infile.read()
    else:
        unformatted_code = sys.stdin.read()
    
    req = 'format'
    if args.diff:
        req = 'format/diff'
    
    conn = http.client.HTTPConnection(args.server_address)
    conn.request('POST', req, body=unformatted_code.encode('utf-8'), headers={'Content-type': 'text/plain'})
    response = conn.getresponse()
    formatted_code = response.read().decode('utf-8')
    # TODO: test 'format/diff'
    
    # if server responded successfully, output the formatted code, otherwise output the original code
    outfile = open(args.output_file, 'wt') if args.output_file else sys.stdout
    if response.status == 200:
        outfile.write(formatted_code)
    else:
        outfile.write(unformatted_code)
        sys.exit(-1)