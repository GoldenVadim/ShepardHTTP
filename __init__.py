from socket import socket,AF_INET6,AF_INET,SOCK_STREAM
from threading import Thread
from http import HTTPMethod
from typing import Callable

class ShepardHTTPExceptions:
    class CoreError(BaseException):...
    class RequestError(BaseException):...

class Request:
    def __init__(self,content):
        """The base class of new request for web-server."""
        try:self.__parse__(content)
        except Exception as e:raise ShepardHTTPExceptions.RequestError(f'Failed to parse request: {e}')
        finally:
            if e:raise e
    def __parse__(self,content:str):
        self.headers,self.data=content.split('\r\n\r\n',1)
        self.headers=self.headers.split('\r\n')
        self.method=self.headers.pop(0)
        self.method=self.method.split(maxsplit=2)
        self.method,self.path,self.version=HTTPMethod(self.method[0]),self.method[1],self.method[2]
        self.headers=[tuple(header.split(': ',2))for header in self.headers]

class ShepardHTTPEvents:
    request=None
    get_request=None
    post_request=None
    head_request=None
    delete_request=None
    options_request=None
    patch_request=None
    put_request=None

class ShepardHTTP:
    def __init__(self,port:int,host:str,ipv6:bool,timeout:float,recv_buffer:int,backlog:int,*,sock:socket=socket()):
        """The class of ShepardHTTP server instance.

        Arguments:
            * port: Port to bind for web-server.
            * host: Host to bind web-server. It can have '' to bind on local address.

            /!\ Arguments below is used to configure preset of default stage of socket instance.
                If you want to manually configure socket, you can use "sock" argument instead.
            * ipv6: Use IPv6 to bind web-server.
            * timeout: Timeout in seconds.
            * recv_buffer: Number of bytes to receive from client.
            * backlog: idk, lol.
            * sock: Socket to use in web-server. You can use it to manually configure socket instead of use args."""
        self.port = port
        self.host = host
        self.ipv6 = ipv6
        self.timeout = timeout
        self.recv_buffer = recv_buffer
        self.backlog = backlog
        self.socket = sock
        self.events = ShepardHTTPEvents
    def reset_socket(self):
        """Close and reset the socket instance of web-server to its default state. It"""
        self.socket.close()
        self.socket = socket(AF_INET6 if self.ipv6 else AF_INET,SOCK_STREAM)
        self.socket.settimeout(self.timeout)
    def event(self,event_func:Callable):
        if event_func.__name__ in self.events.__dict__:setattr(self.events,event_func.__name__,event_func)
        else:raise ShepardHTTPExceptions.CoreError(f'"{event_func}" is invalid event.')
    def open(self):
        self.socket.bind((self.host,self.port))
        self.socket.listen(self.backlog)
    def accept(self):
        sock,addr = self.socket.accept()
        Thread(target=self.events.request,args=(Request(sock.recv(self.recv_buffer).decode()),(sock,addr)),daemon=False).start()