#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'server start module'

__author__ = 'hesc'

from wsgiref.simple_server import make_server
import json
import sys

#read json from file
def read_json(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def path_equal(path1, path2):
    path1 = path1.strip().lower()
    path2 = path2.strip().lower()

    while path1.startswith('/'):
        path1 = path1[1:]

    while path1.endswith('/') or path1.endswith('?'):
        path1 = path1[:-1]

    while path2.startswith('/'):
        path2 = path2[1:]

    while path2.endswith('/') or path2.endswith('?'):
        path2 = path2[:-1]

    return path1 == path2

def find_response(path, response_list):
    if not response_list:
        return None
    if not isinstance(response_list, list):
        return None
    find_result = [response for response in response_list if path_equal(response.get('path'), path)]
    if not find_result:
        return None
    if not len(find_result):
        return None
    return find_result[0].get('response')

def application(environ, start_response):
    request_path = environ['PATH_INFO']
    json_str = read_json('donald.json')
    response_list = json.loads(json_str)
    response = find_response(request_path, response_list)
    response = json.dumps(response)

    start_response('200 OK', [('Content-Type', 'text/json'), ('Content-Length', str(len(response)))])
    return [response.encode('utf-8')]

def str2int(str):
    try:
        return int(str)
    except ValueError:
        return None

def start_server(port=9088):
    httpd = make_server('', port, application)
    print('Serving HTTP on port ', port)
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv)>1:
        start_server(str2int(sys.argv[1]))
    else:
        start_server()