from socket import socket,AF_INET6,AF_INET,SOCK_STREAM
from typing import Callable

class Request:
    def __init__(self,content:str):
        """The base class of new request for web-server."""


class ShepardHTTPEvents:
    request:Callable=None

class ShepardHTTP:
    def __init__(self,port:int,host:str,ipv6:bool,timeout:float,recv_buffer:int,backlog:int,*,sock:socket=socket(),verbose:bool=False,log:str=None):
        """The class of ShepardHTTP server instance.

        Arguments:
            * port: Socket to bind for web-server.
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
        self.events = ShepardHTTPEvents()
    def reset_socket(self):
        """Close and reset the socket instance of web-server to its default state. It"""
        self.socket.close()
        self.socket = socket(AF_INET6 if self.ipv6 else AF_INET,SOCK_STREAM)
        self.socket.settimeout(self.timeout)
    def open(self):
        self.socket.bind((self.host,self.port))
        self.socket.listen(self.backlog)
    def accept(self):
        sock,addr = self.socket.accept()
