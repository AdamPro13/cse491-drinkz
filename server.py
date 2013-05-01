#!/usr/bin/env python

import random
import socket
import time
import StringIO

from drinkz.app import SimpleApp

the_app = SimpleApp()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr

    buffer = c.recv(1024)

    while "\r\n\r\n" not in buffer:
        data = c.recv(1024)
        if not data:
         break
        buffer += data
        print (buffer,)
        time.sleep(1)

    print 'got entire request:', (buffer,)

    # now, parse the HTTP request.
    lines = buffer.splitlines()
    request_line = lines[0]
    request_type, path, protocol = request_line.split()
    print 'GOT', request_type, path, protocol

    request_headers = lines[1:]                  # irrelevant, discard for GET.
    rq_headers = {}
    data = ''
    for header in request_headers:
        parts = header.split(': ')
        if len(parts) >= 2:
            rq_headers[parts[0].lower()] = parts[1]

    query_string = ""
    if '?' in path:
        path, query_string = path.split('?', 1)

    # build environ & start_response
    environ = {}
    environ['PATH_INFO'] = path
    environ['QUERY_STRING'] = query_string
    environ['REQUEST_METHOD'] = request_type
    if 'content-length' in rq_headers:
        environ['CONTENT_LENGTH'] = rq_headers['content-length']
    if request_type.lower() == 'post':
        data = request_headers[-1]
        environ['wsgi.input'] = StringIO.StringIO(data)

    d = {}
    def start_response(status, headers):
        d['status'] = status
        d['headers'] = headers

    try:
        results = the_app(environ, start_response)
    except:
        c.close()
        exit()
    # note -- start_response is called by the_app.

    response_headers = []
    for k, v in d['headers']:
        h = "%s: %s" % (k, v)
        response_headers.append(h)
      
    response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)

    c.send("HTTP/1.0 %s\r\n" % d['status'])
    c.send(response)
    c.close()
