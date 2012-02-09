import socket
import select
import threading
import pickle
import time

BUFFSIZE = 1024

#tasks for server:
# apply a callback for every message arrived
# redistribute the messages for all clients
class Server(threading.Thread):
  def __init__(self, port, connNum, callback):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind(('', port))
    self.sock.listen(5)
    self.num = connNum
    self.callback = callback
    
    threading.Thread.__init__ ( self )
  
  def run(self):
    #accept connections
    self.clients = []
    for i in xrange(0, self.num):
      self.clients.append(self.sock.accept()[0])
    self.exit = False
    
    while not self.exit:
      toRead, toWrite, inError = select.select(self.clients, self.clients, self.clients)
      for conn in toRead:
        msg = conn.recv(BUFFSIZE)
        #distribute message amongst all other writeable clients
        dist = toWrite[:]
        dist.remove(conn)
        for conn2 in dist:
          conn2.sendall(msg)
        obj = pickle.loads(msg)
        self.callback(obj)
        
      time.sleep(0.1)

  def distribute(self, event):
    msg = pickle.dumps(event)
    for conn in self.clients:
      conn.sendall(msg)

class Client(threading.Thread):
  def __init__(self, host, port, callback):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    self.callback = callback
    threading.Thread.__init__ ( self )

  def run(self):
    self.exit = False

    while not self.exit:
      msg = self.sock.recv(BUFFSIZE)
      obj = pickle.loads(msg)
      self.callback(obj)

  def distribute(self, event):
    msg = pickle.dumps(event)
    self.sock.sendall(msg)

