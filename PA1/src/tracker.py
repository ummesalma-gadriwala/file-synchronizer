import socket, sys, threading, json,time,optparse,os

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def validate_port(x):
    if not x.isdigit():
        return False
    i = int(x)
    if i < 0 or i > 65535:
            return False
    return True

class Tracker(threading.Thread):
    def __init__(self, port, host='0.0.0.0'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.BUFFER_SIZE = 8192
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {} # current connections  self.users[(ip,port)] = {'exptime':}
        self.files = {} #{'ip':,'port':,'mtime':} modification time
        self.lock = threading.Lock()
        try:
            #YOUR CODE
            #Bind to address and port
            self.server.bind((host, port))
            
        except socket.error:
            print('Bind failed %s' % (socket.error))
            sys.exit()
        #YOUR CODE
        #listen for connections
        #backlog specifies the max number of queued connections and should be at least 1; max 5
        self.server.listen(5)
        print('The server is ready to receive')
        

    def check_user(self):
        #YOUR CODE
        #checking users are alive
        # keepalive message sent every 180 seconds
        # remove all files with the same port
        print "before: self.users", self.users
        print "before: self.files", self.files
        for user in self.users.keys():
        	uip = user[0]
        	uport = user[1]
        	uexptime = self.users[user]
        	if uexptime < 0:
        		# kick out client
        		self.lock.acquire()
        		self.users.pop(user) # remove from self.users
        		self.lock.release()
        		for f in self.files.keys(): # remove files from self.files
        			print "files", self.files[f], self.files[f]["port"], uport
        			if self.files[f]["port"] == uport:
        				self.lock.acquire()
        				self.files.pop(f)
        				self.lock.release()
        		print "after: self.users", self.users
        		print "after: self.files", self.files
        	else:
        		# decrement timer by 5
        		self.users[user] = uexptime - 5   	
        
        threading.Timer(5, self.check_user).start()
      	
        
        
    #Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    def run(self):
    	# thread to execute check_user executes every 5 seconds
    	threading.Timer(5, self.check_user).start()
    	#t =threading.Timer(10,self.check_user)
    	#t.start()
    	
        print('Waiting for connections on port %s' % (self.port))
        while True:
            #YOUR CODE
            #accept incoming connection and create a thread for receiving messages from FileSynchronizer
            conn, addr = self.server.accept()
            #self.users[addr] = 180.0 # expire time
            threading.Thread(target=self.proces_messages, args=(conn, addr)).start()

    def proces_messages(self, conn, addr):
        conn.settimeout(180.0)
        print 'Client connected with ' + addr[0] + ':' + str(addr[1])
        while True:										
            #receive data
            data = ''
            while True:
                part = conn.recv(self.BUFFER_SIZE)
                data =data+ part
                if len(part) < self.BUFFER_SIZE:
                    break
            #YOUR CODE
            # check if the received data is a json string and load the json string
            #print("data" + data)
            if (is_json(data)):
            	data_dic = json.loads(data)
            	print "client server" + addr[0] + ":" + str(data_dic["port"])
            	self.lock.acquire()
            	self.users[(addr[0],data_dic["port"])] = 180 #expire time
            	self.lock.release()
            	if data_dic.has_key("files"):
            		# sync and send files json data
            		files = data_dic["files"] #list
            		fport = data_dic["port"]
            		for f in files:
            			#THIS IS BAD BUT WORKS!
            			f = eval(json.dumps(f))
            			fname = f["name"]
            			fip = addr[0]
            			fmtime = f["mtime"]
            			#print (fname, fip, fmtime)
            			#{'ip':,'port':,'mtime':}
            			self.lock.acquire()
            			# check modification time here
            			self.files[fname] = {'ip': fip,'port': fport,'mtime': fmtime}
            			self.lock.release()
      	      	print("self.files",self.files)	
            	#sending files
            	conn.sendall(json.dumps(self.files))
            else:
            	print ("Invalid data")
            	# lock released by client on exit
            	conn.sendall(json.dumps(self.files))
            	break
                                
        conn.close() # Close

def is_json(data):
    try:
        string = json.loads(data)
    except ValueError, e:
        return False
    return True
        
if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog ServerIP ServerPort")
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.error("No ServerIP and ServerPort")
    elif len(args) < 2:
        parser.error("No  ServerIP or ServerPort")
    else:
        if validate_ip(args[0]) and validate_port(args[1]):
            server_ip = args[0]
            server_port = int(args[1])
        else:
            parser.error("Invalid ServerIP or ServerPort")
    tracker = Tracker(server_port,server_ip)
    tracker.start()
