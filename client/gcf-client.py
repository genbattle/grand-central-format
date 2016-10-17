#!/usr/bin/env python

# Send a code formatting request to the server

import http.client

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